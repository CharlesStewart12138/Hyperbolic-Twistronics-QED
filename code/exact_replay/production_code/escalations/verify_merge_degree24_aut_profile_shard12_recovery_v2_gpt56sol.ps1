param([string]$BaseDir = ".")
$ErrorActionPreference = "Stop"

function Assert-Eq($Actual,$Expected,[string]$Label) {
    if([string]$Actual -ne [string]$Expected){ throw "$Label mismatch: actual=$Actual expected=$Expected" }
}
function Parse-Pairs([string]$Line,[string]$Prefix,[int]$Start=1) {
    $f=$Line -split "`t"
    if($f[0] -ne $Prefix -or (($f.Count-$Start)%2) -ne 0){ throw "malformed $Prefix line: $Line" }
    $h=@{}
    for($i=$Start;$i -lt $f.Count;$i+=2){ $h[$f[$i]]=$f[$i+1] }
    return $h
}
function Parse-Entry([string]$Line,[string]$Representation) {
    $f=$Line -split "`t"
    if($f.Count -lt 20 -or $f[0] -ne 'ENTRY' -or $f[1] -notmatch '^24T([0-9]+)$' -or (($f.Count-2)%2) -ne 0){ throw "malformed ENTRY: $Line" }
    $k=[int]$Matches[1];$h=@{}
    for($i=2;$i -lt $f.Count;$i+=2){ $h[$f[$i]]=$f[$i+1] }
    foreach($n in @('ORDER','AUT_ORDER','AUT_MS','METHOD','CLASS_MS','ORDER8_CLASSES','RAW_PAIRS')){ if(-not $h.ContainsKey($n)){throw "ENTRY 24T$k missing $n"} }
    if($h.ContainsKey('SOLVABLE_G')){$solvable=$h.SOLVABLE_G}
    elseif($Representation -eq 'pc_single'){$solvable='true'}
    else{throw "ENTRY 24T$k missing SOLVABLE_G"}
    if($Representation -eq 'original'){
        if(-not $h.ContainsKey('PARITY_MAPS')){throw "original ENTRY 24T$k missing PARITY_MAPS"}
        $parity=[int64]$h.PARITY_MAPS;$pcOrder=[int64]$h.ORDER;$iso=[int64]0
    } else {
        foreach($n in @('PARITY_MAPS_G','PC_ORDER','PARITY_MAPS_P','ISO_MS')){if(-not $h.ContainsKey($n)){throw "pc ENTRY 24T$k missing $n"}}
        $parity=[int64]$h.PARITY_MAPS_G;$pcOrder=[int64]$h.PC_ORDER;$iso=[int64]$h.ISO_MS
        Assert-Eq $h.PARITY_MAPS_P $h.PARITY_MAPS_G "24T$k transported parity"
        Assert-Eq $h.PC_ORDER $h.ORDER "24T$k transported order"
    }
    return [pscustomobject]@{K=$k;Order=[int64]$h.ORDER;Solvable=$solvable;Parity=$parity;PCOrder=$pcOrder;AutOrder=$h.AUT_ORDER;IsoMs=$iso;AutMs=[int64]$h.AUT_MS;Method=$h.METHOD;ClassMs=[int64]$h.CLASS_MS;Classes=[int64]$h.ORDER8_CLASSES;Raw=[int64]$h.RAW_PAIRS;Representation=$Representation;Line=$Line}
}
function Load-Map([string]$Name,[bool]$HasSolvable) {
    $m=@{}
    foreach($line in [IO.File]::ReadAllLines((Join-Path $BaseDir $Name))){
        if($line -notmatch '^ENTRY\t24T([0-9]+)\t'){continue}
        $k=[int]$Matches[1];$f=$line -split "`t";$h=@{}
        for($i=2;$i -lt $f.Count;$i+=2){$h[$f[$i]]=$f[$i+1]}
        $m[$k]=[pscustomobject]@{Order=[int64]$h.ORDER;Parity=[int64]$h.PARITY_MAPS;Solvable=if($HasSolvable){[int]$h.SOLVABLE}else{$null}}
    }
    return $m
}
function Expected-Keys($Map,[int]$Lo,[int]$Hi) {
    return @($Map.Keys | ForEach-Object {[int]$_} | Where-Object {$_ -ge $Lo -and $_ -le $Hi} | Sort-Object)
}
function Assert-Keyset($Entries,[int[]]$Expected,[string]$Label) {
    Assert-Eq $Entries.Count $Expected.Count "$Label count"
    Assert-Eq @($Entries | Group-Object K | Where-Object {$_.Count -ne 1}).Count 0 "$Label duplicate keys"
    Assert-Eq @(Compare-Object -ReferenceObject $Expected -DifferenceObject @($Entries.K)).Count 0 "$Label keyset"
    $prev=-1;foreach($e in $Entries){if($e.K -le $prev){throw "$Label non-increasing at 24T$($e.K)"};$prev=$e.K}
}
function Check-Entry($e,$Sol,[string]$Label) {
    $s=$Sol[$e.K];if($null -eq $s){throw "$Label missing sealed key 24T$($e.K)"}
    Assert-Eq $e.Order $s.Order "$Label 24T$($e.K) order"
    Assert-Eq $e.Parity $s.Parity "$Label 24T$($e.K) parity"
    Assert-Eq $e.Solvable $(if($s.Solvable -eq 1){'true'}else{'false'}) "$Label 24T$($e.K) solvable"
    Assert-Eq $e.Raw ($e.Order*$e.Classes) "$Label 24T$($e.K) raw"
    if($e.Parity -le 0 -or $e.AutMs -lt 0 -or $e.ClassMs -lt 0 -or $e.IsoMs -lt 0 -or $e.AutOrder -notmatch '^[1-9][0-9]*$' -or $e.Method -notin @('pc','native')){throw "$Label invalid field at 24T$($e.K)"}
}
function Check-Telemetry([string]$StdoutName,[string]$StderrName,[string]$ExpectedWrote,[int]$ExpectedExit) {
    $stdout=[IO.File]::ReadAllText((Join-Path $BaseDir $StdoutName));$stderr=[IO.File]::ReadAllText((Join-Path $BaseDir $StderrName))
    if($ExpectedWrote -eq ''){Assert-Eq $stdout.Length 0 "$StdoutName empty stdout"}else{Assert-Eq $stdout.Trim() $ExpectedWrote "$StdoutName WROTE"}
    if($stderr -notmatch 'Elapsed \(wall clock\) time \(h:mm:ss or m:ss\): ([^\r\n]+)'){throw "$StderrName missing wall"};$wall=$Matches[1].Trim()
    if($stderr -notmatch 'Maximum resident set size \(kbytes\): ([0-9]+)'){throw "$StderrName missing RSS"};$rss=[int64]$Matches[1]
    if($stderr -notmatch "Exit status: $ExpectedExit"){throw "$StderrName wrong exit"}
    if($rss -ge 50331648){throw "$StderrName RSS guard exceeded"}
    return [pscustomobject]@{Wall=$wall;Rss=$rss;Exit=$ExpectedExit}
}

