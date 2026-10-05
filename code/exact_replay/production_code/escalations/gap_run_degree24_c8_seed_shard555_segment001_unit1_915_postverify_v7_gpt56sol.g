# Exact wrapper for sealed degree-24 seed workload shard555.
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD555_SEGMENT001_UNIT1_915_POSTVERIFY_V7_GPT56SOL.txt";
STOP_AFTER_UNIT:=fail;
INTERNAL_GUARD_MS:=1320000; START_UNIT:=1;
INITIAL_COUNTERS:=[0,0,0,0,0,0,0,0,0,0,0,0];
PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";
PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0;
PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";
CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD555_CHECKPOINT_GPT56SOL.txt";
CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD555_CHECKPOINT_TMP_GPT56SOL.txt";
EXPECTED_PROFILE_SHA256:="1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2";
EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard555_v7_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="169F26B14D73350CADEEF6D385447256ED3C2DC53823BFC14B4E7654C566387A";
S555_RECORDS:=[
rec(k:=15424,first:=59,last:=484,unitFirst:=1,unitLast:=426,order:=49152,autOrder:=3145728,parity:=3,classes:=484,raw:=23789568,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1181),
rec(k:=15425,first:=1,last:=160,unitFirst:=427,unitLast:=586,order:=49152,autOrder:=393216,parity:=7,classes:=160,raw:=7864320,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1332),
rec(k:=15426,first:=1,last:=274,unitFirst:=587,unitLast:=860,order:=49152,autOrder:=3145728,parity:=3,classes:=274,raw:=13467648,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1392),
rec(k:=15427,first:=1,last:=55,unitFirst:=861,unitLast:=915,order:=49152,autOrder:=1572864,parity:=3,classes:=320,raw:=15728640,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1336)
];
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard555_v7_gpt56sol.g");
