param(
# SUITE-LOCK owned_skill_count must remain 63 from CODEX-DISTRIBUTION.json manifests.
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
$SkillRoot = if ($env:CODEX_SKILL_ROOT) { $env:CODEX_SKILL_ROOT } elseif ($env:CODEX_SKILLS_HOME) { $env:CODEX_SKILLS_HOME } else { Join-Path $CodexHome 'skills' }
$AgentRoot = Join-Path $CodexHome 'agents'

function Require-Command([string]$Name) {
    if (-not (Get-Command $Name -ErrorAction SilentlyContinue)) { throw ('Missing required command: ' + $Name) }
}
function Invoke-Checked([string]$Label, [scriptblock]$Block) {
    Write-Output ('==> ' + $Label)
    & $Block
    if ($LASTEXITCODE -ne 0) { throw ($Label + ' failed with exit code ' + $LASTEXITCODE) }
}
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
    $Names += Get-ManifestSkills $PreosPath $false
    $Names += Get-ManifestSkills $GstackPath $true
    $Unique = @($Names | Sort-Object -Unique)
    if ($Names.Count -ne 63 -or $Unique.Count -ne 63) { throw ('Expected 63 unique suite-owned skills, derived ' + $Names.Count) }
    return $Names
}
$OwnedSkills = @(Get-SuiteOwnedSkills)
function Get-LockCommit([string]$ComponentPath) {
    if (-not (Test-Path $SuiteLockPath)) { return $null }
    $Lock = Get-Content -LiteralPath $SuiteLockPath -Raw | ConvertFrom-Json
    foreach ($Component in @($Lock.components)) {
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
function Ensure-BlueprintSelf {
    $Expected = Get-LockCommit 'wed_dev_skill'
    if ($Mode -eq 'update' -or $Mode -eq 'repair') {
        if (-not $AllowUpdate) { throw ('Mode ' + $Mode + ' requires -AllowUpdate') }
        if (Test-Dirty $BlueprintRoot) { throw 'Blueprint repository is dirty; refusing controlled self-update' }
        Invoke-Checked 'fetch Blueprint' { & git -C $BlueprintRoot fetch --all --tags }
        if ($Expected) { Invoke-Checked 'checkout locked Blueprint' { & git -C $BlueprintRoot checkout $Expected } }
    }
    if ($Expected -and $Mode -ne 'install') {
        $Actual = (& git -C $BlueprintRoot rev-parse HEAD).Trim()
        if ($Actual -ne $Expected) { throw ('Blueprint lock drift: expected ' + $Expected + ', got ' + $Actual) }
    }
}
function Backup-SuitePath([string]$Path, [string]$Label) {
    if (Test-Path $Path) {
        $BackupRoot = Join-Path $CodexHome ('framework-install-backups\suite-' + $Label + '-' + (Get-Date -Format 'yyyyMMddTHHmmssZ'))
        New-Item -ItemType Directory -Force -Path $BackupRoot | Out-Null
        Move-Item -LiteralPath $Path -Destination (Join-Path $BackupRoot (Split-Path $Path -Leaf))
    }
}
function Set-SkillFrontmatterName([string]$SkillPath, [string]$Name) {
    $SkillFile = Join-Path $SkillPath 'SKILL.md'
    if (-not (Test-Path $SkillFile)) { throw ('Installed gstack skill missing SKILL.md: ' + $Name) }
    $SkillText = Get-Content -LiteralPath $SkillFile -Raw
    $Updated = [regex]::Replace($SkillText, '(?m)^name:\s*.+$', ('name: ' + $Name), 1)
    [System.IO.File]::WriteAllText((Resolve-Path $SkillFile).Path, $Updated, [System.Text.UTF8Encoding]::new($false))
}
function Install-GstackCodexSkills {
    Invoke-Checked 'materialize gstack Codex distribution' { & python (Join-Path $GstackRoot 'scripts\build_codex_distribution.py') }
    $ManifestPath = Join-Path $GstackRoot 'CODEX-DISTRIBUTION.json'
    $Manifest = Get-Content -LiteralPath $ManifestPath -Raw | ConvertFrom-Json
    foreach ($Skill in @($Manifest.skills)) {
        $SourceName = [string]$Skill.name
        $TargetName = if ($SourceName.StartsWith('gstack')) { $SourceName } else { 'gstack-' + $SourceName }
        $Source = Join-Path $GstackRoot ('codex-distribution\skills\' + $SourceName)
        if (-not (Test-Path (Join-Path $Source 'SKILL.md'))) { throw ('gstack distribution missing skill: ' + $SourceName) }
        $Target = Join-Path $SkillRoot $TargetName
        Backup-SuitePath $Target 'gstack'
        Copy-Item -Recurse -Force $Source $Target
        Set-SkillFrontmatterName $Target $TargetName
    }
    Write-Output 'Installed gstack Codex skills with namespaced prefix from CODEX-DISTRIBUTION.json'
}
function Invoke-SuiteDoctor {
    $env:CODEX_HOME = $CodexHome
    $env:CODEX_SKILL_ROOT = $SkillRoot
    $env:CODEX_SKILLS_HOME = $SkillRoot
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
    New-Item -ItemType Directory -Force -Path $SkillRoot | Out-Null
    $ResolvedSkillRoot = [System.IO.Path]::GetFullPath($SkillRoot)
    $RootPrefix = $ResolvedSkillRoot.TrimEnd([System.IO.Path]::DirectorySeparatorChar, [System.IO.Path]::AltDirectorySeparatorChar) + [System.IO.Path]::DirectorySeparatorChar
    foreach ($Skill in $OwnedSkills) {
        $Target = Join-Path $SkillRoot $Skill
        $ResolvedTarget = [System.IO.Path]::GetFullPath($Target)
        if (-not $ResolvedTarget.StartsWith($RootPrefix, [System.StringComparison]::OrdinalIgnoreCase)) {
            throw ('Refusing to remove path outside skill root: ' + $ResolvedTarget)
        }
        if (Test-Path $ResolvedTarget) { Remove-Item -LiteralPath $ResolvedTarget -Recurse -Force }
    }
    if (Test-Path $AgentRoot) {
        $Manifest = Get-Content -LiteralPath (Join-Path $BlueprintRoot 'CODEX-DISTRIBUTION.json') -Raw | ConvertFrom-Json
        foreach ($Agent in @($Manifest.agents)) {
            $Name = Split-Path ([string]$Agent.source_path) -Leaf
            if ($Name.StartsWith('vt_') -and $Name.EndsWith('.toml')) {
                $Target = Join-Path $AgentRoot $Name
                if (Test-Path $Target) { Remove-Item -LiteralPath $Target -Force }
            }
        }
    }
    Write-Output 'Suite uninstall: PASS'
    return
}
Require-Command 'git'
Require-Command 'python'
Require-Command 'bun'
$env:CODEX_HOME = $CodexHome
$env:CODEX_SKILL_ROOT = $SkillRoot
$env:CODEX_SKILLS_HOME = $SkillRoot
Ensure-BlueprintSelf
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
    Install-GstackCodexSkills
}
Invoke-SuiteDoctor
Write-Output ('Suite ' + $Mode + ' health: PASS')
