param(
    [string]$Version = "2026-09-03"
)

$ErrorActionPreference = "Stop"

$projectRoot = [IO.Path]::GetFullPath((Join-Path $PSScriptRoot ".."))
$reproRoot = [IO.Path]::GetFullPath($PSScriptRoot)
$outputRoot = [IO.Path]::GetFullPath((Join-Path $projectRoot "products\release_archives"))
New-Item -ItemType Directory -Path $outputRoot -Force | Out-Null

$archiveName = "hyperbolic_moire_source_$Version.zip"
$archivePath = [IO.Path]::GetFullPath((Join-Path $outputRoot $archiveName))
$inventoryPath = [IO.Path]::GetFullPath((Join-Path $outputRoot "hyperbolic_moire_source_${Version}_inventory.json"))
$validationPath = [IO.Path]::GetFullPath((Join-Path $outputRoot "hyperbolic_moire_source_${Version}_validation.json"))
$checksumPath = [IO.Path]::GetFullPath((Join-Path $outputRoot "hyperbolic_moire_source_${Version}.sha256"))

foreach ($target in @($archivePath, $inventoryPath, $validationPath, $checksumPath)) {
    if (-not $target.StartsWith($outputRoot, [StringComparison]::OrdinalIgnoreCase)) {
        throw "Unsafe archive target: $target"
    }
    if (Test-Path -LiteralPath $target) {
        Remove-Item -LiteralPath $target -Force
    }
}

$allowedExtensions = @(".py", ".ps1", ".json", ".yml", ".yaml", ".txt", ".md", ".csv")
$dataMetadataNames = @(
    "dataset_schema.json",
    "figure_data_manifest.json",
    "RAW_DATA_POLICY.md",
    "README.md",
    "raw_data_policy_verification.json"
)

$files = Get-ChildItem -LiteralPath $reproRoot -Recurse -File | Where-Object {
    $full = $_.FullName
    if (-not $full.StartsWith($reproRoot, [StringComparison]::OrdinalIgnoreCase)) {
        return $false
    }
    $relativeRepro = $full.Substring($reproRoot.Length).TrimStart([char[]]@(92, 47))
    if ($relativeRepro -match '(^|[\\/])__pycache__([\\/]|$)' -or $_.Extension -eq ".pyc") {
        return $false
    }
    if ($relativeRepro -match '^data[\\/]') {
        return ($_.Extension -eq ".py" -or $dataMetadataNames -contains $_.Name)
    }
    return $allowedExtensions -contains $_.Extension
}

$extraFiles = @(
    (Join-Path $projectRoot "theory_tasks\generate_P1-09-Q5_w0_figure.py")
)
foreach ($extra in $extraFiles) {
    if (-not (Test-Path -LiteralPath $extra -PathType Leaf)) {
        throw "Missing required source file: $extra"
    }
    $files += Get-Item -LiteralPath $extra
}

$files = $files | Sort-Object FullName -Unique
if ($files.Count -eq 0) {
    throw "Source archive selection is empty"
}

Add-Type -AssemblyName System.IO.Compression
$fixedTimestamp = [DateTimeOffset]::Parse("2026-09-03T00:00:00+08:00")
$entries = @()
$stream = [IO.File]::Open($archivePath, [IO.FileMode]::CreateNew, [IO.FileAccess]::ReadWrite, [IO.FileShare]::None)
$archive = [IO.Compression.ZipArchive]::new($stream, [IO.Compression.ZipArchiveMode]::Create, $false)
try {
    foreach ($file in $files) {
        if (-not $file.FullName.StartsWith($projectRoot, [StringComparison]::OrdinalIgnoreCase)) {
            throw "Source file outside project root: $($file.FullName)"
        }
        $entryName = $file.FullName.Substring($projectRoot.Length).TrimStart([char[]]@(92, 47)).Replace("\", "/")
        $entry = $archive.CreateEntry($entryName, [IO.Compression.CompressionLevel]::Optimal)
        $entry.LastWriteTime = $fixedTimestamp
        $input = [IO.File]::OpenRead($file.FullName)
        $output = $entry.Open()
        try {
            $input.CopyTo($output)
        }
        finally {
            $output.Dispose()
            $input.Dispose()
        }
        $digest = (Get-FileHash -Algorithm SHA256 -LiteralPath $file.FullName).Hash.ToLowerInvariant()
        $entries += [ordered]@{
            path = $entryName
            bytes = $file.Length
            sha256 = $digest
        }
    }
}
finally {
    $archive.Dispose()
    $stream.Dispose()
}

$archiveDigest = (Get-FileHash -Algorithm SHA256 -LiteralPath $archivePath).Hash.ToLowerInvariant()
$inventory = [ordered]@{
    schema_version = 1
    package = "hyperbolic_moire_source"
    version = $Version
    scope = "source code, registered configurations, environment, provenance metadata, and current figure registry; numerical datasets and rendered outputs excluded"
    archive = $archiveName
    archive_bytes = (Get-Item -LiteralPath $archivePath).Length
    archive_sha256 = $archiveDigest
    entry_count = $entries.Count
    entries = $entries
}
$inventory | ConvertTo-Json -Depth 6 | Set-Content -LiteralPath $inventoryPath -Encoding UTF8
"$archiveDigest  $archiveName" | Set-Content -LiteralPath $checksumPath -Encoding ascii

$expected = @{}
foreach ($item in $entries) {
    $expected[$item.path] = $item.sha256
}
$validated = 0
$zipStream = [IO.File]::OpenRead($archivePath)
$zip = [IO.Compression.ZipArchive]::new($zipStream, [IO.Compression.ZipArchiveMode]::Read, $false)
try {
    if ($zip.Entries.Count -ne $entries.Count) {
        throw "Archive entry count mismatch"
    }
    foreach ($entry in $zip.Entries) {
        if (-not $expected.ContainsKey($entry.FullName)) {
            throw "Unexpected archive entry: $($entry.FullName)"
        }
        $entryStream = $entry.Open()
        $hasher = [Security.Cryptography.SHA256]::Create()
        try {
            $actual = ([BitConverter]::ToString($hasher.ComputeHash($entryStream))).Replace("-", "").ToLowerInvariant()
        }
        finally {
            $hasher.Dispose()
            $entryStream.Dispose()
        }
        if ($actual -ne $expected[$entry.FullName]) {
            throw "Archive member checksum mismatch: $($entry.FullName)"
        }
        $validated += 1
    }
}
finally {
    $zip.Dispose()
    $zipStream.Dispose()
}

$validation = [ordered]@{
    package = $archiveName
    archive_sha256 = $archiveDigest
    expected_entries = $entries.Count
    validated_entries = $validated
    unexpected_entries = 0
    checksum_failures = 0
    result = "PASS"
    public_persistent_identifier = $null
}
$validation | ConvertTo-Json -Depth 4 | Set-Content -LiteralPath $validationPath -Encoding UTF8

Write-Output ($validation | ConvertTo-Json -Compress)

