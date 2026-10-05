param(
    [int]$KMin,
    [int]$KMax,
    [int]$ExpectedWindow,
    [int]$ExpectedParity,
    [string]$ShardTag,
    [string]$BaseDir = "."
)

$ErrorActionPreference="Stop"
if($KMin -lt 1 -or $KMax -lt $KMin -or $KMax -gt 25000){throw 'invalid range'}
if([string]::IsNullOrWhiteSpace($ShardTag)){throw 'missing shard tag'}
$outName="GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_${KMin}_${KMax}_CHECKPOINT_GPT56SOL.txt"
$stdoutName="GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_${ShardTag}_RUN_STDOUT_GPT56SOL.txt"
$stderrName="GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_${ShardTag}_RUN_STDERR_GPT56SOL.txt"
$verifyName="GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_${ShardTag}_VERIFY_GPT56SOL.txt"

function Assert-Eq($Actual,$Expected,[string]$Label){if($Actual -ne $Expected){throw "$Label mismatch: actual=$Actual expected=$Expected"}}
function Parse-Pairs([string]$Line,[string]$Prefix){
    $f=$Line -split "`t"; if($f[0] -ne $Prefix -or (($f.Count-1)%2)-ne 0){throw "malformed $Prefix line: $Line"}
    $h=@{}; for($i=1;$i -lt $f.Count;$i+=2){$h[$f[$i]]=$f[$i+1]}; return $h
}
function Parse-Entry([string]$Line,[int]$Index){
    $f=$Line -split "`t"
    if($f.Count -ne 20 -or $f[0] -ne 'ENTRY' -or $f[1] -notmatch '^24T([0-9]+)$'){throw "malformed ENTRY line $($Index+1): $Line"}
    $k=[int]$Matches[1]; $h=@{}; for($i=2;$i -lt $f.Count;$i+=2){$h[$f[$i]]=$f[$i+1]}
    foreach($name in @('ORDER','SOLVABLE_G','PARITY_MAPS','AUT_ORDER','AUT_MS','METHOD','CLASS_MS','ORDER8_CLASSES','RAW_PAIRS')){if(-not $h.ContainsKey($name)){throw "ENTRY missing $name at 24T$k"}}
    if($h.AUT_ORDER -notmatch '^[1-9][0-9]*$'){throw "invalid Aut order at 24T$k"}
    [pscustomobject]@{Index=$Index;K=$k;Order=[int64]$h.ORDER;Solvable=$h.SOLVABLE_G;Parity=[int64]$h.PARITY_MAPS;AutOrder=$h.AUT_ORDER;AutMs=[int64]$h.AUT_MS;Method=$h.METHOD;ClassMs=[int64]$h.CLASS_MS;Classes=[int64]$h.ORDER8_CLASSES;Raw=[int64]$h.RAW_PAIRS}
}
function Load-Map([string[]]$Names,[bool]$HasSolvable){
    $map=@{}
    foreach($name in $Names){foreach($line in [IO.File]::ReadAllLines((Join-Path $BaseDir $name))){
        if($line -notmatch '^ENTRY\t24T([0-9]+)\t'){continue};$k=[int]$Matches[1];$f=$line -split "`t";$h=@{};for($i=2;$i -lt $f.Count;$i+=2){$h[$f[$i]]=$f[$i+1]}
        if($map.ContainsKey($k)){throw "duplicate sealed key 24T$k"}
        $map[$k]=[pscustomobject]@{Order=[int64]$h.ORDER;Parity=[int64]$h.PARITY_MAPS;Solvable=if($HasSolvable){[int]$h.SOLVABLE}else{$null}}
    }}
    return $map
}

