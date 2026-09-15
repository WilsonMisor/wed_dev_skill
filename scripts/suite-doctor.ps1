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
$AgentsHome = if ($env:AGENTS_HOME) { $env:AGENTS_HOME } else { Join-Path $HOME '.agents' }
$SkillRoot = if ($env:CODEX_SKILLS_HOME) { $env:CODEX_SKILLS_HOME } else { Join-Path $AgentsHome 'skills' }

function Require-Command([string]$Name) {
    if (-not (Get-Command $Name -ErrorAction SilentlyContinue)) { throw ('Missing required command: ' + $Name) }
}

function Invoke-Checked([string]$Label, [scriptblock]$Block) {
    Write-Output ('==> ' + $Label)
    & $Block
    if ($LASTEXITCODE -ne 0) { throw ($Label + ' failed with exit code ' + $LASTEXITCODE) }
}

function Get-Head([string]$Repo) {
    return (& git -C $Repo rev-parse HEAD).Trim()
}

Require-Command 'git'
Require-Command 'python'

foreach ($Repo in @($BlueprintRoot, $PreosRoot, $GstackRoot)) {
    if (-not (Test-Path (Join-Path $Repo '.git'))) { throw ('Repository missing .git: ' + $Repo) }
    Invoke-Checked ('verify git repository ' + $Repo) { & git -C $Repo rev-parse HEAD | Out-Null }
}

if (Test-Path $SuiteLockPath) {
    $Lock = Get-Content -LiteralPath $SuiteLockPath -Raw | ConvertFrom-Json
    foreach ($Component in $Lock.components) {
        $RepoPath = Join-Path $SuiteRoot $Component.path
        if (-not (Test-Path $RepoPath)) { throw ('Suite lock component path missing: ' + $Component.path) }
        $Actual = Get-Head $RepoPath
        if ($Component.commit -and $Actual -ne $Component.commit) {
            throw ('Suite lock drift for ' + $Component.name + ': expected ' + $Component.commit + ', got ' + $Actual)
        }
    }
    Write-Output ('Suite lock: PASS ' + $SuiteLockPath)
} else {
    Write-Output ('Suite lock: NOT FOUND ' + $SuiteLockPath)
}

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
    $RequiredSkills = @('ai-product-delivery-blueprint','preos','preos-risk-model','preos-production-plan','gstack')
    foreach ($Skill in $RequiredSkills) {
        $Path = Join-Path $SkillRoot $Skill
        if (-not (Test-Path (Join-Path $Path 'SKILL.md'))) { throw ('Installed skill missing SKILL.md: ' + $Path) }
    }
    $AgentRoot = Join-Path $CodexHome 'agents'
    $AgentCount = (Get-ChildItem -Path $AgentRoot -Filter 'vt_*.toml' -ErrorAction SilentlyContinue).Count
    if ($AgentCount -lt 9) { throw 'Virtual Team agent metadata is incomplete' }
    Write-Output ('Installed skills: PASS ' + $SkillRoot)
} else {
    Write-Output 'Installed skills: SKIPPED by caller'
}

Write-Output 'Suite doctor: PASS'
Write-Output ('Blueprint ' + (Get-Head $BlueprintRoot))
Write-Output ('PREOS ' + (Get-Head $PreosRoot))
Write-Output ('gstack ' + (Get-Head $GstackRoot))
