# Exact wrapper for sealed degree-24 seed workload shard140.
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD140_SEGMENT001_UNIT1_1831_POSTVERIFY_V7_GPT56SOL.txt";
STOP_AFTER_UNIT:=fail;
INTERNAL_GUARD_MS:=1320000; START_UNIT:=1;
INITIAL_COUNTERS:=[0,0,0,0,0,0,0,0,0,0,0,0];
PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";
PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0;
PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";
CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD140_CHECKPOINT_GPT56SOL.txt";
CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD140_CHECKPOINT_TMP_GPT56SOL.txt";
EXPECTED_PROFILE_SHA256:="1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2";
EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard140_v7_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="D4A594D2E0974D5909343E8C20EFAD9507D24C46E443C95D8C8294CA790F1F39";
S140_RECORDS:=[
rec(k:=12956,first:=68,last:=128,unitFirst:=1,unitLast:=61,order:=24576,autOrder:=393216,parity:=3,classes:=128,raw:=3145728,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1169),
rec(k:=12957,first:=1,last:=277,unitFirst:=62,unitLast:=338,order:=24576,autOrder:=3145728,parity:=1,classes:=277,raw:=6807552,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=930),
rec(k:=12958,first:=1,last:=160,unitFirst:=339,unitLast:=498,order:=24576,autOrder:=786432,parity:=1,classes:=160,raw:=3932160,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=971),
rec(k:=12959,first:=1,last:=170,unitFirst:=499,unitLast:=668,order:=24576,autOrder:=3145728,parity:=3,classes:=170,raw:=4177920,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=2298),
rec(k:=12960,first:=1,last:=160,unitFirst:=669,unitLast:=828,order:=24576,autOrder:=786432,parity:=1,classes:=160,raw:=3932160,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1362),
rec(k:=12961,first:=1,last:=137,unitFirst:=829,unitLast:=965,order:=24576,autOrder:=1572864,parity:=1,classes:=137,raw:=3366912,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=858),
rec(k:=12962,first:=1,last:=396,unitFirst:=966,unitLast:=1361,order:=24576,autOrder:=3145728,parity:=1,classes:=396,raw:=9732096,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1600),
rec(k:=12963,first:=1,last:=128,unitFirst:=1362,unitLast:=1489,order:=24576,autOrder:=786432,parity:=7,classes:=128,raw:=3145728,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1161),
rec(k:=12964,first:=1,last:=72,unitFirst:=1490,unitLast:=1561,order:=24576,autOrder:=1572864,parity:=1,classes:=72,raw:=1769472,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1536),
rec(k:=12965,first:=1,last:=112,unitFirst:=1562,unitLast:=1673,order:=24576,autOrder:=3145728,parity:=1,classes:=112,raw:=2752512,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1780),
rec(k:=12966,first:=1,last:=158,unitFirst:=1674,unitLast:=1831,order:=24576,autOrder:=786432,parity:=1,classes:=160,raw:=3932160,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1368)
];
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard140_v7_gpt56sol.g");
