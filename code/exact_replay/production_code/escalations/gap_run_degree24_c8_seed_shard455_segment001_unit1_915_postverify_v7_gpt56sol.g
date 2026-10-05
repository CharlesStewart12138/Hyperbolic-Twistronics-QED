# Exact wrapper for sealed degree-24 seed workload shard455.
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD455_SEGMENT001_UNIT1_915_POSTVERIFY_V7_GPT56SOL.txt";
STOP_AFTER_UNIT:=fail;
INTERNAL_GUARD_MS:=1320000; START_UNIT:=1;
INITIAL_COUNTERS:=[0,0,0,0,0,0,0,0,0,0,0,0];
PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";
PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0;
PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";
CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD455_CHECKPOINT_GPT56SOL.txt";
CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD455_CHECKPOINT_TMP_GPT56SOL.txt";
EXPECTED_PROFILE_SHA256:="1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2";
EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard455_v7_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="8382DF819E3F8338048D4EFE10D37FB3C0B68E4D8CAB3A263B18FEF1E32DE27D";
S455_RECORDS:=[
rec(k:=15187,first:=137,last:=320,unitFirst:=1,unitLast:=184,order:=49152,autOrder:=1572864,parity:=3,classes:=320,raw:=15728640,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1454),
rec(k:=15188,first:=1,last:=274,unitFirst:=185,unitLast:=458,order:=49152,autOrder:=3145728,parity:=3,classes:=274,raw:=13467648,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1159),
rec(k:=15189,first:=1,last:=48,unitFirst:=459,unitLast:=506,order:=49152,autOrder:=1572864,parity:=1,classes:=48,raw:=2359296,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1366),
rec(k:=15190,first:=1,last:=48,unitFirst:=507,unitLast:=554,order:=49152,autOrder:=1572864,parity:=1,classes:=48,raw:=2359296,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1203),
rec(k:=15191,first:=1,last:=361,unitFirst:=555,unitLast:=915,order:=49152,autOrder:=6291456,parity:=7,classes:=370,raw:=18186240,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1970)
];
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard455_v7_gpt56sol.g");
