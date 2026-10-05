# Exact wrapper for sealed degree-24 seed workload shard575.
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD575_SEGMENT001_UNIT1_915_POSTVERIFY_V7_GPT56SOL.txt";
STOP_AFTER_UNIT:=fail;
INTERNAL_GUARD_MS:=1320000; START_UNIT:=1;
INITIAL_COUNTERS:=[0,0,0,0,0,0,0,0,0,0,0,0];
PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";
PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0;
PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";
CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD575_CHECKPOINT_GPT56SOL.txt";
CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD575_CHECKPOINT_TMP_GPT56SOL.txt";
EXPECTED_PROFILE_SHA256:="1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2";
EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard575_v7_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="644CCBABCFD3AED8E1D6EA45B3A7E0A1A67CC55AB999B44AF6A35B3BFADDF8EA";
S575_RECORDS:=[
rec(k:=15490,first:=172,last:=236,unitFirst:=1,unitLast:=65,order:=49152,autOrder:=3145728,parity:=3,classes:=236,raw:=11599872,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1918),
rec(k:=15491,first:=1,last:=236,unitFirst:=66,unitLast:=301,order:=49152,autOrder:=3145728,parity:=3,classes:=236,raw:=11599872,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1809),
rec(k:=15492,first:=1,last:=272,unitFirst:=302,unitLast:=573,order:=49152,autOrder:=3145728,parity:=3,classes:=272,raw:=13369344,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1858),
rec(k:=15493,first:=1,last:=64,unitFirst:=574,unitLast:=637,order:=49152,autOrder:=1572864,parity:=3,classes:=64,raw:=3145728,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=2393),
rec(k:=15494,first:=1,last:=128,unitFirst:=638,unitLast:=765,order:=49152,autOrder:=3145728,parity:=3,classes:=128,raw:=6291456,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=2868),
rec(k:=15495,first:=1,last:=150,unitFirst:=766,unitLast:=915,order:=49152,autOrder:=3145728,parity:=3,classes:=272,raw:=13369344,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1701)
];
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard575_v7_gpt56sol.g");
