$ErrorActionPreference = 'Stop'
# Manifest-owned Blueprint skill: ai-product-delivery-blueprint
$Root = Resolve-Path (Join-Path $PSScriptRoot '..')
$CodexHome = if ($env:CODEX_HOME) { $env:CODEX_HOME } else { Join-Path $HOME '.codex' }
$SkillRoot = if ($env:CODEX_SKILL_ROOT) { $env:CODEX_SKILL_ROOT } elseif ($env:CODEX_SKILLS_HOME) { $env:CODEX_SKILLS_HOME } else { Join-Path $CodexHome 'skills' }
$AgentRoot = Join-Path $CodexHome 'agents'
$Dist = Join-Path $Root 'codex-distribution'
$Manifest = Get-Content -LiteralPath (Join-Path $Root 'CODEX-DISTRIBUTION.json') -Raw | ConvertFrom-Json
$Skills = @($Manifest.skills)
if ($Skills.Count -ne 1 -or -not $Skills[0].name) { throw 'Blueprint CODEX-DISTRIBUTION.json must declare exactly one skill' }
$SkillName = [string]$Skills[0].name

if (-not (Test-Path (Join-Path $Dist 'skills'))) {
    & python (Join-Path $Root 'scripts\build_codex_distribution.py')
}

$SkillSource = Join-Path $Dist ('skills\' + $SkillName)
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