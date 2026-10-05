# Exact wrapper for sealed degree-24 seed workload shard336.
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD336_SEGMENT001_UNIT1_915_POSTVERIFY_V7_GPT56SOL.txt";
STOP_AFTER_UNIT:=fail;
INTERNAL_GUARD_MS:=1320000; START_UNIT:=1;
INITIAL_COUNTERS:=[0,0,0,0,0,0,0,0,0,0,0,0];
PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";
PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0;
PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";
CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD336_CHECKPOINT_GPT56SOL.txt";
CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD336_CHECKPOINT_TMP_GPT56SOL.txt";
EXPECTED_PROFILE_SHA256:="1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2";
EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard336_v7_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="08AB5B572316D8E9F9F4C91C8A464055A81C34D4F18863253D323616B49D7F56";
S336_RECORDS:=[
rec(k:=14788,first:=330,last:=368,unitFirst:=1,unitLast:=39,order:=49152,autOrder:=6291456,parity:=3,classes:=368,raw:=18087936,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=2432),
rec(k:=14789,first:=1,last:=200,unitFirst:=40,unitLast:=239,order:=49152,autOrder:=1572864,parity:=15,classes:=200,raw:=9830400,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=869),
rec(k:=14790,first:=1,last:=72,unitFirst:=240,unitLast:=311,order:=49152,autOrder:=786432,parity:=15,classes:=72,raw:=3538944,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=941),
rec(k:=14791,first:=1,last:=48,unitFirst:=312,unitLast:=359,order:=49152,autOrder:=393216,parity:=7,classes:=48,raw:=2359296,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=922),
rec(k:=14792,first:=1,last:=48,unitFirst:=360,unitLast:=407,order:=49152,autOrder:=393216,parity:=7,classes:=48,raw:=2359296,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=871),
rec(k:=14793,first:=1,last:=48,unitFirst:=408,unitLast:=455,order:=49152,autOrder:=393216,parity:=7,classes:=48,raw:=2359296,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1033),
rec(k:=14794,first:=1,last:=120,unitFirst:=456,unitLast:=575,order:=49152,autOrder:=786432,parity:=7,classes:=120,raw:=5898240,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=956),
rec(k:=14795,first:=1,last:=120,unitFirst:=576,unitLast:=695,order:=49152,autOrder:=786432,parity:=7,classes:=120,raw:=5898240,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=812),
rec(k:=14796,first:=1,last:=48,unitFirst:=696,unitLast:=743,order:=49152,autOrder:=393216,parity:=7,classes:=48,raw:=2359296,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1098),
rec(k:=14797,first:=1,last:=172,unitFirst:=744,unitLast:=915,order:=49152,autOrder:=6291456,parity:=1,classes:=368,raw:=18087936,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1644)
];
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard336_v7_gpt56sol.g");
