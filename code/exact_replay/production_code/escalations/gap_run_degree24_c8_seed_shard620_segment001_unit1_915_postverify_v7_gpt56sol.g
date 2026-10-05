# Exact wrapper for sealed degree-24 seed workload shard620.
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD620_SEGMENT001_UNIT1_915_POSTVERIFY_V7_GPT56SOL.txt";
STOP_AFTER_UNIT:=fail;
INTERNAL_GUARD_MS:=1320000; START_UNIT:=1;
INITIAL_COUNTERS:=[0,0,0,0,0,0,0,0,0,0,0,0];
PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";
PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0;
PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";
CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD620_CHECKPOINT_GPT56SOL.txt";
CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD620_CHECKPOINT_TMP_GPT56SOL.txt";
EXPECTED_PROFILE_SHA256:="1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2";
EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard620_v7_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="939DD6906DAED5B2C81D4930E8A9E313382E428C497DCD62008C469A869F72BD";
S620_RECORDS:=[
rec(k:=15607,first:=45,last:=160,unitFirst:=1,unitLast:=116,order:=49152,autOrder:=1572864,parity:=7,classes:=160,raw:=7864320,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1445),
rec(k:=15608,first:=1,last:=136,unitFirst:=117,unitLast:=252,order:=49152,autOrder:=393216,parity:=7,classes:=136,raw:=6684672,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1033),
rec(k:=15609,first:=1,last:=60,unitFirst:=253,unitLast:=312,order:=49152,autOrder:=393216,parity:=7,classes:=60,raw:=2949120,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1187),
rec(k:=15610,first:=1,last:=603,unitFirst:=313,unitLast:=915,order:=49152,autOrder:=1572864,parity:=7,classes:=940,raw:=46202880,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=2611)
];
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard620_v7_gpt56sol.g");