$solFiles=@('GAP_TRANSITIVE_DEGREE24_SOLVABILITY_1_7860_GPT56SOL.txt','GAP_TRANSITIVE_DEGREE24_SOLVABILITY_7861_10567_GPT56SOL.txt','GAP_TRANSITIVE_DEGREE24_SOLVABILITY_10568_13274_GPT56SOL.txt','GAP_TRANSITIVE_DEGREE24_SOLVABILITY_13275_25000_GPT56SOL.txt')
$parityFiles=@('GAP_TRANSITIVE_DEGREE24_PARITY_1_7860_GPT56SOL.txt','GAP_TRANSITIVE_DEGREE24_PARITY_7861_10567_GPT56SOL.txt','GAP_TRANSITIVE_DEGREE24_PARITY_10568_13274_GPT56SOL.txt','GAP_TRANSITIVE_DEGREE24_PARITY_13275_25000_GPT56SOL.txt')
$sol=Load-Map $solFiles $true;$win=Load-Map $parityFiles $false
$expectedKeys=@($sol.Keys|ForEach-Object{[int]$_}|Where-Object{$_ -ge $KMin -and $_ -le $KMax}|Sort-Object)
$windowKeys=@($win.Keys|ForEach-Object{[int]$_}|Where-Object{$_ -ge $KMin -and $_ -le $KMax}|Sort-Object)
Assert-Eq $expectedKeys.Count $ExpectedParity 'sealed parity key count';Assert-Eq $windowKeys.Count $ExpectedWindow 'sealed window key count'

$lines=[IO.File]::ReadAllLines((Join-Path $BaseDir $outName));if($lines.Count -lt 10){throw 'profile output too short'}
$header=@("CERTIFICATE_PROFILE`tPF-GRP-001-C8-TRANSITIVE-DEGREE24-AUT-CHECKPOINT","GAP_VERSION`t4.12.1","DATABASE`t25000","RANGE`t$KMin`t$KMax","GUARD_MS`t1320000","EXPECTED_ORDER_WINDOW`t$ExpectedWindow","EXPECTED_PARITY`t$ExpectedParity")
for($i=0;$i -lt $header.Count;$i++){Assert-Eq $lines[$i] $header[$i] "header line $($i+1)"}
Assert-Eq @($lines|Where-Object{$_ -match '^TOTAL\t'}).Count 1 'TOTAL count';Assert-Eq @($lines|Where-Object{$_ -eq 'DONE'}).Count 1 'DONE count';Assert-Eq $lines[-1] 'DONE' 'terminal DONE';Assert-Eq @($lines|Where-Object{$_ -match '^(TOTAL_PARTIAL|STOPPED_GUARD)'}).Count 0 'guard markers'

$entries=@();for($i=0;$i -lt $lines.Count;$i++){if($lines[$i] -match '^ENTRY\t'){$entries+=Parse-Entry $lines[$i] $i}}
Assert-Eq $entries.Count $ExpectedParity 'ENTRY count';Assert-Eq @($entries|Group-Object K|Where-Object{$_.Count-ne 1}).Count 0 'duplicate keys';Assert-Eq @(Compare-Object -ReferenceObject $expectedKeys -DifferenceObject @($entries.K)).Count 0 'ENTRY keyset'
[int64]$classes=0;[int64]$raw=0;[int64]$autMs=0;[int64]$classMs=0;$previous=$KMin-1
for($ei=0;$ei -lt $entries.Count;$ei++){
    $e=$entries[$ei];if($e.K -le $previous){throw "non-increasing key 24T$($e.K)"};$previous=$e.K;$s=$sol[$e.K]
    Assert-Eq $e.Order $s.Order "24T$($e.K) order";Assert-Eq $e.Parity $s.Parity "24T$($e.K) parity";Assert-Eq $e.Solvable $(if($s.Solvable-eq 1){'true'}else{'false'}) "24T$($e.K) solvable";Assert-Eq $e.Raw ($e.Order*$e.Classes) "24T$($e.K) raw"
    if($e.Parity-le 0 -or $e.AutMs-lt 0 -or $e.ClassMs-lt 0 -or $e.Method-notin @('pc','native')){throw "invalid field at 24T$($e.K)"}
    $classes+=$e.Classes;$raw+=$e.Raw;$autMs+=$e.AutMs;$classMs+=$e.ClassMs
    $cp=Parse-Pairs $lines[$e.Index+1] 'CHECKPOINT';Assert-Eq ([int]$cp.LAST_COMPLETE_K) $e.K "checkpoint key";Assert-Eq ([int]$cp.PROCESSED) ($ei+1) "checkpoint processed";Assert-Eq ([int64]$cp.ORDER8_CLASSES) $classes "checkpoint classes";Assert-Eq ([int64]$cp.RAW_PAIRS) $raw "checkpoint raw"
}

