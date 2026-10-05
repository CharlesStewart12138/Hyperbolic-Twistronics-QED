# Exact wrapper for sealed degree-24 seed workload shard315.
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD315_SEGMENT001_UNIT1_1220_POSTVERIFY_V7_GPT56SOL.txt";
STOP_AFTER_UNIT:=fail;
INTERNAL_GUARD_MS:=1320000; START_UNIT:=1;
INITIAL_COUNTERS:=[0,0,0,0,0,0,0,0,0,0,0,0];
PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";
PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0;
PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";
CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD315_CHECKPOINT_GPT56SOL.txt";
CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD315_CHECKPOINT_TMP_GPT56SOL.txt";
EXPECTED_PROFILE_SHA256:="1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2";
EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard315_v7_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="73A39086ED20D52D24AC282E88172C5A0A467B15441322041D2CA5E9C281E975";
S315_RECORDS:=[
rec(k:=14303,first:=13,last:=40,unitFirst:=1,unitLast:=28,order:=36864,autOrder:=294912,parity:=7,classes:=40,raw:=1474560,method:="pc",representation:="pc_transport",pcOrder:=36864,profileMs:=621),
rec(k:=14304,first:=1,last:=40,unitFirst:=29,unitLast:=68,order:=36864,autOrder:=294912,parity:=3,classes:=40,raw:=1474560,method:="pc",representation:="pc_transport",pcOrder:=36864,profileMs:=751),
rec(k:=14305,first:=1,last:=68,unitFirst:=69,unitLast:=136,order:=36864,autOrder:=1179648,parity:=15,classes:=68,raw:=2506752,method:="pc",representation:="pc_transport",pcOrder:=36864,profileMs:=524),
rec(k:=14306,first:=1,last:=53,unitFirst:=137,unitLast:=189,order:=36864,autOrder:=589824,parity:=7,classes:=53,raw:=1953792,method:="pc",representation:="pc_transport",pcOrder:=36864,profileMs:=643),
rec(k:=14307,first:=1,last:=68,unitFirst:=190,unitLast:=257,order:=36864,autOrder:=1179648,parity:=7,classes:=68,raw:=2506752,method:="pc",representation:="pc_transport",pcOrder:=36864,profileMs:=538),
rec(k:=14308,first:=1,last:=42,unitFirst:=258,unitLast:=299,order:=36864,autOrder:=589824,parity:=7,classes:=42,raw:=1548288,method:="pc",representation:="pc_transport",pcOrder:=36864,profileMs:=484),
rec(k:=14309,first:=1,last:=42,unitFirst:=300,unitLast:=341,order:=36864,autOrder:=589824,parity:=3,classes:=42,raw:=1548288,method:="pc",representation:="pc_transport",pcOrder:=36864,profileMs:=527),
rec(k:=14310,first:=1,last:=176,unitFirst:=342,unitLast:=517,order:=36864,autOrder:=589824,parity:=7,classes:=176,raw:=6488064,method:="pc",representation:="pc_transport",pcOrder:=36864,profileMs:=660),
rec(k:=14311,first:=1,last:=68,unitFirst:=518,unitLast:=585,order:=36864,autOrder:=1179648,parity:=15,classes:=68,raw:=2506752,method:="pc",representation:="pc_transport",pcOrder:=36864,profileMs:=520),
rec(k:=14312,first:=1,last:=160,unitFirst:=586,unitLast:=745,order:=36864,autOrder:=294912,parity:=7,classes:=160,raw:=5898240,method:="pc",representation:="pc_transport",pcOrder:=36864,profileMs:=725),
rec(k:=14313,first:=1,last:=128,unitFirst:=746,unitLast:=873,order:=36864,autOrder:=147456,parity:=7,classes:=128,raw:=4718592,method:="pc",representation:="pc_transport",pcOrder:=36864,profileMs:=581),
rec(k:=14314,first:=1,last:=112,unitFirst:=874,unitLast:=985,order:=36864,autOrder:=294912,parity:=7,classes:=112,raw:=4128768,method:="pc",representation:="pc_transport",pcOrder:=36864,profileMs:=482),
rec(k:=14315,first:=1,last:=112,unitFirst:=986,unitLast:=1097,order:=36864,autOrder:=294912,parity:=7,classes:=112,raw:=4128768,method:="pc",representation:="pc_transport",pcOrder:=36864,profileMs:=428),
rec(k:=14316,first:=1,last:=123,unitFirst:=1098,unitLast:=1220,order:=36864,autOrder:=147456,parity:=7,classes:=128,raw:=4718592,method:="pc",representation:="pc_transport",pcOrder:=36864,profileMs:=493)
];
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard315_v7_gpt56sol.g");
