$ErrorActionPreference = 'Stop'

$figureRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$sourceDir = Join-Path $figureRoot 'source'
$buildDir = Join-Path $figureRoot 'build'
$outputDir = Join-Path $figureRoot 'outputs'

New-Item -ItemType Directory -Path $buildDir -Force | Out-Null
New-Item -ItemType Directory -Path $outputDir -Force | Out-Null

$figures = @(
    'FIG_R7_01_THEOREM_BRIDGE',
    'FIG_R7_02_MAGIC_CERTIFICATE',
    'FIG_R7_03_HYPERBOLIC_SCALE_WINDOW',
    'FIG_R7_04_LOCALITY_ENVELOPES'
)

Push-Location $sourceDir
try {
    foreach ($figure in $figures) {
        & pdflatex --disable-installer -interaction=nonstopmode -halt-on-error -output-directory $buildDir "$figure.tex"
        if ($LASTEXITCODE -ne 0) {
            throw "LaTeX build failed for $figure"
        }

        $builtPdf = Join-Path $buildDir "$figure.pdf"
        $finalPdf = Join-Path $outputDir "$figure.pdf"
        Copy-Item -LiteralPath $builtPdf -Destination $finalPdf -Force

        & pdftocairo -svg $finalPdf (Join-Path $outputDir "$figure.svg")
        if ($LASTEXITCODE -ne 0) {
            throw "SVG conversion failed for $figure"
        }

        & pdftocairo -png -singlefile -r 600 $finalPdf (Join-Path $outputDir $figure)
        if ($LASTEXITCODE -ne 0) {
            throw "PNG conversion failed for $figure"
        }
    }
}
finally {
    Pop-Location
}

Write-Output "R7_FIGURE_BUILD = PASS"
Write-Output "R7_FIGURE_COUNT = $($figures.Count)"