$sol=Load-Map 'GAP_TRANSITIVE_DEGREE24_SOLVABILITY_10568_13274_GPT56SOL.txt' $true
$win=Load-Map 'GAP_TRANSITIVE_DEGREE24_PARITY_10568_13274_GPT56SOL.txt' $false
$fullKeys=Expected-Keys $sol 11341 11845;$fullWindow=Expected-Keys $win 11341 11845
Assert-Eq $fullKeys.Count 501 'sealed full parity';Assert-Eq $fullWindow.Count 505 'sealed full window'

# Segment A: externally interrupted original-representation prefix.
$prefixName='GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_11341_11845_CHECKPOINT_EXTERNAL_GUARD_PARTIAL1_GPT56SOL.txt'
$a=[IO.File]::ReadAllLines((Join-Path $BaseDir $prefixName))
$aHeader=@("CERTIFICATE_PROFILE`tPF-GRP-001-C8-TRANSITIVE-DEGREE24-AUT-CHECKPOINT","GAP_VERSION`t4.12.1","DATABASE`t25000","RANGE`t11341`t11845","GUARD_MS`t1320000","EXPECTED_ORDER_WINDOW`t505","EXPECTED_PARITY`t501","SCOPE`tExact Aut(G), exact-order-8 conjugacy classes, and raw=Size(G)*class-count for parity-capable order-window targets only; no seeds.","RECOVERY`tENTRY and CHECKPOINT certify each completed eligible key; SCAN_CHECKPOINT certifies every 25th completed catalogue key.")
for($i=0;$i -lt $aHeader.Count;$i++){Assert-Eq $a[$i] $aHeader[$i] "prefix header $($i+1)"}
Assert-Eq @($a|Where-Object{$_ -match '^(TOTAL|TOTAL_PARTIAL)\t'}).Count 0 'prefix totals';Assert-Eq @($a|Where-Object{$_ -in @('DONE','STOPPED_GUARD')}).Count 0 'prefix terminals'
$aEntries=@();for($i=0;$i -lt $a.Count;$i++){if($a[$i] -match '^ENTRY\t'){$aEntries+=Parse-Entry $a[$i] 'original'}}
Assert-Keyset $aEntries (Expected-Keys $sol 11341 11362) 'prefix';[int64]$aClasses=0;[int64]$aRaw=0;[int64]$aAut=0;[int64]$aClass=0
for($i=0;$i -lt $aEntries.Count;$i++){$e=$aEntries[$i];Check-Entry $e $sol 'prefix';$aClasses+=$e.Classes;$aRaw+=$e.Raw;$aAut+=$e.AutMs;$aClass+=$e.ClassMs;$idx=[Array]::IndexOf($a,$e.Line);$cp=Parse-Pairs $a[$idx+1] 'CHECKPOINT';Assert-Eq $cp.LAST_COMPLETE_K $e.K "prefix cp key";Assert-Eq $cp.PROCESSED ($i+1) "prefix cp processed";Assert-Eq $cp.ORDER8_CLASSES $aClasses "prefix cp classes";Assert-Eq $cp.RAW_PAIRS $aRaw "prefix cp raw"}
Assert-Eq $aEntries.Count 22 'prefix entries';Assert-Eq $aClasses 3644 'prefix classes';Assert-Eq $aRaw 44777472 'prefix raw';Assert-Eq $aAut 5928 'prefix AutMs';Assert-Eq $aClass 18807 'prefix ClassMs'
$aScans=@($a|Where-Object{$_ -match '^SCAN_CHECKPOINT\t'});Assert-Eq $aScans.Count 1 'prefix scans';$aScan=Parse-Pairs $aScans[0] 'SCAN_CHECKPOINT';Assert-Eq $aScan.LAST_COMPLETE_K 11350 'prefix scan key';Assert-Eq $aScan.ORDER_WINDOW 10 'prefix scan window';Assert-Eq $aScan.PROCESSED 10 'prefix scan processed'
$aLast=Parse-Pairs $a[-1] 'CHECKPOINT';Assert-Eq $aLast.LAST_COMPLETE_K 11362 'prefix last key';$aMs=[int64]$aLast.MS
$partialTelemetry=Check-Telemetry 'GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_SHARD12_PARTIAL1_RUN_STDOUT_GPT56SOL.txt' 'GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_SHARD12_PARTIAL1_RUN_STDERR_GPT56SOL.txt' '' 124

