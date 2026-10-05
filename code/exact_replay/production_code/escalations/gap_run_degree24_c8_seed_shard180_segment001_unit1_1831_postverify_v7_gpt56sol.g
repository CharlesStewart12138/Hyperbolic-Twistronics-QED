# Exact wrapper for sealed degree-24 seed workload shard180.
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD180_SEGMENT001_UNIT1_1831_POSTVERIFY_V7_GPT56SOL.txt";
STOP_AFTER_UNIT:=fail;
INTERNAL_GUARD_MS:=1320000; START_UNIT:=1;
INITIAL_COUNTERS:=[0,0,0,0,0,0,0,0,0,0,0,0];
PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";
PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0;
PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";
CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD180_CHECKPOINT_GPT56SOL.txt";
CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD180_CHECKPOINT_TMP_GPT56SOL.txt";
EXPECTED_PROFILE_SHA256:="1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2";
EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard180_v7_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="795E08A35477AF365D9D6390D4FAD7279EF5656308D2891FD80304B1117FF351";
S180_RECORDS:=[
rec(k:=13311,first:=30,last:=128,unitFirst:=1,unitLast:=99,order:=24576,autOrder:=393216,parity:=7,classes:=128,raw:=3145728,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1409),
rec(k:=13312,first:=1,last:=512,unitFirst:=100,unitLast:=611,order:=24576,autOrder:=393216,parity:=7,classes:=512,raw:=12582912,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1957),
rec(k:=13313,first:=1,last:=120,unitFirst:=612,unitLast:=731,order:=24576,autOrder:=786432,parity:=3,classes:=120,raw:=2949120,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1433),
rec(k:=13314,first:=1,last:=64,unitFirst:=732,unitLast:=795,order:=24576,autOrder:=393216,parity:=3,classes:=64,raw:=1572864,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1016),
rec(k:=13316,first:=1,last:=124,unitFirst:=796,unitLast:=919,order:=24576,autOrder:=786432,parity:=3,classes:=124,raw:=3047424,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1063),
rec(k:=13317,first:=1,last:=204,unitFirst:=920,unitLast:=1123,order:=24576,autOrder:=1572864,parity:=7,classes:=204,raw:=5013504,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1313),
rec(k:=13318,first:=1,last:=124,unitFirst:=1124,unitLast:=1247,order:=24576,autOrder:=786432,parity:=3,classes:=124,raw:=3047424,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=955),
rec(k:=13319,first:=1,last:=32,unitFirst:=1248,unitLast:=1279,order:=24576,autOrder:=393216,parity:=3,classes:=32,raw:=786432,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=882),
rec(k:=13320,first:=1,last:=64,unitFirst:=1280,unitLast:=1343,order:=24576,autOrder:=393216,parity:=3,classes:=64,raw:=1572864,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1076),
rec(k:=13321,first:=1,last:=64,unitFirst:=1344,unitLast:=1407,order:=24576,autOrder:=393216,parity:=3,classes:=64,raw:=1572864,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1210),
rec(k:=13322,first:=1,last:=32,unitFirst:=1408,unitLast:=1439,order:=24576,autOrder:=393216,parity:=3,classes:=32,raw:=786432,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=934),
rec(k:=13323,first:=1,last:=180,unitFirst:=1440,unitLast:=1619,order:=24576,autOrder:=786432,parity:=3,classes:=180,raw:=4423680,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1349),
rec(k:=13325,first:=1,last:=162,unitFirst:=1620,unitLast:=1781,order:=24576,autOrder:=1572864,parity:=7,classes:=162,raw:=3981312,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1569),
rec(k:=13326,first:=1,last:=50,unitFirst:=1782,unitLast:=1831,order:=24576,autOrder:=786432,parity:=3,classes:=128,raw:=3145728,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1128)
];
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard180_v7_gpt56sol.g");
