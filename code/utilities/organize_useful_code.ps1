$ErrorActionPreference = 'Stop'

$workspace = (Get-Location).Path
$courseRoot = Join-Path $workspace '5203'
$physicsRoot = Join-Path $workspace '电子物理'
$archiveName = 'REVISION_PROJECT_RETAINED_ARTIFACTS_2026-10-01.tar.zst'
$sourceArchive = Join-Path $courseRoot $archiveName
$codeRoot = Join-Path $physicsRoot 'code'
$stageRoot = Join-Path $physicsRoot '.code_extract_staging'
$archiveRoot = Join-Path $physicsRoot 'archives'
$expectedArchiveHash = 'BADEF8DC1B391BA4A3C39762C51BE5D456C76F958C9F9E016C696EEEE325E8B3'

if (-not (Test-Path -LiteralPath $sourceArchive -PathType Leaf)) {
    throw "Source archive not found: $sourceArchive"
}
if (Test-Path -LiteralPath $codeRoot) {
    throw "Target already exists; refusing to overwrite: $codeRoot"
}
if (Test-Path -LiteralPath $stageRoot) {
    throw "Staging directory already exists; inspect it before retrying: $stageRoot"
}

$actualArchiveHash = (Get-FileHash -Algorithm SHA256 -LiteralPath $sourceArchive).Hash
if ($actualArchiveHash -ne $expectedArchiveHash) {
    throw "Archive SHA-256 mismatch. Expected $expectedArchiveHash, got $actualArchiveHash"
}

New-Item -ItemType Directory -Path $stageRoot | Out-Null
$memberList = Join-Path $stageRoot 'archive_members.txt'
$selectedList = Join-Path $stageRoot 'selected_members.txt'

& tar -tf $sourceArchive | Set-Content -LiteralPath $memberList -Encoding utf8
if ($LASTEXITCODE -ne 0) { throw 'Unable to list source archive.' }