# Segments B/C: exact isolated pc-domain keys.
function Parse-SinglePc([int]$Key,[string]$OutputName,[string]$StdoutName,[string]$StderrName) {
    $l=[IO.File]::ReadAllLines((Join-Path $BaseDir $OutputName));Assert-Eq $l.Count 11 "24T$Key line count"
    Assert-Eq $l[0] "CERTIFICATE_PROFILE`tPF-GRP-001-C8-TRANSITIVE-PC-DOMAIN-AUT-PROFILE-V3" "24T$Key header"
    Assert-Eq $l[1] "DEGREE`t24" "24T$Key degree";Assert-Eq $l[2] "KEY`t$Key" "24T$Key key";Assert-Eq $l[3] "GUARD_MS`t1320000" "24T$Key guard"
    Assert-Eq @($l|Where-Object{$_ -match '^STAGE\t'}).Count 3 "24T$Key stages";Assert-Eq @($l|Where-Object{$_ -match '^TOTAL\t'}).Count 1 "24T$Key total";Assert-Eq $l[-1] 'DONE' "24T$Key DONE";Assert-Eq @($l|Where-Object{$_ -match '^(TOTAL_PARTIAL|STOPPED_GUARD)'}).Count 0 "24T$Key guard markers"
    $entry=Parse-Entry (@($l|Where-Object{$_ -match '^ENTRY\t'})[0]) 'pc_single';Check-Entry $entry $sol "24T$Key";Assert-Eq $entry.K $Key "24T$Key entry key"
    $tot=Parse-Pairs (@($l|Where-Object{$_ -match '^TOTAL\t'})[0]) 'TOTAL';Assert-Eq $tot.DEGREE 24 "24T$Key total degree";Assert-Eq $tot.KEY $Key "24T$Key total key";Assert-Eq $tot.PROCESSED 1 "24T$Key processed";Assert-Eq $tot.ORDER8_CLASSES $entry.Classes "24T$Key total classes";Assert-Eq $tot.RAW_PAIRS $entry.Raw "24T$Key total raw";Assert-Eq $tot.ISO_MS $entry.IsoMs "24T$Key total iso";Assert-Eq $tot.AUT_MS $entry.AutMs "24T$Key total aut";Assert-Eq $tot.CLASS_MS $entry.ClassMs "24T$Key total class"
    $tele=Check-Telemetry $StdoutName $StderrName "WROTE /mnt/d/work/revise/production_code/escalations/$OutputName" 0
    return @{Entry=$entry;Ms=[int64]$tot.MS;Telemetry=$tele}
}
$b=Parse-SinglePc 11363 'GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_24T11363_PC_DOMAIN_V3_GPT56SOL.txt' 'GAP_TRANSITIVE_DEGREE24_24T11363_PC_DOMAIN_V3_RUN_STDOUT_GPT56SOL.txt' 'GAP_TRANSITIVE_DEGREE24_24T11363_PC_DOMAIN_V3_RUN_STDERR_GPT56SOL.txt'
$c=Parse-SinglePc 11364 'GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_24T11364_PC_DOMAIN_V3_GPT56SOL.txt' 'GAP_TRANSITIVE_DEGREE24_24T11364_PC_DOMAIN_V3_RUN_STDOUT_GPT56SOL.txt' 'GAP_TRANSITIVE_DEGREE24_24T11364_PC_DOMAIN_V3_RUN_STDERR_GPT56SOL.txt'

