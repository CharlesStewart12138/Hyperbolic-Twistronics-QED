# Exact wrapper for sealed degree-24 seed workload shard452.
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD452_SEGMENT001_UNIT1_915_POSTVERIFY_V7_GPT56SOL.txt";
STOP_AFTER_UNIT:=fail;
INTERNAL_GUARD_MS:=1320000; START_UNIT:=1;
INITIAL_COUNTERS:=[0,0,0,0,0,0,0,0,0,0,0,0];
PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";
PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0;
PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";
CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD452_CHECKPOINT_GPT56SOL.txt";
CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD452_CHECKPOINT_TMP_GPT56SOL.txt";
EXPECTED_PROFILE_SHA256:="1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2";
EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard452_v7_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="7B0AD72CB40C3E086C4D4192D929AEACF4FA7A676D836FA644BDBE02B96A40DB";
S452_RECORDS:=[
rec(k:=15176,first:=32,last:=120,unitFirst:=1,unitLast:=89,order:=49152,autOrder:=1572864,parity:=1,classes:=120,raw:=5898240,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1954),
rec(k:=15177,first:=1,last:=320,unitFirst:=90,unitLast:=409,order:=49152,autOrder:=1572864,parity:=3,classes:=320,raw:=15728640,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1679),
rec(k:=15178,first:=1,last:=152,unitFirst:=410,unitLast:=561,order:=49152,autOrder:=786432,parity:=3,classes:=152,raw:=7471104,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1382),
rec(k:=15179,first:=1,last:=134,unitFirst:=562,unitLast:=695,order:=49152,autOrder:=1572864,parity:=3,classes:=134,raw:=6586368,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1863),
rec(k:=15180,first:=1,last:=124,unitFirst:=696,unitLast:=819,order:=49152,autOrder:=786432,parity:=3,classes:=124,raw:=6094848,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1227),
rec(k:=15181,first:=1,last:=96,unitFirst:=820,unitLast:=915,order:=49152,autOrder:=1572864,parity:=3,classes:=320,raw:=15728640,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1745)
];
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard452_v7_gpt56sol.g");
