param([string]$BaseDir = ".")
$ErrorActionPreference = "Stop"

function Assert-Eq($Actual,$Expected,[string]$Label) {
    if([string]$Actual -ne [string]$Expected){ throw "$Label mismatch: actual=$Actual expected=$Expected" }
}
function Parse-Pairs([string]$Line,[string]$Prefix,[int]$Start=1) {
    $f=$Line -split "`t"
    if($f[0] -ne $Prefix -or (($f.Count-$Start)%2) -ne 0){ throw "malformed $Prefix line: $Line" }
    $h=@{}
    for($i=$Start;$i -lt $f.Count;$i+=2){ if($h.ContainsKey($f[$i])){throw "duplicate field $($f[$i])"};$h[$f[$i]]=$f[$i+1] }
    return $h
}
function Load-Map([string]$Name,[bool]$HasSolvable) {
    $m=@{}
    foreach($line in [IO.File]::ReadAllLines((Join-Path $BaseDir $Name))){
        if($line -notmatch '^ENTRY\t24T([0-9]+)\t'){continue}
        $k=[int]$Matches[1];if($m.ContainsKey($k)){throw "$Name duplicate 24T$k"}
        $f=$line -split "`t";$h=@{};for($i=2;$i -lt $f.Count;$i+=2){$h[$f[$i]]=$f[$i+1]}
        $m[$k]=[pscustomobject]@{Order=[int64]$h.ORDER;Parity=[int64]$h.PARITY_MAPS;Solvable=if($HasSolvable){[int]$h.SOLVABLE}else{$null}}
    }
    return $m
}
function Expected-Keys($Map,[int]$Lo,[int]$Hi) {
    return @($Map.Keys | ForEach-Object {[int]$_} | Where-Object {$_ -ge $Lo -and $_ -le $Hi} | Sort-Object)
}
function Parse-Entry([string]$Line,[string]$Representation) {
    $f=$Line -split "`t"
    if($f[0] -ne 'ENTRY' -or $f[1] -notmatch '^24T([0-9]+)$' -or (($f.Count-2)%2) -ne 0){throw "malformed ENTRY: $Line"}
    $k=[int]$Matches[1];$h=@{};for($i=2;$i -lt $f.Count;$i+=2){if($h.ContainsKey($f[$i])){throw "24T$k duplicate field $($f[$i])"};$h[$f[$i]]=$f[$i+1]}
    foreach($n in @('ORDER','SOLVABLE_G','AUT_ORDER','AUT_MS','METHOD','CLASS_MS','ORDER8_CLASSES','RAW_PAIRS')){if(-not $h.ContainsKey($n)){throw "24T$k missing $n"}}
    if($Representation -eq 'pc_transport'){
        foreach($n in @('PARITY_MAPS_G','PC_ORDER','PARITY_MAPS_P','ISO_MS')){if(-not $h.ContainsKey($n)){throw "24T$k missing $n"}}
        $parity=[int64]$h.PARITY_MAPS_G;$pcOrder=[int64]$h.PC_ORDER;$iso=[int64]$h.ISO_MS
        Assert-Eq $h.PARITY_MAPS_P $h.PARITY_MAPS_G "24T$k transported parity"
        Assert-Eq $h.PC_ORDER $h.ORDER "24T$k transported order"
    } else {
        if(-not $h.ContainsKey('PARITY_MAPS')){throw "24T$k missing PARITY_MAPS"}
        $parity=[int64]$h.PARITY_MAPS;$pcOrder=[int64]$h.ORDER;$iso=[int64]0
    }
    return [pscustomobject]@{K=$k;Order=[int64]$h.ORDER;Solvable=$h.SOLVABLE_G;Parity=$parity;PCOrder=$pcOrder;AutOrder=$h.AUT_ORDER;IsoMs=$iso;AutMs=[int64]$h.AUT_MS;Method=$h.METHOD;ClassMs=[int64]$h.CLASS_MS;Classes=[int64]$h.ORDER8_CLASSES;Raw=[int64]$h.RAW_PAIRS;Representation=$Representation;Line=$Line}
}
function Parse-Wall-Centis([string]$Wall) {
    $p=$Wall -split ':'
    if($p.Count -eq 2){$minutes=[int64]$p[0];$hours=0;$seconds=[decimal]::Parse($p[1],[Globalization.CultureInfo]::InvariantCulture)}
    elseif($p.Count -eq 3){$hours=[int64]$p[0];$minutes=[int64]$p[1];$seconds=[decimal]::Parse($p[2],[Globalization.CultureInfo]::InvariantCulture)}
    else{throw "malformed wall: $Wall"}
    return [int64](($hours*3600+$minutes*60)*100+[decimal]::Round($seconds*100,0))
}
function Format-Wall-Centis([int64]$Centis) {
    $minutes=[math]::Floor($Centis/6000);$seconds=($Centis-$minutes*6000)/100.0
    return ('{0}:{1:00.00}' -f $minutes,$seconds)
}
function Check-Telemetry([string]$StdoutName,[string]$StderrName,[string]$ExpectedWrote,[string]$Wrapper) {
    $stdout=[IO.File]::ReadAllText((Join-Path $BaseDir $StdoutName));$stderr=[IO.File]::ReadAllText((Join-Path $BaseDir $StderrName))
    Assert-Eq $stdout.Trim() $ExpectedWrote "$StdoutName WROTE"
    if($stderr -notmatch 'Elapsed \(wall clock\) time \(h:mm:ss or m:ss\): ([^\r\n]+)'){throw "$StderrName missing wall"};$wall=$Matches[1].Trim()
    if($stderr -notmatch 'Maximum resident set size \(kbytes\): ([0-9]+)'){throw "$StderrName missing RSS"};$rss=[int64]$Matches[1]
    if($stderr -notmatch 'Exit status: 0'){throw "$StderrName wrong exit"}
    if($stderr -notmatch [regex]::Escape($Wrapper)){throw "$StderrName does not bind $Wrapper"}
    if($rss -ge 50331648){throw "$StderrName RSS guard exceeded"}
    return [pscustomobject]@{Wall=$wall;WallCentis=Parse-Wall-Centis $wall;Rss=$rss}
}
function Check-Segment($Def,$Sol,$Win) {
    $lines=[IO.File]::ReadAllLines((Join-Path $BaseDir $Def.Output))
    $cert=if($Def.Representation -eq 'pc_transport'){'PF-GRP-001-C8-TRANSITIVE-DEGREE24-AUT-PC-DOMAIN-RECOVERY-CHECKPOINT'}else{'PF-GRP-001-C8-TRANSITIVE-DEGREE24-AUT-CHECKPOINT'}
    $scope=if($Def.Representation -eq 'pc_transport'){'Exact pc-isomorphic Aut(G), exact-order-8 conjugacy classes, and raw=Size(G)*class-count for solvable parity-capable order-window targets only; no seeds.'}else{'Exact Aut(G), exact-order-8 conjugacy classes, and raw=Size(G)*class-count for parity-capable order-window targets only; no seeds.'}
    $header=@("CERTIFICATE_PROFILE`t$cert","GAP_VERSION`t4.12.1","DATABASE`t25000","RANGE`t$($Def.Lo)`t$($Def.Hi)","GUARD_MS`t1320000","EXPECTED_ORDER_WINDOW`t$($Def.Window)","EXPECTED_PARITY`t$($Def.Parity)","SCOPE`t$scope","RECOVERY`tENTRY and CHECKPOINT certify each completed eligible key; SCAN_CHECKPOINT certifies every 25th completed catalogue key.")
    if($lines.Count -lt 11){throw "$($Def.Label) truncated"};for($i=0;$i -lt $header.Count;$i++){Assert-Eq $lines[$i] $header[$i] "$($Def.Label) header $($i+1)"}
    Assert-Eq @($lines|Where-Object{$_ -match '^TOTAL\t'}).Count 1 "$($Def.Label) TOTAL count";Assert-Eq $lines[-1] 'DONE' "$($Def.Label) DONE"
    Assert-Eq @($lines|Where-Object{$_ -match '^(TOTAL_PARTIAL|STOPPED_GUARD)'}).Count 0 "$($Def.Label) guard markers"
    $entries=@();for($i=0;$i -lt $lines.Count;$i++){if($lines[$i] -match '^ENTRY\t'){$entries+=Parse-Entry $lines[$i] $Def.Representation}}
    $expected=Expected-Keys $Sol $Def.Lo $Def.Hi;Assert-Eq $entries.Count $expected.Count "$($Def.Label) entry count";Assert-Eq @($entries|Group-Object K|Where-Object{$_.Count-ne1}).Count 0 "$($Def.Label) duplicate keys";Assert-Eq @(Compare-Object $expected @($entries.K)).Count 0 "$($Def.Label) keyset"
    [int64]$classes=0;[int64]$raw=0;[int64]$iso=0;[int64]$aut=0;[int64]$class=0;$previous=-1
    for($j=0;$j -lt $entries.Count;$j++){
        $e=$entries[$j];if($e.K-le$previous){throw "$($Def.Label) non-increasing key 24T$($e.K)"};$previous=$e.K;$sealed=$Sol[$e.K]
        Assert-Eq $e.Order $sealed.Order "$($Def.Label) 24T$($e.K) order";Assert-Eq $e.Parity $sealed.Parity "$($Def.Label) 24T$($e.K) parity";Assert-Eq $e.Solvable $(if($sealed.Solvable-eq1){'true'}else{'false'}) "$($Def.Label) 24T$($e.K) solvability"
        if($Def.Representation -eq 'pc_transport'){Assert-Eq $e.Solvable 'true' "$($Def.Label) pc route";Assert-Eq $e.PCOrder $e.Order "$($Def.Label) 24T$($e.K) pc order"}
        else{Assert-Eq $e.Solvable 'false' "$($Def.Label) native route"}
        Assert-Eq $e.Raw ($e.Order*$e.Classes) "$($Def.Label) 24T$($e.K) raw";if($e.Parity-le0-or$e.AutMs-lt0-or$e.ClassMs-lt0-or$e.IsoMs-lt0-or$e.AutOrder-notmatch'^[1-9][0-9]*$'-or$e.Method-notin@('pc','native')){throw "$($Def.Label) invalid entry 24T$($e.K)"}
        $classes+=$e.Classes;$raw+=$e.Raw;$iso+=$e.IsoMs;$aut+=$e.AutMs;$class+=$e.ClassMs
        $idx=[Array]::IndexOf($lines,$e.Line);if($idx-lt0-or$idx+1-ge$lines.Count){throw "$($Def.Label) missing adjacent checkpoint 24T$($e.K)"};$cp=Parse-Pairs $lines[$idx+1] 'CHECKPOINT'
        Assert-Eq $cp.LAST_COMPLETE_K $e.K "$($Def.Label) cp key";Assert-Eq $cp.PROCESSED ($j+1) "$($Def.Label) cp processed";Assert-Eq $cp.ORDER8_CLASSES $classes "$($Def.Label) cp classes";Assert-Eq $cp.RAW_PAIRS $raw "$($Def.Label) cp raw";if($Def.Representation-eq'pc_transport'){Assert-Eq $cp.ISO_MS $iso "$($Def.Label) cp iso"}
    }
    $scans=@($lines|Where-Object{$_-match'^SCAN_CHECKPOINT\t'});$scanKeys=@();for($k=$Def.Lo;$k-le$Def.Hi;$k++){if($k%25-eq0){$scanKeys+=$k}};Assert-Eq $scans.Count $scanKeys.Count "$($Def.Label) scan count"
    for($j=0;$j-lt$scans.Count;$j++){$h=Parse-Pairs $scans[$j] 'SCAN_CHECKPOINT';$k=$scanKeys[$j];$prefix=@($entries|Where-Object{$_.K-le$k});Assert-Eq $h.LAST_COMPLETE_K $k "$($Def.Label) scan key";Assert-Eq $h.ORDER_WINDOW (Expected-Keys $Win $Def.Lo $k).Count "$($Def.Label) scan window";Assert-Eq $h.PROCESSED $prefix.Count "$($Def.Label) scan processed";Assert-Eq $h.ORDER8_CLASSES ([int64](($prefix|Measure-Object Classes -Sum).Sum)) "$($Def.Label) scan classes";Assert-Eq $h.RAW_PAIRS ([int64](($prefix|Measure-Object Raw -Sum).Sum)) "$($Def.Label) scan raw";if($Def.Representation-eq'pc_transport'){Assert-Eq $h.ISO_MS ([int64](($prefix|Measure-Object IsoMs -Sum).Sum)) "$($Def.Label) scan iso"}}
    # RANGE has two values, so validate the exact TOTAL line with a schema regex, then validate every scientific total.
    $tp='^TOTAL\tDEGREE\t24\tDATABASE\t25000\tRANGE\t'+$Def.Lo+'\t'+$Def.Hi+'\tLAST_COMPLETE_K\t'+$Def.Hi+'\tORDER_WINDOW\t([0-9]+)\tPROCESSED\t([0-9]+)\tORDER8_CLASSES\t([0-9]+)\tRAW_PAIRS\t([0-9]+)\t'+$(if($Def.Representation-eq'pc_transport'){'ISO_MS\t([0-9]+)\t'}else{''})+'AUT_MS\t([0-9]+)\tCLASS_MS\t([0-9]+)\tMS\t([0-9]+)$';$tl=@($lines|Where-Object{$_-match'^TOTAL\t'})[0];if($tl-notmatch$tp){throw "$($Def.Label) malformed TOTAL: $tl"}
    $g=$Matches;if($Def.Representation-eq'pc_transport'){$tw=$g[1];$tproc=$g[2];$tclasses=$g[3];$traw=$g[4];$tiso=$g[5];$taut=$g[6];$tclass=$g[7];$tms=$g[8]}else{$tw=$g[1];$tproc=$g[2];$tclasses=$g[3];$traw=$g[4];$tiso=0;$taut=$g[5];$tclass=$g[6];$tms=$g[7]}
    Assert-Eq $tw $Def.Window "$($Def.Label) total window";Assert-Eq $tproc $Def.Parity "$($Def.Label) total parity";Assert-Eq $tclasses $classes "$($Def.Label) total classes";Assert-Eq $traw $raw "$($Def.Label) total raw";Assert-Eq $tiso $iso "$($Def.Label) total iso";Assert-Eq $taut $aut "$($Def.Label) total aut";Assert-Eq $tclass $class "$($Def.Label) total class"
    $tele=Check-Telemetry $Def.Stdout $Def.Stderr "WROTE /mnt/d/work/revise/production_code/escalations/$($Def.Output)" $Def.Wrapper
    return [pscustomobject]@{Def=$Def;Entries=$entries;Lines=$lines;Classes=$classes;Raw=$raw;Iso=$iso;Aut=$aut;Class=$class;Ms=[int64]$tms;Scans=$scans.Count;Telemetry=$tele}
}