# Segment D: checkpointed pc-domain suffix.
$suffixName='GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_11365_11845_PC_DOMAIN_RECOVERY_CHECKPOINT_GPT56SOL.txt';$dlines=[IO.File]::ReadAllLines((Join-Path $BaseDir $suffixName))
$dHeader=@("CERTIFICATE_PROFILE`tPF-GRP-001-C8-TRANSITIVE-DEGREE24-AUT-PC-DOMAIN-RECOVERY-CHECKPOINT","GAP_VERSION`t4.12.1","DATABASE`t25000","RANGE`t11365`t11845","GUARD_MS`t1320000","EXPECTED_ORDER_WINDOW`t481","EXPECTED_PARITY`t477","SCOPE`tExact pc-isomorphic Aut(G), exact-order-8 conjugacy classes, and raw=Size(G)*class-count for solvable parity-capable order-window targets only; no seeds.","RECOVERY`tENTRY and CHECKPOINT certify each completed eligible key; SCAN_CHECKPOINT certifies every 25th completed catalogue key.")
for($i=0;$i -lt $dHeader.Count;$i++){Assert-Eq $dlines[$i] $dHeader[$i] "suffix header $($i+1)"}
Assert-Eq @($dlines|Where-Object{$_ -match '^TOTAL\t'}).Count 1 'suffix total count';Assert-Eq $dlines[-1] 'DONE' 'suffix DONE';Assert-Eq @($dlines|Where-Object{$_ -match '^(TOTAL_PARTIAL|STOPPED_GUARD)'}).Count 0 'suffix guard markers'
$dEntries=@();for($i=0;$i -lt $dlines.Count;$i++){if($dlines[$i] -match '^ENTRY\t'){$dEntries+=Parse-Entry $dlines[$i] 'pc_transport'}}
Assert-Keyset $dEntries (Expected-Keys $sol 11365 11845) 'suffix';[int64]$dClasses=0;[int64]$dRaw=0;[int64]$dIso=0;[int64]$dAut=0;[int64]$dClass=0
for($i=0;$i -lt $dEntries.Count;$i++){$e=$dEntries[$i];Check-Entry $e $sol 'suffix';$dClasses+=$e.Classes;$dRaw+=$e.Raw;$dIso+=$e.IsoMs;$dAut+=$e.AutMs;$dClass+=$e.ClassMs;$idx=[Array]::IndexOf($dlines,$e.Line);$cp=Parse-Pairs $dlines[$idx+1] 'CHECKPOINT';Assert-Eq $cp.LAST_COMPLETE_K $e.K 'suffix cp key';Assert-Eq $cp.PROCESSED ($i+1) 'suffix cp processed';Assert-Eq $cp.ISO_MS $dIso 'suffix cp iso';Assert-Eq $cp.ORDER8_CLASSES $dClasses 'suffix cp classes';Assert-Eq $cp.RAW_PAIRS $dRaw 'suffix cp raw'}
$dScans=@($dlines|Where-Object{$_ -match '^SCAN_CHECKPOINT\t'});Assert-Eq $dScans.Count 19 'suffix scans'
for($j=0;$j -lt 19;$j++){$s=Parse-Pairs $dScans[$j] 'SCAN_CHECKPOINT';$k=11375+25*$j;Assert-Eq $s.LAST_COMPLETE_K $k "suffix scan key $k";Assert-Eq $s.ORDER_WINDOW (Expected-Keys $win 11365 $k).Count "suffix scan window $k";Assert-Eq $s.PROCESSED @($dEntries|Where-Object{$_.K-le$k}).Count "suffix scan processed $k";Assert-Eq $s.ORDER8_CLASSES ([int64](($dEntries|Where-Object{$_.K-le$k}|Measure-Object Classes -Sum).Sum)) "suffix scan classes $k";Assert-Eq $s.RAW_PAIRS ([int64](($dEntries|Where-Object{$_.K-le$k}|Measure-Object Raw -Sum).Sum)) "suffix scan raw $k"}
$dt=@($dlines|Where-Object{$_ -match '^TOTAL\t'})[0];$dp='^TOTAL\tDEGREE\t24\tDATABASE\t25000\tRANGE\t11365\t11845\tLAST_COMPLETE_K\t11845\tORDER_WINDOW\t481\tPROCESSED\t477\tORDER8_CLASSES\t([0-9]+)\tRAW_PAIRS\t([0-9]+)\tISO_MS\t([0-9]+)\tAUT_MS\t([0-9]+)\tCLASS_MS\t([0-9]+)\tMS\t([0-9]+)$';if($dt-notmatch$dp){throw "malformed suffix TOTAL: $dt"};Assert-Eq ([int64]$Matches[1]) $dClasses 'suffix total classes';Assert-Eq ([int64]$Matches[2]) $dRaw 'suffix total raw';Assert-Eq ([int64]$Matches[3]) $dIso 'suffix total iso';Assert-Eq ([int64]$Matches[4]) $dAut 'suffix total aut';Assert-Eq ([int64]$Matches[5]) $dClass 'suffix total class';$dMs=[int64]$Matches[6]
$dTele=Check-Telemetry 'GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_SHARD12_CONT3_RUN_STDOUT_GPT56SOL.txt' 'GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_SHARD12_CONT3_RUN_STDERR_GPT56SOL.txt' "WROTE /mnt/d/work/revise/production_code/escalations/$suffixName" 0

