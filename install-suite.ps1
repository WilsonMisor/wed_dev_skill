param(
    [ValidateSet('install','verify','repair','update','uninstall')][string]$Mode = 'install',
    [string]$PreosPath,
    [string]$GstackPath,
    [string]$SuiteLockPath,
    [switch]$SkipGstackSetup,
    [switch]$SkipInstalledSkillCheck,
    [switch]$AllowUpdate
)
$ErrorActionPreference = 'Stop'
$BlueprintRoot = Resolve-Path $PSScriptRoot
$SuiteRoot = Resolve-Path (Join-Path $BlueprintRoot '..')
if (-not $PreosPath) { $PreosPath = Join-Path $SuiteRoot 'PREOS' }
if (-not $GstackPath) { $GstackPath = Join-Path $SuiteRoot 'gstack' }
if (-not $SuiteLockPath) { $SuiteLockPath = Join-Path $SuiteRoot 'SUITE-LOCK.json' }
$CodexHome = if ($env:CODEX_HOME) { $env:CODEX_HOME } else { Join-Path $HOME '.codex' }
$AgentsHome = if ($env:AGENTS_HOME) { $env:AGENTS_HOME } else { Join-Path $HOME '.agents' }
$SkillRoot = if ($env:CODEX_SKILLS_HOME) { $env:CODEX_SKILLS_HOME } else { Join-Path $AgentsHome 'skills' }
$AgentRoot = Join-Path $CodexHome 'agents'
$OwnedSkills = @(
'ai-product-delivery-blueprint','preos','preos-risk-model','preos-architecture-economics',
'preos-production-plan','preos-production-implement','preos-production-learn','preos-project-init',
'preos-handoff','gstack','gstack-review','gstack-qa','gstack-qa-only','gstack-cso',
'gstack-benchmark','gstack-canary','gstack-ship','gstack-investigate','gstack-design-review',
'gstack-devex-review','gstack-health','gstack-spec','gstack-scrape','gstack-document-generate',
'gstack-document-release','gstack-context-save','gstack-context-restore','gstack-preos-handoff'
)
function Require-Command([string]$Name) {
    if (-not (Get-Command $Name -ErrorAction SilentlyContinue)) { throw ('Missing required command: ' + $Name) }
}
function Invoke-Checked([string]$Label, [scriptblock]$Block) {
    Write-Output ('==> ' + $Label)
    & $Block
    if ($LASTEXITCODE -ne 0) { throw ($Label + ' failed with exit code ' + $LASTEXITCODE) }
}
function Get-LockCommit([string]$ComponentPath) {
    if (-not (Test-Path $SuiteLockPath)) { return $null }
    $Lock = Get-Content -LiteralPath $SuiteLockPath -Raw | ConvertFrom-Json
    foreach ($Component in $Lock.components) {
        if ($Component.path -eq $ComponentPath -and $Component.commit) { return $Component.commit }
    }
    if ($ComponentPath -eq 'PREOS' -and $Lock.preos_commit) { return $Lock.preos_commit }
    if ($ComponentPath -eq 'wed_dev_skill' -and $Lock.blueprint_commit) { return $Lock.blueprint_commit }
    if ($ComponentPath -eq 'gstack' -and $Lock.gstack_commit) { return $Lock.gstack_commit }
    return $null
}
function Test-Dirty([string]$Repo) {
    $Dirty = (& git -C $Repo status --porcelain=v1)
    return -not [string]::IsNullOrWhiteSpace(($Dirty -join ''))
}
function Ensure-Repo([string]$Name, [string]$PathText, [string]$Url, [string]$ComponentPath) {
    if (-not (Test-Path $PathText)) {
        if ($Mode -notin @('install','repair','update')) { throw ($Name + ' repository missing: ' + $PathText) }
        $Parent = Split-Path -Parent $PathText
        if (-not (Test-Path $Parent)) { New-Item -ItemType Directory -Path $Parent | Out-Null }
        Invoke-Checked ('clone ' + $Name) { & git clone $Url $PathText }
    }
    if (-not (Test-Path (Join-Path $PathText '.git'))) { throw ($Name + ' repository missing .git: ' + $PathText) }
    $Expected = Get-LockCommit $ComponentPath
    if ($Mode -eq 'update' -or $Mode -eq 'repair') {
        if (-not $AllowUpdate) { throw ('Mode ' + $Mode + ' requires -AllowUpdate') }
        if (Test-Dirty $PathText) { throw ($Name + ' repository is dirty; refusing controlled update') }
        Invoke-Checked ('fetch ' + $Name) { & git -C $PathText fetch --all --tags }
        if ($Expected) { Invoke-Checked ('checkout locked ' + $Name) { & git -C $PathText checkout $Expected } }
    }
    if ($Expected) {
        $Actual = (& git -C $PathText rev-parse HEAD).Trim()
        if ($Actual -ne $Expected -and $Mode -ne 'install') { throw ($Name + ' lock drift: expected ' + $Expected + ', got ' + $Actual) }
    }
}
function Invoke-SuiteDoctor {
    $Args = @('-File', (Join-Path $BlueprintRoot 'scripts\suite-doctor.ps1'), '-PreosPath', $PreosPath, '-GstackPath', $GstackPath, '-SuiteLockPath', $SuiteLockPath)
    if ($SkipInstalledSkillCheck) { $Args += '-SkipInstalledSkillCheck' }
    & powershell @Args
    if ($LASTEXITCODE -ne 0) { throw 'suite doctor failed' }
}
if ($Mode -eq 'verify') {
    Invoke-SuiteDoctor
    return
}
if ($Mode -eq 'update' -and -not $AllowUpdate) {
    throw 'Mode update requires -AllowUpdate so suite drift cannot happen implicitly.'
}
if ($Mode -eq 'uninstall') {
    if (-not $AllowUpdate) { throw 'Mode uninstall requires -AllowUpdate before installed files are removed.' }
    $ResolvedSkillRoot = [System.IO.Path]::GetFullPath($SkillRoot)
    foreach ($Skill in $OwnedSkills) {
        $Target = Join-Path $SkillRoot $Skill
        $ResolvedTarget = [System.IO.Path]::GetFullPath($Target)
        if (-not $ResolvedTarget.StartsWith($ResolvedSkillRoot + [System.IO.Path]::DirectorySeparatorChar)) {
            throw ('Refusing to remove path outside skill root: ' + $ResolvedTarget)
        }
        if (Test-Path $ResolvedTarget) { Remove-Item -LiteralPath $ResolvedTarget -Recurse -Force }
    }
    if (Test-Path $AgentRoot) {
        Get-ChildItem -Path $AgentRoot -Filter 'vt_*.toml' -ErrorAction SilentlyContinue | Remove-Item -Force
    }
    Write-Output 'Suite uninstall: PASS'
    return
}
Require-Command 'git'
Require-Command 'python'
Require-Command 'bun'
Ensure-Repo 'PREOS' $PreosPath 'https://github.com/WilsonMisor/PREOS.git' 'PREOS'
Ensure-Repo 'gstack' $GstackPath 'https://github.com/WilsonMisor/gstack.git' 'gstack'
$PreosRoot = Resolve-Path $PreosPath
$GstackRoot = Resolve-Path $GstackPath
foreach ($Repo in @($BlueprintRoot, $PreosRoot, $GstackRoot)) {
    if (-not (Test-Path (Join-Path $Repo '.git'))) { throw ('Repository missing .git: ' + $Repo) }
    Invoke-Checked ('verify git repository ' + $Repo) { & git -C $Repo rev-parse HEAD | Out-Null }
}
Invoke-Checked 'validate Blueprint' { & python (Join-Path $BlueprintRoot 'scripts\validate_blueprint.py') }
Invoke-Checked 'validate Blueprint source semantics' { & python (Join-Path $BlueprintRoot 'scripts\validate_source_semantics.py') }
$env:PYTHONPATH = Join-Path $PreosRoot 'scripts'
Invoke-Checked 'validate PREOS' { & python (Join-Path $PreosRoot 'scripts\validate-preos.py') }
Invoke-Checked 'validate PREOS PAS v2 remediation artifacts' { & python (Join-Path $PreosRoot 'scripts\validate-pasv2-remediation-artifacts.py') }
Invoke-Checked 'validate gstack PREOS integration' { & python (Join-Path $GstackRoot 'scripts\validate-preos-integration.py') }
Invoke-Checked 'validate gstack Codex contract applicability' { & python (Join-Path $GstackRoot 'scripts\validate-codex-project-contract-applicability.py') }
Invoke-Checked 'validate three-repo acceptance' { & python (Join-Path $GstackRoot 'scripts\validate-three-repo-acceptance.py') --blueprint $BlueprintRoot --preos $PreosRoot --gstack $GstackRoot }
Invoke-Checked 'install Blueprint for Codex' { & (Join-Path $BlueprintRoot 'scripts\install-codex.ps1') }
Invoke-Checked 'install PREOS for Codex' { & (Join-Path $PreosRoot 'scripts\install-codex.ps1') }
if (-not $SkipGstackSetup) {
    $Setup = Join-Path $GstackRoot 'setup'
    if (-not (Test-Path $Setup)) { throw 'gstack setup script is missing' }
    Require-Command 'bash'
    Invoke-Checked 'install gstack for Codex with namespaced prefix' { & bash $Setup --host codex --prefix }
}
Invoke-SuiteDoctor
Write-Output ('Suite ' + $Mode + ' health: PASS')