$sol=Load-Map 'GAP_TRANSITIVE_DEGREE24_SOLVABILITY_10568_13274_GPT56SOL.txt' $true;$win=Load-Map 'GAP_TRANSITIVE_DEGREE24_PARITY_10568_13274_GPT56SOL.txt' $false
$defs=@(
 [pscustomobject]@{Label='S1';Lo=11846;Hi=12111;Window=266;Parity=264;Representation='pc_transport';Wrapper='gap_run_degree24_aut_profile_shard13_s1_11846_12111_pc_domain_gpt56sol.g';Output='GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_11846_12111_PC_DOMAIN_RECOVERY_CHECKPOINT_GPT56SOL.txt';Stdout='GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_SHARD13_S1_RUN_STDOUT_GPT56SOL.txt';Stderr='GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_SHARD13_S1_RUN_STDERR_GPT56SOL.txt'},
 [pscustomobject]@{Label='S2';Lo=12112;Hi=12139;Window=28;Parity=28;Representation='native';Wrapper='gap_run_degree24_aut_profile_shard13_s2_12112_12139_generic_gpt56sol.g';Output='GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_12112_12139_CHECKPOINT_GPT56SOL.txt';Stdout='GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_SHARD13_S2_RUN_STDOUT_GPT56SOL.txt';Stderr='GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_SHARD13_S2_RUN_STDERR_GPT56SOL.txt'},
 [pscustomobject]@{Label='S3';Lo=12140;Hi=12203;Window=64;Parity=60;Representation='pc_transport';Wrapper='gap_run_degree24_aut_profile_shard13_s3_12140_12203_pc_domain_gpt56sol.g';Output='GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_12140_12203_PC_DOMAIN_RECOVERY_CHECKPOINT_GPT56SOL.txt';Stdout='GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_SHARD13_S3_RUN_STDOUT_GPT56SOL.txt';Stderr='GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_SHARD13_S3_RUN_STDERR_GPT56SOL.txt'},
 [pscustomobject]@{Label='S4';Lo=12204;Hi=12205;Window=2;Parity=2;Representation='native';Wrapper='gap_run_degree24_aut_profile_shard13_s4_12204_12205_generic_gpt56sol.g';Output='GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_12204_12205_CHECKPOINT_GPT56SOL.txt';Stdout='GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_SHARD13_S4_RUN_STDOUT_GPT56SOL.txt';Stderr='GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_SHARD13_S4_RUN_STDERR_GPT56SOL.txt'},
 [pscustomobject]@{Label='S5';Lo=12206;Hi=12332;Window=127;Parity=122;Representation='pc_transport';Wrapper='gap_run_degree24_aut_profile_shard13_s5_12206_12332_pc_domain_gpt56sol.g';Output='GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_12206_12332_PC_DOMAIN_RECOVERY_CHECKPOINT_GPT56SOL.txt';Stdout='GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_SHARD13_S5_RUN_STDOUT_GPT56SOL.txt';Stderr='GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_SHARD13_S5_RUN_STDERR_GPT56SOL.txt'}
)
$results=@();foreach($d in $defs){$results+=Check-Segment $d $sol $win}
for($i=0;$i-lt$defs.Count-1;$i++){Assert-Eq ($defs[$i].Hi+1) $defs[$i+1].Lo "segment adjacency $i"};Assert-Eq $defs[0].Lo 11846 'full lo';Assert-Eq $defs[-1].Hi 12332 'full hi'
$fullKeys=Expected-Keys $sol 11846 12332;$fullWindow=Expected-Keys $win 11846 12332;Assert-Eq $fullKeys.Count 476 'full parity';Assert-Eq $fullWindow.Count 487 'full window'
$all=@($results|ForEach-Object{$_.Entries}|Sort-Object K);Assert-Eq $all.Count 476 'merged entry count';Assert-Eq @($all|Group-Object K|Where-Object{$_.Count-ne1}).Count 0 'merged duplicate';Assert-Eq @(Compare-Object $fullKeys @($all.K)).Count 0 'merged keyset'
$pc=@($all|Where-Object{$_.Representation-eq'pc_transport'});$native=@($all|Where-Object{$_.Representation-eq'native'});Assert-Eq $pc.Count 446 'pc count';Assert-Eq $native.Count 30 'native count';Assert-Eq @($pc|Where-Object{$_.Solvable-ne'true'}).Count 0 'pc solvability';Assert-Eq @($native|Where-Object{$_.Solvable-ne'false'}).Count 0 'native nonsolvability'
[int64]$classes=($all|Measure-Object Classes -Sum).Sum;[int64]$raw=($all|Measure-Object Raw -Sum).Sum;[int64]$iso=($all|Measure-Object IsoMs -Sum).Sum;[int64]$aut=($all|Measure-Object AutMs -Sum).Sum;[int64]$class=($all|Measure-Object ClassMs -Sum).Sum;[int64]$gapMs=($results|Measure-Object Ms -Sum).Sum;[int64]$scans=($results|Measure-Object Scans -Sum).Sum
Assert-Eq $classes 67899 'full classes';Assert-Eq $raw 858757344 'full raw';Assert-Eq $iso 491 'full iso';Assert-Eq $aut 162135 'full aut';Assert-Eq $class 415915 'full class';Assert-Eq $gapMs 595057 'full gap ms';Assert-Eq $scans 20 'full scans'
[int64]$wallCentis=($results|ForEach-Object{$_.Telemetry.WallCentis}|Measure-Object -Sum).Sum;$wall=Format-Wall-Centis $wallCentis;Assert-Eq $wall '10:00.00' 'full wall';[int64]$maxRss=($results|ForEach-Object{$_.Telemetry.Rss}|Measure-Object -Maximum).Maximum;Assert-Eq $maxRss 445056 'max rss'
$mergedName='GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_11846_12332_MERGED_ROUTED_GPT56SOL.txt';$m=[Collections.Generic.List[string]]::new();$m.Add("CERTIFICATE_PROFILE`tPF-GRP-001-C8-TRANSITIVE-DEGREE24-AUT-SHARD13-MERGED-ROUTED");$m.Add("GAP_VERSION`t4.12.1");$m.Add("DATABASE`t25000");$m.Add("RANGE`t11846`t12332");$m.Add("ORDER_WINDOW`t487");$m.Add("PARITY_KEYS`t476");$m.Add("SEGMENTS`t11846..12111:pc`t12112..12139:native`t12140..12203:pc`t12204..12205:native`t12206..12332:pc");$m.Add("SCOPE`tExact Aut/order-8 profile invariants only; no seed predicates.")
foreach($e in $all){$m.Add("ENTRY`t24T$($e.K)`tORDER`t$($e.Order)`tSOLVABLE_G`t$($e.Solvable)`tPARITY_MAPS`t$($e.Parity)`tREPRESENTATION`t$($e.Representation)`tPC_ORDER`t$($e.PCOrder)`tAUT_ORDER`t$($e.AutOrder)`tISO_MS`t$($e.IsoMs)`tAUT_MS`t$($e.AutMs)`tMETHOD`t$($e.Method)`tCLASS_MS`t$($e.ClassMs)`tORDER8_CLASSES`t$($e.Classes)`tRAW_PAIRS`t$($e.Raw)")}
$m.Add("TOTAL`tDEGREE`t24`tDATABASE`t25000`tRANGE`t11846`t12332`tORDER_WINDOW`t487`tPROCESSED`t476`tPC_TRANSPORT`t446`tNATIVE_NONSOLVABLE`t30`tORDER8_CLASSES`t$classes`tRAW_PAIRS`t$raw`tISO_MS`t$iso`tAUT_MS`t$aut`tCLASS_MS`t$class`tSEGMENT_GAP_MS`t$gapMs");$m.Add('DONE');[IO.File]::WriteAllLines((Join-Path $BaseDir $mergedName),$m,[Text.UTF8Encoding]::new($false))
$verifyName='GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_SHARD13_VERIFY_GPT56SOL.txt';$v=@("CERTIFICATE_VERIFY`tPF-GRP-001-C8-TRANSITIVE-DEGREE24-AUT-PROFILE-SHARD13-ROUTED","RANGE`t11846`t12332","SEGMENT_RANGES_DISJOINT_CONTIGUOUS`tPASS","ORDER_WINDOW`t487","PARITY_KEYS`t476","ENTRY_KEYS_EXACT`tPASS","SOLVABLE_PC_ROUTE`t446`tPASS","NONSOLVABLE_NATIVE_ROUTE`t30`tPASS","PC_ORDER_PARITY_TRANSPORT`t446`tPASS","RAW_IDENTITIES`t476`tPASS","ENTRY_CHECKPOINT_PAIRS`t476`tPASS","SCAN_CHECKPOINTS`t20`tPASS","UNIQUE_TOTAL_DONE_NO_GUARD`t5`tPASS","ORDER8_CLASSES`t$classes","RAW_PAIRS`t$raw","ISO_MS`t$iso","AUT_MS`t$aut","CLASS_MS`t$class","SEGMENT_GAP_MS`t$gapMs","WALL`t$wall","MAX_RSS_KB`t$maxRss","SEALED_KEYSETS_AND_STREAMS`tPASS","CANDIDATE_OR_SEED_PREDICATES`tNOT_RUN","VERIFY`tPASS","DONE");[IO.File]::WriteAllLines((Join-Path $BaseDir $verifyName),$v,[Text.UTF8Encoding]::new($false))
$aggregateName='GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_SHARD13_AGGREGATE_GPT56SOL.txt';$ratio=[math]::Round(($aut+$class)/367101.0,6).ToString('0.000000',[Globalization.CultureInfo]::InvariantCulture);$rawRatio=[math]::Round($raw/149085888.0,6).ToString('0.000000',[Globalization.CultureInfo]::InvariantCulture);$a=@("CERTIFICATE`tPF-GRP-001-C8-TRANSITIVE-DEGREE24-AUT-PROFILE-SHARD13","STATUS`tSHARD_COMPLETE_ROUTED_INDEPENDENTLY_VERIFIED","DEGREE`t24","DATABASE`t25000","RANGE`t11846`t12332","LAST_COMPLETE_K`t12332","ORDER_WINDOW`t487","PARITY_KEYS`t476","PARITY_EXCLUDED`t11","SEGMENTS`t11846..12111-pc;12112..12139-native;12140..12203-pc;12204..12205-native;12206..12332-pc","PC_TRANSPORT_KEYS`t446","NATIVE_NONSOLVABLE_KEYS`t30","ORDER8_CLASSES`t$classes","RAW_PAIRS`t$raw","ISO_MS`t$iso","AUT_MS`t$aut","CLASS_MS`t$class","AUT_PLUS_CLASS_MS`t$($aut+$class)","SEGMENT_GAP_MS`t$gapMs","POINT_FORECAST_MS`t367101","ACTUAL_TO_POINT_RATIO`t$ratio","POINT_FORECAST_CLASSES`t9822","POINT_FORECAST_RAW_PAIRS`t149085888","ACTUAL_TO_RAW_POINT_RATIO`t$rawRatio","ENTRY_CHECKPOINT_PAIRS`t476","SCAN_CHECKPOINTS`t20","RAW_IDENTITIES_PASS`t476","PC_TRANSPORT_IDENTITIES_PASS`t446","CANDIDATE_OR_SEED_PREDICATES`tNOT_RUN","INTERNAL_GUARD_MS`t1320000","EXTERNAL_WALL_GUARD_SECONDS`t1400","WALL`t$wall","S1_WALL`t$($results[0].Telemetry.Wall)","S2_WALL`t$($results[1].Telemetry.Wall)","S3_WALL`t$($results[2].Telemetry.Wall)","S4_WALL`t$($results[3].Telemetry.Wall)","S5_WALL`t$($results[4].Telemetry.Wall)","MAX_RSS_KB`t$maxRss","EXTERNAL_GUARD_EVENTS`t0","GUARD_TRIGGERED_FINAL_SEGMENT`t0","VERIFY`tPASS","SCOPE`tExact Aut(G), exact-order-8 conjugacy-class count, and raw=Size(G)*class-count for range 11846..12332 only. This is not full degree-24 closure and contains no seed test.","DONE");[IO.File]::WriteAllLines((Join-Path $BaseDir $aggregateName),$a,[Text.UTF8Encoding]::new($false))
$certName='GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_SHARD13_GPT56SOL_CERTIFICATE.md';$c=@('# Degree-24 exact Aut/order-8 profile - shard 13','','Status: **complete and independently verified for catalogue range `11846..12332` only**. This is not full degree-24 closure.','',"The sealed order/parity and solvability evidence partitions the 476 parity-capable keys exactly into 446 solvable and 30 nonsolvable keys. The five contiguous catalogue segments are `11846..12111` (pc), `12112..12139` (native), `12140..12203` (pc), `12204..12205` (native), and `12206..12332` (pc). Their union is the full shard range with no overlap or omission. The nonsolvable keys are exactly `12112..12139` and `12204..12205`; no pc transport is used for them.",'','For every solvable key, GAP constructs an exact isomorphism `f:G->P` onto a pc group. Conjugation `a |-> f a f^-1` is an isomorphism `Aut(G)->Aut(P)`, preserving automorphism order and conjugacy. The scanner also checks `|P|=|G|` and equality of the exact numbers of epimorphisms onto `C2`; therefore every exact-order-8 class count and `|G| * class-count` raw contribution is transported without change. Nonsolvable keys use the original exact permutation-domain computation.','',"Exact totals are: order-window 487; parity keys 476; exact-order-8 automorphism conjugacy classes $classes; raw pairs $raw; pc-isomorphism time $iso ms; automorphism time $aut ms; class time $class ms; completed-segment GAP time $gapMs ms. There are 476 adjacent ENTRY/CHECKPOINT pairs and 20 exact scan checkpoints.",'',"All five outputs have their complete headers, one TOTAL, terminal DONE, no partial/guard marker, and exit status 0. Exact wall records sum to $wall; peak RSS is $maxRss KiB, below 48 GiB. The Aut-plus-class time is $($aut+$class) ms, or $ratio times the point forecast. The actual raw total is $rawRatio times the point forecast.",'','The deterministic verifier checks the sealed key sets, disjoint routing, every raw identity, every transported order/parity identity, cumulative checkpoints, scan checkpoints, totals, streams, and resource records. It emits the normalized merged profile, verification record, and aggregate only after all assertions pass. No inverse, relator, B3, generation, centralizer-orbit, candidate, or other seed predicate was run.','',"Conclusion: shard 13 is an exact Aut/order-8 profile result for `24T11846..24T12332`. Within the sealed campaign, shards 1-13 are complete; shards 14-32 remain unrun.");[IO.File]::WriteAllLines((Join-Path $BaseDir $certName),$c,[Text.UTF8Encoding]::new($false))
Write-Output "PASS shard13 range=11846-12332 window=487 parity=476 pc=446 native=30 classes=$classes raw=$raw isoMs=$iso autMs=$aut classMs=$class gapMs=$gapMs wall=$wall maxRssKb=$maxRss"