# Exact disjoint union and normalized merged profile.
$all=@($aEntries)+@($b.Entry)+@($c.Entry)+@($dEntries);$all=@($all|Sort-Object K)
Assert-Keyset $all $fullKeys 'full merge';Assert-Eq $all[21].K 11362 'prefix boundary';Assert-Eq $all[22].K 11363 'single B boundary';Assert-Eq $all[23].K 11364 'single C boundary';Assert-Eq $all[24].K 11365 'suffix boundary'
[int64]$classes=($all|Measure-Object Classes -Sum).Sum;[int64]$raw=($all|Measure-Object Raw -Sum).Sum;[int64]$iso=($all|Measure-Object IsoMs -Sum).Sum;[int64]$aut=($all|Measure-Object AutMs -Sum).Sum;[int64]$class=($all|Measure-Object ClassMs -Sum).Sum
[int64]$segmentMs=$aMs+$b.Ms+$c.Ms+$dMs
Assert-Eq $classes 91439 'full classes';Assert-Eq $raw 1123602432 'full raw';Assert-Eq $iso 609 'full iso';Assert-Eq $aut 190194 'full aut';Assert-Eq $class 360455 'full class';Assert-Eq $segmentMs 570397 'full segment ms'

$mergedName='GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_11341_11845_MERGED_RECOVERY_GPT56SOL.txt';$m=[Collections.Generic.List[string]]::new()
$m.Add("CERTIFICATE_PROFILE`tPF-GRP-001-C8-TRANSITIVE-DEGREE24-AUT-SHARD12-MERGED-RECOVERY")
$m.Add("GAP_VERSION`t4.12.1");$m.Add("DATABASE`t25000");$m.Add("RANGE`t11341`t11845");$m.Add("ORDER_WINDOW`t505");$m.Add("PARITY_KEYS`t501")
$m.Add("SEGMENTS`t11341..11362:original-prefix`t11363:pc-transport`t11364:pc-transport`t11365..11845:pc-transport")
$m.Add("SCOPE`tExact Aut/order-8 profile invariants only; no seed predicates. Abandoned in-memory work is excluded.")
foreach($e in $all){$m.Add("ENTRY`t24T$($e.K)`tORDER`t$($e.Order)`tSOLVABLE_G`t$($e.Solvable)`tPARITY_MAPS`t$($e.Parity)`tREPRESENTATION`t$($e.Representation)`tPC_ORDER`t$($e.PCOrder)`tAUT_ORDER`t$($e.AutOrder)`tISO_MS`t$($e.IsoMs)`tAUT_MS`t$($e.AutMs)`tMETHOD`t$($e.Method)`tCLASS_MS`t$($e.ClassMs)`tORDER8_CLASSES`t$($e.Classes)`tRAW_PAIRS`t$($e.Raw)")}
$m.Add("TOTAL`tDEGREE`t24`tDATABASE`t25000`tRANGE`t11341`t11845`tORDER_WINDOW`t505`tPROCESSED`t501`tORDER8_CLASSES`t$classes`tRAW_PAIRS`t$raw`tISO_MS`t$iso`tAUT_MS`t$aut`tCLASS_MS`t$class`tSEGMENT_GAP_MS`t$segmentMs")
$m.Add('DONE');[IO.File]::WriteAllLines((Join-Path $BaseDir $mergedName),$m,[Text.UTF8Encoding]::new($false))

