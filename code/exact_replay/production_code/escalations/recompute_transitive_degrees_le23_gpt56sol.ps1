$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $MyInvocation.MyCommand.Path

function Read-One([string]$name, [string]$pattern) {
  $line = (Select-String -LiteralPath (Join-Path $root $name) -Pattern $pattern).Line
  if ($line -is [array]) { throw "expected one record: $name / $pattern" }
  if (-not $line) { throw "missing record: $name / $pattern" }
  return $line
}
function Field([string]$line, [string]$name) {
  $m = [regex]::Match($line, "(?:^|`t)$name`t([0-9]+)(?:`t|$)")
  if (-not $m.Success) { throw "missing field $name in $line" }
  return [long]$m.Groups[1].Value
}
function Sum-Field($lines, [string]$name) {
  [long]$s = 0
  foreach ($line in $lines) { $s += Field $line $name }
  return $s
}
function Make-Row([string]$block,[long]$db,[long]$win,[long]$par,[long]$alpha,
                  [long]$raw,[long]$inv,[long]$orb,[long]$rel,[long]$b3,
                  [long]$gen,[long]$corb) {
  [pscustomobject]@{Block=$block;Database=$db;Window=$win;Parity=$par;
    Alpha=$alpha;Raw=$raw;Inverse=$inv;Orbit8=$orb;Relator=$rel;B3=$b3;
    GenerateParity=$gen;CentralizerOrbits=$corb}
}

$rows = @()

$d15name = 'GAP_TRANSITIVE_DEGREE15_C8_EXHAUSTIVE_GPT56SOL.txt'
$d15 = Read-One $d15name '^TOTAL\t'
$d15raw = Get-Content -LiteralPath (Join-Path $root $d15name) -Raw
$d15Parity = [regex]::Matches($d15raw,'(?m)^ENTRY[^\r\n]*\tPARITY_MAPS\t[1-9][0-9]*(?:\t|$)').Count
$rows += Make-Row 'degrees1-15' (Field $d15 'DATABASE_ENTRIES') (Field $d15 'ELIGIBLE_ENTRIES') $d15Parity `
  (Field $d15 'ORDER8_CLASSES') (Field $d15 'SEED_PAIRS') (Field $d15 'INVERSE') `
  (Field $d15 'ORBIT8') (Field $d15 'RELATOR') (Field $d15 'B3') (Field $d15 'PARITY') `
  (Field $d15 'PARITY_CENTRALIZER_ORBITS')

$d16Probe = Read-One 'GAP_TRANSITIVE_DEGREE16_PROBE_GPT56SOL.txt' '^TOTAL\t'
$d16Names = @('1_1564','1565_1580','1581_1609','1610_1646','1647_1666',
  '1667_1686','1687_1706','1707_1770','1771_1806','1807_1954')
$d16Lines = foreach($s in $d16Names) { Read-One "GAP_TRANSITIVE_DEGREE16_C8_BETA_${s}_GPT56SOL.txt" '^TOTAL_SLICE\t' }
$rows += Make-Row 'degree16' (Field $d16Probe 'DATABASE') (Sum-Field $d16Lines 'ORDER_WINDOW_ENTRIES') `
  (Sum-Field $d16Lines 'PARITY_ENTRIES') (Sum-Field $d16Lines 'ORDER8_CLASSES') `
  (Sum-Field $d16Lines 'FULL_SEED_PAIRS') (Sum-Field $d16Lines 'INVERSE') `
  (Sum-Field $d16Lines 'ORBIT8') (Sum-Field $d16Lines 'RELATOR') (Sum-Field $d16Lines 'B3') `
  (Sum-Field $d16Lines 'PARITY') (Sum-Field $d16Lines 'CENTRALIZER_ORBITS')

$d171923 = Read-One 'GAP_TRANSITIVE_DEGREES17_19_23_C8_EXHAUSTIVE_GPT56SOL.txt' '^TOTAL\t'
$rows += Make-Row 'degrees17,19,23' (Field $d171923 'CATALOGUE_ENTRIES') `
  (Field $d171923 'ORDER_WINDOW_ENTRIES') (Field $d171923 'PARITY_ENTRIES') `
  (Field $d171923 'ORDER8_CLASSES') (Field $d171923 'FULL_SEED_PAIRS') `
  (Field $d171923 'INVERSE') (Field $d171923 'ORBIT8') (Field $d171923 'RELATOR') `
  (Field $d171923 'B3') (Field $d171923 'PARITY') (Field $d171923 'CENTRALIZER_ORBITS')

$d18head = Read-One 'GAP_TRANSITIVE_DEGREE18_C8_BETA_AGGREGATE_GPT56SOL.txt' '^CATALOGUE_ENTRIES\t'
$d18 = Read-One 'GAP_TRANSITIVE_DEGREE18_C8_BETA_AGGREGATE_GPT56SOL.txt' '^TOTAL\t'
$rows += Make-Row 'degree18' (Field $d18head 'CATALOGUE_ENTRIES') (Field $d18 'ORDER_WINDOW_ENTRIES') `
  (Field $d18 'PARITY_ENTRIES') (Field $d18 'ORDER8_CLASSES') (Field $d18 'FULL_SEED_PAIRS') `
  (Field $d18 'INVERSE') (Field $d18 'ORBIT8') (Field $d18 'RELATOR') (Field $d18 'B3') `
  (Field $d18 'GENERATE') (Field $d18 'CENTRALIZER_ORBITS')

