$ErrorActionPreference = 'Stop'
$Root = Resolve-Path (Join-Path $PSScriptRoot '..')
$CodexHome = if ($env:CODEX_HOME) { $env:CODEX_HOME } else { Join-Path $HOME '.codex' }
$AgentsHome = if ($env:AGENTS_HOME) { $env:AGENTS_HOME } else { Join-Path $HOME '.agents' }
$SkillRoot = if ($env:CODEX_SKILLS_HOME) { $env:CODEX_SKILLS_HOME } else { Join-Path $AgentsHome 'skills' }
$AgentRoot = Join-Path $CodexHome 'agents'
$Dist = Join-Path $Root 'codex-distribution'
$SkillName = 'ai-product-delivery-blueprint'

if (-not (Test-Path (Join-Path $Dist 'skills'))) {
    & python (Join-Path $Root 'scripts\build_codex_distribution.py')
}

$SkillSource = Join-Path $Dist 'skills\ai-product-delivery-blueprint'
$AgentsSource = Join-Path $Dist 'agents'
if (-not (Test-Path (Join-Path $SkillSource 'SKILL.md'))) { throw 'Blueprint distribution missing SKILL.md' }
if (-not (Test-Path $AgentsSource)) { throw 'Blueprint distribution missing agents directory' }

New-Item -ItemType Directory -Force -Path $SkillRoot | Out-Null
New-Item -ItemType Directory -Force -Path $AgentRoot | Out-Null
$BackupRoot = Join-Path $CodexHome ('framework-install-backups\blueprint-' + (Get-Date -Format 'yyyyMMddTHHmmssZ'))

function Backup-ExistingPath([string]$Path) {
    if (Test-Path $Path) {
        New-Item -ItemType Directory -Force -Path $BackupRoot | Out-Null
        $Name = Split-Path $Path -Leaf
        Move-Item -LiteralPath $Path -Destination (Join-Path $BackupRoot $Name)
    }
}

$TargetSkill = Join-Path $SkillRoot $SkillName
Backup-ExistingPath $TargetSkill
Copy-Item -Recurse -Force $SkillSource $TargetSkill

Get-ChildItem -Path $AgentsSource -Filter '*.toml' | ForEach-Object {
    $TargetAgent = Join-Path $AgentRoot $_.Name
    Backup-ExistingPath $TargetAgent
    Copy-Item -Force $_.FullName $TargetAgent
}

if (-not (Test-Path (Join-Path $TargetSkill 'SKILL.md'))) { throw 'Installed Blueprint skill missing SKILL.md' }
$AgentCount = (Get-ChildItem -Path $AgentRoot -Filter 'vt_*.toml').Count
if ($AgentCount -lt 9) { throw 'Installed Blueprint agents incomplete' }
$Commit = (& git -C $Root rev-parse --short HEAD).Trim()
Write-Output ('Installed Blueprint skill under ' + $SkillRoot)
Write-Output ('Installed Blueprint agents under ' + $AgentRoot)
Write-Output ('Blueprint commit ' + $Commit)
if (Test-Path $BackupRoot) { Write-Output ('Previous governed targets backed up under ' + $BackupRoot) }