$maxRss=(@($partialTelemetry.Rss,$b.Telemetry.Rss,$c.Telemetry.Rss,$dTele.Rss)|Measure-Object -Maximum).Maximum
$verifyName='GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_SHARD12_VERIFY_GPT56SOL.txt';$v=@("CERTIFICATE_VERIFY`tPF-GRP-001-C8-TRANSITIVE-DEGREE24-AUT-PROFILE-SHARD12-RECOVERY","RANGE`t11341`t11845","SEGMENT_KEYSETS_DISJOINT_CONTIGUOUS`tPASS","ORDER_WINDOW`t505","PARITY_KEYS`t501","ENTRY_KEYS_EXACT`tPASS","RAW_IDENTITIES`t501`tPASS","ENTRY_CHECKPOINT_PAIRS`t499`tPASS","SINGLE_KEY_TOTALS`t2`tPASS","SCAN_CHECKPOINTS`t20`tPASS","PC_ORDER_PARITY_TRANSPORT`t479`tPASS","ORDER8_CLASSES`t$classes","RAW_PAIRS`t$raw","ISO_MS`t$iso","AUT_MS`t$aut","CLASS_MS`t$class","SEGMENT_GAP_MS`t$segmentMs","EXTERNAL_GUARD_PREFIX_WALL`t$($partialTelemetry.Wall)","PC_11363_WALL`t$($b.Telemetry.Wall)","PC_11364_WALL`t$($c.Telemetry.Wall)","PC_SUFFIX_WALL`t$($dTele.Wall)","MAX_RSS_KB`t$maxRss","ABANDONED_IN_MEMORY_WORK_EXCLUDED`tPASS","HEADER_UNIQUE_TOTAL_DONE_NO_GUARD_COMPLETED_SEGMENTS`tPASS","SEALED_KEYSETS_AND_STREAMS`tPASS","SCOPE`tExact Aut/order-8 profile only; no seed predicates.","VERIFY`tPASS","DONE")
[IO.File]::WriteAllLines((Join-Path $BaseDir $verifyName),$v,[Text.UTF8Encoding]::new($false))
Write-Output "PASS shard12 range=11341-11845 window=505 parity=501 classes=$classes raw=$raw isoMs=$iso autMs=$aut classMs=$class segmentMs=$segmentMs maxRssKb=$maxRss"