$d20Probe = Read-One 'GAP_TRANSITIVE_DEGREE20_PROBE_GPT56SOL.txt' '^TOTAL\t'
$d20Names = @('1_482','483_533','534_604','605_1117')
$d20Lines = foreach($s in $d20Names) { Read-One "GAP_TRANSITIVE_DEGREE20_C8_BETA_${s}_GPT56SOL.txt" '^TOTAL_SLICE\t' }
$rows += Make-Row 'degree20' (Field $d20Probe 'DATABASE') (Sum-Field $d20Lines 'ORDER_WINDOW_ENTRIES') `
  (Sum-Field $d20Lines 'PARITY_ENTRIES') (Sum-Field $d20Lines 'ORDER8_CLASSES') `
  (Sum-Field $d20Lines 'FULL_SEED_PAIRS') (Sum-Field $d20Lines 'INVERSE') `
  (Sum-Field $d20Lines 'ORBIT8') (Sum-Field $d20Lines 'RELATOR') (Sum-Field $d20Lines 'B3') `
  (Sum-Field $d20Lines 'PARITY') (Sum-Field $d20Lines 'CENTRALIZER_ORBITS')

$d2122 = Select-String -LiteralPath (Join-Path $root 'GAP_TRANSITIVE_DEGREE21_22_C8_EXHAUSTIVE_GPT56SOL.txt') -Pattern '^DEGREE_TOTAL\t' | ForEach-Object Line
$rows += Make-Row 'degrees21-22' (Sum-Field $d2122 'DATABASE') (Sum-Field $d2122 'ORDER_WINDOW') `
  (Sum-Field $d2122 'PARITY_ENTRIES') (Sum-Field $d2122 'ORDER8_CLASSES') `
  (Sum-Field $d2122 'FULL_PAIRS') (Sum-Field $d2122 'INVERSE') (Sum-Field $d2122 'ORBIT8') `
  (Sum-Field $d2122 'RELATOR') (Sum-Field $d2122 'B3') (Sum-Field $d2122 'GENERATE') `
  (Sum-Field $d2122 'ORBITS')

$fields = @('Database','Window','Parity','Alpha','Raw','Inverse','Orbit8','Relator','B3','GenerateParity','CentralizerOrbits')
$rows | ForEach-Object { 'BLOCK' + "`t" + (($_.PSObject.Properties | ForEach-Object { "$($_.Name)`t$($_.Value)" }) -join "`t") }
'AGGREGATE'
foreach($f in $fields) { "$f`t$(($rows | Measure-Object -Property $f -Sum).Sum)" }

$based15 = Field (Read-One 'GAP_TRANSITIVE_DEGREE15_BASED_GPT56SOL.txt' '^CANDIDATES\t') 'CANDIDATES'
$based16 = Field (Read-One 'GAP_TRANSITIVE_DEGREE16_BASED_GPT56SOL.txt' '^CANDIDATES\t') 'CANDIDATES'
$based20line = Read-One 'GAP_TRANSITIVE_DEGREE20_BASED_SCAN_GPT56SOL.txt' '^candidates='
$based20 = [long]([regex]::Match($based20line,'^candidates=([0-9]+)$').Groups[1].Value)
"BASED_REJECTED`t$($based15+$based16+$based20)"
