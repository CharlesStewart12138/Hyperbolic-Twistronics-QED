param([string]$BaseDir = ".")
$ErrorActionPreference = "Stop"
$names = @(
  'gap_transitive_degree24_aut_profile_checkpoint_guard_gpt56sol.g',
  'gap_transitive_degree24_aut_profile_pc_domain_checkpoint_guard_recovery_gpt56sol.g',
  'gap_run_degree24_aut_profile_shard13_s1_11846_12111_pc_domain_gpt56sol.g',
  'gap_run_degree24_aut_profile_shard13_s2_12112_12139_generic_gpt56sol.g',
  'gap_run_degree24_aut_profile_shard13_s3_12140_12203_pc_domain_gpt56sol.g',
  'gap_run_degree24_aut_profile_shard13_s4_12204_12205_generic_gpt56sol.g',
  'gap_run_degree24_aut_profile_shard13_s5_12206_12332_pc_domain_gpt56sol.g',
  'GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_11846_12111_PC_DOMAIN_RECOVERY_CHECKPOINT_GPT56SOL.txt',
  'GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_12112_12139_CHECKPOINT_GPT56SOL.txt',
  'GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_12140_12203_PC_DOMAIN_RECOVERY_CHECKPOINT_GPT56SOL.txt',
  'GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_12204_12205_CHECKPOINT_GPT56SOL.txt',
  'GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_12206_12332_PC_DOMAIN_RECOVERY_CHECKPOINT_GPT56SOL.txt',
  'GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_SHARD13_S1_RUN_STDOUT_GPT56SOL.txt',
  'GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_SHARD13_S1_RUN_STDERR_GPT56SOL.txt',
  'GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_SHARD13_S2_RUN_STDOUT_GPT56SOL.txt',
  'GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_SHARD13_S2_RUN_STDERR_GPT56SOL.txt',
  'GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_SHARD13_S3_RUN_STDOUT_GPT56SOL.txt',
  'GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_SHARD13_S3_RUN_STDERR_GPT56SOL.txt',
  'GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_SHARD13_S4_RUN_STDOUT_GPT56SOL.txt',
  'GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_SHARD13_S4_RUN_STDERR_GPT56SOL.txt',
  'GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_SHARD13_S5_RUN_STDOUT_GPT56SOL.txt',
  'GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_SHARD13_S5_RUN_STDERR_GPT56SOL.txt',
  'GAP_TRANSITIVE_DEGREE24_SOLVABILITY_10568_13274_GPT56SOL.txt',
  'GAP_TRANSITIVE_DEGREE24_PARITY_10568_13274_GPT56SOL.txt',
  'build_degree24_aut_profile_32shard_plan_gpt56sol.ps1',
  'GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_32SHARD_PLAN_GPT56SOL.tsv',
  'GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_32SHARD_PLAN_AGGREGATE_GPT56SOL.txt',
  'GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_32SHARD_PLAN_GPT56SOL_CERTIFICATE.md',
  'GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_32SHARD_PLAN_GPT56SOL_MANIFEST.sha256',
  'verify_merge_degree24_aut_profile_shard13_routed_FAILED_V1_RANGE_PARSE_GPT56SOL.ps1',
  'GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_SHARD13_VERIFY_FAILED_V1_RECORD_GPT56SOL.txt',
  'verify_merge_degree24_aut_profile_shard13_routed_FAILED_V2_CERT_INTERPOLATION_GPT56SOL.ps1',
  'GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_SHARD13_CERTIFICATE_SUPERSEDED_V2_LITERAL_GPT56SOL.md',
  'GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_SHARD13_VERIFY_V2_RUN_STDOUT_GPT56SOL.txt',
  'GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_SHARD13_VERIFY_V2_RUN_STDERR_GPT56SOL.txt',
  'GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_SHARD13_VERIFY_FAILED_V2_RECORD_GPT56SOL.txt',
  'verify_merge_degree24_aut_profile_shard13_routed_gpt56sol.ps1',
  'GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_11846_12332_MERGED_ROUTED_GPT56SOL.txt',
  'GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_SHARD13_VERIFY_GPT56SOL.txt',
  'GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_SHARD13_VERIFY_RUN_STDOUT_GPT56SOL.txt',
  'GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_SHARD13_VERIFY_RUN_STDERR_GPT56SOL.txt',
  'GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_SHARD13_AGGREGATE_GPT56SOL.txt',
  'GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_SHARD13_GPT56SOL_CERTIFICATE.md',
  'build_verify_degree24_aut_profile_shard13_manifest_gpt56sol.ps1'
)
if(($names | Select-Object -Unique).Count -ne $names.Count){throw 'duplicate manifest name'}
$out = [Collections.Generic.List[string]]::new()
foreach($name in $names){
  $path=Join-Path $BaseDir $name
  if(-not(Test-Path -LiteralPath $path -PathType Leaf)){throw "missing manifest target: $name"}
  $hash=(Get-FileHash -Algorithm SHA256 -LiteralPath $path).Hash
  $out.Add("$hash  $name")
}
$manifest=Join-Path $BaseDir 'GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_SHARD13_GPT56SOL_MANIFEST.sha256'
[IO.File]::WriteAllLines($manifest,$out,[Text.UTF8Encoding]::new($false))
$lines=[IO.File]::ReadAllLines($manifest);if($lines.Count-ne$names.Count){throw 'manifest count mismatch'}
$bad=0
foreach($line in $lines){if($line-notmatch '^([0-9A-F]{64})  (.+)$'){throw "malformed manifest line: $line"};$actual=(Get-FileHash -Algorithm SHA256 -LiteralPath (Join-Path $BaseDir $Matches[2])).Hash;if($actual-ne$Matches[1]){$bad++}}
if($bad-ne0){throw "manifest mismatches: $bad"}
Write-Output "PASS manifest entries=$($names.Count) mismatches=0"