$codeExtensions = @('.py', '.cpp', '.ps1')
$selected = foreach ($member in Get-Content -LiteralPath $memberList) {
    $normalized = $member.Replace('\', '/')
    if ($normalized -like 'production_code/*' -and $normalized -notlike 'production_code/escalations/*') {
        $normalized
        continue
    }
    if ($normalized -like 'FINAL_NUMERICAL_FIGURES/*') {
        $normalized
        continue
    }
    if ($normalized -in @(
        '.archive_metadata_2026-10-01/ARCHIVE_CONTENT_MANIFEST.tsv',
        '.archive_metadata_2026-10-01/ARCHIVE_SCOPE.md',
        '.archive_metadata_2026-10-01/SOURCE_FILE_LIST.txt'
    )) {
        $normalized
        continue
    }
    $directPrefix = 'production_code/escalations/'
    if ($normalized.StartsWith($directPrefix)) {
        $remainder = $normalized.Substring($directPrefix.Length)
        if (-not $remainder.Contains('/') -and $codeExtensions -contains [IO.Path]::GetExtension($remainder).ToLowerInvariant()) {
            $normalized
            continue
        }
    }
    $repairPrefix = 'production_code/escalations/degree24_v3_repair/'
    if ($normalized.StartsWith($repairPrefix)) {
        $remainder = $normalized.Substring($repairPrefix.Length)
        if (-not $remainder.Contains('/') -and $codeExtensions -contains [IO.Path]::GetExtension($remainder).ToLowerInvariant()) {
            $normalized
            continue
        }
    }
}
$selected = @($selected | Sort-Object -Unique)
if ($selected.Count -lt 500) { throw "Unexpectedly small selection: $($selected.Count) members" }
$selected | Set-Content -LiteralPath $selectedList -Encoding utf8

& tar -xf $sourceArchive -C $stageRoot -T $selectedList
if ($LASTEXITCODE -ne 0) { throw 'Selective extraction failed.' }

$manifestPath = Join-Path $stageRoot '.archive_metadata_2026-10-01\ARCHIVE_CONTENT_MANIFEST.tsv'
if (-not (Test-Path -LiteralPath $manifestPath -PathType Leaf)) { throw 'Embedded archive manifest was not extracted.' }

$manifest = @{}
foreach ($row in Import-Csv -LiteralPath $manifestPath -Delimiter "`t") {
    $pathValue = $null
    foreach ($candidate in @('path', 'relative_path', 'relpath', 'source_path')) {
        if ($row.PSObject.Properties.Name -contains $candidate) {
            $pathValue = [string]$row.$candidate
            break
        }
    }
    if ($pathValue) { $manifest[$pathValue.Replace('\', '/')] = $row }
}

$verifiedCount = 0
$verifiedBytes = [int64]0
$verificationErrors = [Collections.Generic.List[string]]::new()
foreach ($member in $selected) {
    if ($member.EndsWith('/')) { continue }
    $localPath = Join-Path $stageRoot ($member.Replace('/', '\'))
    if (-not (Test-Path -LiteralPath $localPath -PathType Leaf)) {
        $verificationErrors.Add("missing`t$member")
        continue
    }
    $file = Get-Item -LiteralPath $localPath
    $verifiedCount++
    $verifiedBytes += $file.Length
    if ($manifest.ContainsKey($member)) {
        $row = $manifest[$member]
        $sizeField = @('bytes', 'size', 'length') | Where-Object { $row.PSObject.Properties.Name -contains $_ } | Select-Object -First 1
        $hashField = @('sha256', 'sha_256', 'hash') | Where-Object { $row.PSObject.Properties.Name -contains $_ } | Select-Object -First 1
        if ($sizeField -and [int64]$row.$sizeField -ne $file.Length) {
            $verificationErrors.Add("size`t$member")
        }
        if ($hashField -and $row.$hashField) {
            $hash = (Get-FileHash -Algorithm SHA256 -LiteralPath $localPath).Hash
            if ($hash -ne ([string]$row.$hashField).ToUpperInvariant()) {
                $verificationErrors.Add("sha256`t$member")
            }
        }
    }
}
if ($verificationErrors.Count -gt 0) {
    $verificationErrors | Set-Content -LiteralPath (Join-Path $stageRoot 'verification_errors.tsv') -Encoding utf8
    throw "Extraction verification failed for $($verificationErrors.Count) files. Staging was preserved."
}

New-Item -ItemType Directory -Path $codeRoot | Out-Null
Move-Item -LiteralPath (Join-Path $stageRoot 'production_code') -Destination (Join-Path $codeRoot 'production_code')
Move-Item -LiteralPath (Join-Path $stageRoot 'FINAL_NUMERICAL_FIGURES') -Destination (Join-Path $codeRoot 'FINAL_NUMERICAL_FIGURES')
Move-Item -LiteralPath (Join-Path $stageRoot '.archive_metadata_2026-10-01') -Destination (Join-Path $codeRoot 'archive_provenance')

$existingValidation = Join-Path $physicsRoot 'validation_code'
if (Test-Path -LiteralPath $existingValidation -PathType Container) {
    Move-Item -LiteralPath $existingValidation -Destination (Join-Path $codeRoot 'validation_code')
}
$existingUtility = Join-Path $physicsRoot 'scan_axis6_interlayer_cutoffs.cpp'
if (Test-Path -LiteralPath $existingUtility -PathType Leaf) {
    $utilityRoot = Join-Path $codeRoot 'utilities'
    New-Item -ItemType Directory -Path $utilityRoot | Out-Null
    Move-Item -LiteralPath $existingUtility -Destination (Join-Path $utilityRoot 'scan_axis6_interlayer_cutoffs.cpp')
}

$inventoryPath = Join-Path $codeRoot 'CODE_INVENTORY.tsv'
$inventoryRows = Get-ChildItem -LiteralPath $codeRoot -Recurse -File | ForEach-Object {
    $relative = $_.FullName.Substring($codeRoot.Length + 1).Replace('\', '/')
    $category = $relative.Split('/')[0]
    [pscustomobject]@{
        category = $category
        relative_path = $relative
        bytes = $_.Length
        sha256 = (Get-FileHash -Algorithm SHA256 -LiteralPath $_.FullName).Hash
    }
}
$inventoryRows | Sort-Object category,relative_path | Export-Csv -LiteralPath $inventoryPath -Delimiter "`t" -NoTypeInformation -Encoding utf8

$archiveHashRecord = @(
    "archive`t$archiveName",
    "sha256`t$actualArchiveHash",
    "selected_members`t$($selected.Count)",
    "verified_files`t$verifiedCount",
    "verified_bytes`t$verifiedBytes",
    "organized_utc`t$([DateTime]::UtcNow.ToString('o'))"
)
$archiveHashRecord | Set-Content -LiteralPath (Join-Path $codeRoot 'SOURCE_ARCHIVE_SHA256.txt') -Encoding utf8

New-Item -ItemType Directory -Path $archiveRoot -Force | Out-Null
$archiveDestination = Join-Path $archiveRoot $archiveName
if (Test-Path -LiteralPath $archiveDestination) { throw "Archive destination already exists: $archiveDestination" }
Move-Item -LiteralPath $sourceArchive -Destination $archiveDestination

foreach ($largeArchiveName in @(
    'AUTHORITATIVE_FROZEN_DATA_COLD_ARCHIVE_2026-10-01.tar.zst',
    'BUCKET_REPLAY_MATERIALS_2026-10-01.tar.zst'
)) {
    $largeSource = Join-Path $workspace $largeArchiveName
    $largeDestination = Join-Path $archiveRoot $largeArchiveName
    if (Test-Path -LiteralPath $largeSource -PathType Leaf) {
        if (Test-Path -LiteralPath $largeDestination) { throw "Archive destination already exists: $largeDestination" }
        Move-Item -LiteralPath $largeSource -Destination $largeDestination
    }
}

Remove-Item -LiteralPath $stageRoot -Recurse -Force

[pscustomobject]@{
    CodeRoot = $codeRoot
    SelectedArchiveMembers = $selected.Count
    VerifiedFiles = $verifiedCount
    VerifiedBytes = $verifiedBytes
    ArchiveDestination = $archiveDestination
} | Format-List
