# Exact wrapper for sealed degree-24 seed workload shard342.
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD342_SEGMENT001_UNIT1_915_POSTVERIFY_V7_GPT56SOL.txt";
STOP_AFTER_UNIT:=fail;
INTERNAL_GUARD_MS:=1320000; START_UNIT:=1;
INITIAL_COUNTERS:=[0,0,0,0,0,0,0,0,0,0,0,0];
PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";
PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0;
PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";
CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD342_CHECKPOINT_GPT56SOL.txt";
CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD342_CHECKPOINT_TMP_GPT56SOL.txt";
EXPECTED_PROFILE_SHA256:="1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2";
EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard342_v7_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="CC4C1B6973B3C5099580E1ACFEA87F1A4DC0C2DA5CB2DB24199B632F6BE04FD0";
S342_RECORDS:=[
rec(k:=14819,first:=162,last:=240,unitFirst:=1,unitLast:=79,order:=49152,autOrder:=3145728,parity:=3,classes:=240,raw:=11796480,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=2711),
rec(k:=14820,first:=1,last:=64,unitFirst:=80,unitLast:=143,order:=49152,autOrder:=1572864,parity:=3,classes:=64,raw:=3145728,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=2586),
rec(k:=14821,first:=1,last:=236,unitFirst:=144,unitLast:=379,order:=49152,autOrder:=3145728,parity:=3,classes:=236,raw:=11599872,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1324),
rec(k:=14822,first:=1,last:=224,unitFirst:=380,unitLast:=603,order:=49152,autOrder:=1572864,parity:=3,classes:=224,raw:=11010048,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=2707),
rec(k:=14823,first:=1,last:=224,unitFirst:=604,unitLast:=827,order:=49152,autOrder:=1572864,parity:=3,classes:=224,raw:=11010048,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=2419),
rec(k:=14824,first:=1,last:=88,unitFirst:=828,unitLast:=915,order:=49152,autOrder:=3145728,parity:=3,classes:=276,raw:=13565952,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=4642)
];
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard342_v7_gpt56sol.g");
