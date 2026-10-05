# Exact wrapper for sealed degree-24 seed workload shard577.
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD577_SEGMENT001_UNIT1_915_POSTVERIFY_V7_GPT56SOL.txt";
STOP_AFTER_UNIT:=fail;
INTERNAL_GUARD_MS:=1320000; START_UNIT:=1;
INITIAL_COUNTERS:=[0,0,0,0,0,0,0,0,0,0,0,0];
PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";
PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0;
PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";
CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD577_CHECKPOINT_GPT56SOL.txt";
CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD577_CHECKPOINT_TMP_GPT56SOL.txt";
EXPECTED_PROFILE_SHA256:="1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2";
EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard577_v7_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="E0BB2A00202CBFB9612DB371F228D3198E9AAED7F178F19156B0C678F2F85699";
S577_RECORDS:=[
rec(k:=15498,first:=262,last:=406,unitFirst:=1,unitLast:=145,order:=49152,autOrder:=6291456,parity:=7,classes:=406,raw:=19955712,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1190),
rec(k:=15499,first:=1,last:=224,unitFirst:=146,unitLast:=369,order:=49152,autOrder:=1572864,parity:=7,classes:=224,raw:=11010048,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1939),
rec(k:=15500,first:=1,last:=132,unitFirst:=370,unitLast:=501,order:=49152,autOrder:=9437184,parity:=7,classes:=132,raw:=6488064,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1912),
rec(k:=15501,first:=1,last:=242,unitFirst:=502,unitLast:=743,order:=49152,autOrder:=9437184,parity:=7,classes:=242,raw:=11894784,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1709),
rec(k:=15502,first:=1,last:=172,unitFirst:=744,unitLast:=915,order:=49152,autOrder:=3145728,parity:=7,classes:=334,raw:=16416768,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=2468)
];
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard577_v7_gpt56sol.g");
