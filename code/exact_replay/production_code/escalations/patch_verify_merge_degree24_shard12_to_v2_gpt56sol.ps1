param([string]$BaseDir = ".")
$ErrorActionPreference="Stop"
$src=Join-Path $BaseDir 'verify_merge_degree24_aut_profile_shard12_recovery_gpt56sol.ps1'
$dst=Join-Path $BaseDir 'verify_merge_degree24_aut_profile_shard12_recovery_v2_gpt56sol.ps1'
if(Test-Path -LiteralPath $dst){throw 'V2 destination already exists'}
$inputLines=[IO.File]::ReadAllLines($src)
$outputLines=[Collections.Generic.List[string]]::new()
$changedRequired=0;$changedSolvable=0;$changedSingle=0
foreach($line in $inputLines){
    if($line.Contains("foreach(`$n in @('ORDER','SOLVABLE_G','AUT_ORDER'")){
        $outputLines.Add('    foreach($n in @(''ORDER'',''AUT_ORDER'',''AUT_MS'',''METHOD'',''CLASS_MS'',''ORDER8_CLASSES'',''RAW_PAIRS'')){ if(-not $h.ContainsKey($n)){throw "ENTRY 24T$k missing $n"} }')
        $outputLines.Add('    if($h.ContainsKey(''SOLVABLE_G'')){$solvable=$h.SOLVABLE_G}')
        $outputLines.Add('    elseif($Representation -eq ''pc_single''){$solvable=''true''}')
        $outputLines.Add('    else{throw "ENTRY 24T$k missing SOLVABLE_G"}')
        $changedRequired++
    } elseif($line.Contains('return [pscustomobject]') -and $line.Contains('Solvable=$h.SOLVABLE_G;')){
        $outputLines.Add($line.Replace('Solvable=$h.SOLVABLE_G;','Solvable=$solvable;'))
        $changedSolvable++
    } elseif($line.Contains('$entry=Parse-Entry') -and $line.Contains("'pc_transport';Check-Entry")){
        $outputLines.Add($line.Replace("'pc_transport';Check-Entry","'pc_single';Check-Entry"))
        $changedSingle++
    } else {
        $outputLines.Add($line)
    }
}
if($changedRequired-ne1 -or $changedSolvable-ne1 -or $changedSingle-ne1){throw "unexpected replacement counts required=$changedRequired solvable=$changedSolvable single=$changedSingle"}
[IO.File]::WriteAllLines($dst,$outputLines,[Text.UTF8Encoding]::new($false))
Write-Output "WROTE $dst"
