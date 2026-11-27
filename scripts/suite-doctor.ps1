param(
    [string]$PreosPath,
    [string]$GstackPath,
    [string]$SuiteLockPath,
    [switch]$SkipInstalledSkillCheck,
    [switch]$SkipGstackValidation
)
$ErrorActionPreference = 'Stop'
$BlueprintRoot = Resolve-Path (Join-Path $PSScriptRoot '..')
$SuiteRoot = Resolve-Path (Join-Path $BlueprintRoot '..')
if (-not $PreosPath) { $PreosPath = Join-Path $SuiteRoot 'PREOS' }
if (-not $GstackPath) { $GstackPath = Join-Path $SuiteRoot 'gstack' }
if (-not $SuiteLockPath) { $SuiteLockPath = Join-Path $SuiteRoot 'SUITE-LOCK.json' }
$PreosRoot = Resolve-Path $PreosPath
$GstackRoot = Resolve-Path $GstackPath
$CodexHome = if ($env:CODEX_HOME) { $env:CODEX_HOME } else { Join-Path $HOME '.codex' }
$SkillRoot = if ($env:CODEX_SKILL_ROOT) { $env:CODEX_SKILL_ROOT } elseif ($env:CODEX_SKILLS_HOME) { $env:CODEX_SKILLS_HOME } else { Join-Path $CodexHome 'skills' }
function Invoke-Checked([string]$Label, [scriptblock]$Block) {
    Write-Output ('==> ' + $Label)
    & $Block
    if ($LASTEXITCODE -ne 0) { throw ($Label + ' failed with exit code ' + $LASTEXITCODE) }
}
function Get-Head([string]$Repo) { return (& git -C $Repo rev-parse HEAD).Trim() }
function Get-ManifestSkills([string]$RepoRoot, [bool]$PrefixGstack = $false) {
    $ManifestPath = Join-Path $RepoRoot 'CODEX-DISTRIBUTION.json'
    if (-not (Test-Path $ManifestPath)) { throw ('Missing distribution manifest: ' + $ManifestPath) }
    $Manifest = Get-Content -LiteralPath $ManifestPath -Raw | ConvertFrom-Json
    $Names = @()
    foreach ($Skill in @($Manifest.skills)) {
        $Name = [string]$Skill.name
        if (-not $Name) { throw ('Malformed skill entry in ' + $ManifestPath) }
        if ($PrefixGstack -and -not $Name.StartsWith('gstack')) { $Name = 'gstack-' + $Name }
        $Names += $Name
    }
    return $Names
}
function Get-SuiteOwnedSkills {
    $Names = @()
    $Names += Get-ManifestSkills $BlueprintRoot $false
    $Names += Get-ManifestSkills $PreosRoot $false
    $Names += Get-ManifestSkills $GstackRoot $true
    $Unique = @($Names | Sort-Object -Unique)
    if ($Names.Count -eq 0 -or $Unique.Count -ne $Names.Count) { throw ('Suite skill inventory is empty or contains duplicate names: ' + $Names.Count) }
    return $Names
}
if (-not (Test-Path $SuiteLockPath)) { throw ('Suite lock missing: ' + $SuiteLockPath) }
$Lock = Get-Content -LiteralPath $SuiteLockPath -Raw | ConvertFrom-Json
$RequiredLockFields = @(
'suite_version','preos_version','preos_commit','blueprint_version','blueprint_commit',
'gstack_version','gstack_commit','integration_contract_version','risk_catalogue_version',
'risk_schema_version','readiness_framework_mapping_version','gate_schema_version',
'virtual_team_contract_version','tested_codex_host_profile','os_runtime_profile',
'selected_skill_root','owned_skill_source','owned_skill_count','owned_skill_ids'
)
foreach ($Field in $RequiredLockFields) {
    if (-not $Lock.PSObject.Properties[$Field] -or -not $Lock.$Field) { throw ('Suite lock missing ' + $Field) }
}
$ExpectedSkills = @(Get-SuiteOwnedSkills)
$LockedSkills = @($Lock.owned_skill_ids)
if ($Lock.owned_skill_count -ne $ExpectedSkills.Count) { throw ('Suite lock owned_skill_count mismatch: ' + $Lock.owned_skill_count + ' != ' + $ExpectedSkills.Count) }
if (($LockedSkills -join "`n") -ne ($ExpectedSkills -join "`n")) { throw 'Suite lock owned_skill_ids do not match manifest-derived inventory' }
if ($Lock.selected_skill_root -ne 'CODEX_HOME/skills') { throw 'Suite lock selected_skill_root must be CODEX_HOME/skills' }
foreach ($Component in @($Lock.components)) {
    if ($Component.path -eq 'PREOS') { $RepoPath = $PreosRoot }
    elseif ($Component.path -eq 'wed_dev_skill') { $RepoPath = $BlueprintRoot }
    elseif ($Component.path -eq 'gstack') { $RepoPath = $GstackRoot }
    else { $RepoPath = Join-Path $SuiteRoot $Component.path }
    if (-not (Test-Path $RepoPath)) { throw ('Suite lock component path missing: ' + $Component.path) }
    $Actual = Get-Head $RepoPath
    if ($Component.commit -and $Actual -ne $Component.commit) {
        throw ('Suite lock drift for ' + $Component.name + ': expected ' + $Component.commit + ', got ' + $Actual)
    }
}
Write-Output ('Suite lock: PASS ' + $SuiteLockPath)
Invoke-Checked 'validate Blueprint' { & python (Join-Path $BlueprintRoot 'scripts\validate_blueprint.py') }
Invoke-Checked 'validate Blueprint source semantics' { & python (Join-Path $BlueprintRoot 'scripts\validate_source_semantics.py') }
$env:PYTHONPATH = Join-Path $PreosRoot 'scripts'
Invoke-Checked 'validate PREOS' { & python (Join-Path $PreosRoot 'scripts\validate-preos.py') }
Invoke-Checked 'validate PREOS PAS v2 remediation artifacts' { & python (Join-Path $PreosRoot 'scripts\validate-pasv2-remediation-artifacts.py') }
if (-not $SkipGstackValidation) {
    Invoke-Checked 'validate gstack PREOS integration' { & python (Join-Path $GstackRoot 'scripts\validate-preos-integration.py') }
    Invoke-Checked 'validate gstack Codex contract applicability' { & python (Join-Path $GstackRoot 'scripts\validate-codex-project-contract-applicability.py') }
    Invoke-Checked 'validate three-repo acceptance' { & python (Join-Path $GstackRoot 'scripts\validate-three-repo-acceptance.py') --blueprint $BlueprintRoot --preos $PreosRoot --gstack $GstackRoot }
} else {
    Write-Output 'gstack bounded validators: SKIPPED by caller'
}
if (-not $SkipInstalledSkillCheck) {
    foreach ($Skill in $ExpectedSkills) {
        $Path = Join-Path $SkillRoot $Skill
        if (-not (Test-Path (Join-Path $Path 'SKILL.md'))) { throw ('Installed skill missing SKILL.md: ' + $Path) }
    }
    $Manifest = Get-Content -LiteralPath (Join-Path $BlueprintRoot 'CODEX-DISTRIBUTION.json') -Raw | ConvertFrom-Json
    $AgentRoot = Join-Path $CodexHome 'agents'
    foreach ($Agent in @($Manifest.agents)) {
        $Name = Split-Path ([string]$Agent.source_path) -Leaf
        if (-not (Test-Path (Join-Path $AgentRoot $Name))) { throw ('Virtual Team agent metadata missing: ' + (Join-Path $AgentRoot $Name)) }
    }
    Invoke-Checked 'verify installed suite file hashes' { & python (Join-Path $BlueprintRoot 'scripts\verify_installed_suite.py') --preos $PreosRoot --gstack $GstackRoot --codex-home $CodexHome --skill-root $SkillRoot }
    Write-Output ('Installed skills: PASS ' + $SkillRoot)
} else {
    Write-Output 'Installed skills: SKIPPED by caller'
}
Write-Output 'Suite doctor: PASS'