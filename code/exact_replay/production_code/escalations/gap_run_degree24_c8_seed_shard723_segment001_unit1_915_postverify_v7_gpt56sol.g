# Exact wrapper for sealed degree-24 seed workload shard723.
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD723_SEGMENT001_UNIT1_915_POSTVERIFY_V7_GPT56SOL.txt";
STOP_AFTER_UNIT:=fail;
INTERNAL_GUARD_MS:=1320000; START_UNIT:=1;
INITIAL_COUNTERS:=[0,0,0,0,0,0,0,0,0,0,0,0];
PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";
PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0;
PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";
CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD723_CHECKPOINT_GPT56SOL.txt";
CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD723_CHECKPOINT_TMP_GPT56SOL.txt";
EXPECTED_PROFILE_SHA256:="1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2";
EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard723_v7_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="C6E9218B40BBD98AC8C9EDD7E2D89877DFE2FBA2DA245C5E70148515C7505FE1";
S723_RECORDS:=[
rec(k:=15765,first:=4,last:=172,unitFirst:=1,unitLast:=169,order:=49152,autOrder:=6291456,parity:=1,classes:=172,raw:=8454144,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=2079),
rec(k:=15766,first:=1,last:=208,unitFirst:=170,unitLast:=377,order:=49152,autOrder:=6291456,parity:=1,classes:=208,raw:=10223616,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=4556),
rec(k:=15767,first:=1,last:=538,unitFirst:=378,unitLast:=915,order:=49152,autOrder:=3145728,parity:=1,classes:=1224,raw:=60162048,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=3108)
];
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard723_v7_gpt56sol.g");
