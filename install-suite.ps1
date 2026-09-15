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
$PreosRoot = Resolve-Path $PreosPath
$GstackRoot = Resolve-Path $GstackPath
$CodexHome = if ($env:CODEX_HOME) { $env:CODEX_HOME } else { Join-Path $HOME '.codex' }
$AgentsHome = if ($env:AGENTS_HOME) { $env:AGENTS_HOME } else { Join-Path $HOME '.agents' }
$SkillRoot = if ($env:CODEX_SKILLS_HOME) { $env:CODEX_SKILLS_HOME } else { Join-Path $AgentsHome 'skills' }
$AgentRoot = Join-Path $CodexHome 'agents'

function Require-Command([string]$Name) {
    if (-not (Get-Command $Name -ErrorAction SilentlyContinue)) { throw ('Missing required command: ' + $Name) }
}

function Invoke-Checked([string]$Label, [scriptblock]$Block) {
    Write-Output ('==> ' + $Label)
    & $Block
    if ($LASTEXITCODE -ne 0) { throw ($Label + ' failed with exit code ' + $LASTEXITCODE) }
}

function Invoke-SuiteDoctor {
    $Args = @('-File', (Join-Path $BlueprintRoot 'scripts\suite-doctor.ps1'), '-PreosPath', $PreosRoot, '-GstackPath', $GstackRoot, '-SuiteLockPath', $SuiteLockPath)
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
    foreach ($Skill in @('ai-product-delivery-blueprint','preos','preos-risk-model','preos-production-plan','gstack')) {
        $Path = Join-Path $SkillRoot $Skill
        $ResolvedTarget = [System.IO.Path]::GetFullPath($Path)
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
    if ($IsWindows) {
        Require-Command 'bash'
        Invoke-Checked 'install gstack for Codex with namespaced prefix' { & bash $Setup --host codex --prefix }
    } else {
        Invoke-Checked 'install gstack for Codex with namespaced prefix' { & $Setup --host codex --prefix }
    }
}

$RequiredSkills = @('ai-product-delivery-blueprint','preos','preos-risk-model','preos-production-plan','gstack')
foreach ($Skill in $RequiredSkills) {
    $Path = Join-Path $SkillRoot $Skill
    if (-not (Test-Path (Join-Path $Path 'SKILL.md'))) { throw ('Installed skill missing SKILL.md: ' + $Path) }
}
$AgentCount = (Get-ChildItem -Path $AgentRoot -Filter 'vt_*.toml' -ErrorAction SilentlyContinue).Count
if ($AgentCount -lt 9) { throw 'Virtual Team agent metadata is incomplete' }

Invoke-SuiteDoctor
$BlueprintHead = (& git -C $BlueprintRoot rev-parse --short HEAD).Trim()
$PreosHead = (& git -C $PreosRoot rev-parse --short HEAD).Trim()
$GstackHead = (& git -C $GstackRoot rev-parse --short HEAD).Trim()
Write-Output ('Suite ' + $Mode + ' health: PASS')
Write-Output ('Blueprint ' + $BlueprintHead)
Write-Output ('PREOS ' + $PreosHead)
Write-Output ('gstack ' + $GstackHead)
Write-Output ('Skills: ' + $SkillRoot)
Write-Output ('Agents: ' + $AgentRoot)
