# Exact wrapper for sealed degree-24 seed workload shard634.
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD634_SEGMENT001_UNIT1_915_POSTVERIFY_V7_GPT56SOL.txt";
STOP_AFTER_UNIT:=fail;
INTERNAL_GUARD_MS:=1320000; START_UNIT:=1;
INITIAL_COUNTERS:=[0,0,0,0,0,0,0,0,0,0,0,0];
PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";
PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0;
PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";
CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD634_CHECKPOINT_GPT56SOL.txt";
CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD634_CHECKPOINT_TMP_GPT56SOL.txt";
EXPECTED_PROFILE_SHA256:="1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2";
EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard634_v7_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="CC2C60C5531A3976AC1507465007226DB63ECC1C239514574B569F6F182BAC6F";
S634_RECORDS:=[
rec(k:=15648,first:=3,last:=200,unitFirst:=1,unitLast:=198,order:=49152,autOrder:=1572864,parity:=3,classes:=200,raw:=9830400,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1915),
rec(k:=15649,first:=1,last:=132,unitFirst:=199,unitLast:=330,order:=49152,autOrder:=1572864,parity:=3,classes:=132,raw:=6488064,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1414),
rec(k:=15650,first:=1,last:=180,unitFirst:=331,unitLast:=510,order:=49152,autOrder:=1572864,parity:=3,classes:=180,raw:=8847360,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=2346),
rec(k:=15651,first:=1,last:=276,unitFirst:=511,unitLast:=786,order:=49152,autOrder:=1572864,parity:=3,classes:=276,raw:=13565952,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1589),
rec(k:=15652,first:=1,last:=129,unitFirst:=787,unitLast:=915,order:=49152,autOrder:=1572864,parity:=3,classes:=200,raw:=9830400,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=2173)
];
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard634_v7_gpt56sol.g");