$scanLines=@($lines|Where-Object{$_ -match '^SCAN_CHECKPOINT\t'});$firstScan=[int]([math]::Ceiling($KMin/25.0)*25);$expectedScans=if($firstScan-le $KMax){[int]([math]::Floor(($KMax-$firstScan)/25)+1)}else{0};Assert-Eq $scanLines.Count $expectedScans 'scan checkpoint count'
for($j=0;$j -lt $scanLines.Count;$j++){
    $s=Parse-Pairs $scanLines[$j] 'SCAN_CHECKPOINT';$k=$firstScan+25*$j;Assert-Eq ([int]$s.LAST_COMPLETE_K) $k "scan key $k";Assert-Eq ([int]$s.ORDER_WINDOW) @($windowKeys|Where-Object{$_-le $k}).Count "scan window $k";Assert-Eq ([int]$s.PROCESSED) @($entries|Where-Object{$_.K-le $k}).Count "scan processed $k";Assert-Eq ([int64]$s.ORDER8_CLASSES) ([int64](($entries|Where-Object{$_.K-le $k}|Measure-Object Classes -Sum).Sum)) "scan classes $k";Assert-Eq ([int64]$s.RAW_PAIRS) ([int64](($entries|Where-Object{$_.K-le $k}|Measure-Object Raw -Sum).Sum)) "scan raw $k"
}

$total=@($lines|Where-Object{$_ -match '^TOTAL\t'})[0];$pattern="^TOTAL\tDEGREE\t24\tDATABASE\t25000\tRANGE\t$KMin\t$KMax\tLAST_COMPLETE_K\t$KMax\tORDER_WINDOW\t$ExpectedWindow\tPROCESSED\t$ExpectedParity\tORDER8_CLASSES\t([0-9]+)\tRAW_PAIRS\t([0-9]+)\tAUT_MS\t([0-9]+)\tCLASS_MS\t([0-9]+)\tMS\t([0-9]+)$";if($total-notmatch $pattern){throw "malformed TOTAL: $total"};Assert-Eq ([int64]$Matches[1]) $classes 'total classes';Assert-Eq ([int64]$Matches[2]) $raw 'total raw';Assert-Eq ([int64]$Matches[3]) $autMs 'total AutMs';Assert-Eq ([int64]$Matches[4]) $classMs 'total ClassMs';$totalMs=[int64]$Matches[5]
$stdout=[IO.File]::ReadAllText((Join-Path $BaseDir $stdoutName));$stderr=[IO.File]::ReadAllText((Join-Path $BaseDir $stderrName));if($stdout.Trim()-ne "WROTE /mnt/d/work/revise/production_code/escalations/$outName"){throw 'unexpected stdout'};if($stderr-notmatch 'Exit status: 0' -or $stderr-notmatch 'Maximum resident set size \(kbytes\): ([0-9]+)'){throw 'bad runtime telemetry'};$rss=[int64]$Matches[1];if($rss-ge 50331648){throw "RSS guard exceeded: $rss"}
$result=@("CERTIFICATE_VERIFY`tPF-GRP-001-C8-TRANSITIVE-DEGREE24-AUT-PROFILE-$ShardTag","RANGE`t$KMin`t$KMax","ORDER_WINDOW`t$ExpectedWindow","PARITY_KEYS`t$ExpectedParity","ENTRY_KEYS_EXACT`tPASS","RAW_IDENTITIES`t$ExpectedParity`tPASS","ENTRY_CHECKPOINT_PAIRS`t$ExpectedParity`tPASS","SCAN_CHECKPOINTS`t$expectedScans`tPASS","ORDER8_CLASSES`t$classes","RAW_PAIRS`t$raw","AUT_MS`t$autMs","CLASS_MS`t$classMs","TOTAL_MS`t$totalMs","MAX_RSS_KB`t$rss","HEADER_UNIQUE_TOTAL_DONE_NO_GUARD`tPASS","STDOUT_STDERR_TELEMETRY`tPASS","SCOPE`tExact Aut/order-8 profile only; no seed predicates.","VERIFY`tPASS","DONE")
[IO.File]::WriteAllLines((Join-Path $BaseDir $verifyName),$result,[Text.UTF8Encoding]::new($false));Write-Output "PASS tag=$ShardTag range=$KMin-$KMax entries=$ExpectedParity window=$ExpectedWindow classes=$classes raw=$raw autMs=$autMs classMs=$classMs totalMs=$totalMs rssKb=$rss scans=$expectedScans"
