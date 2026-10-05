# Exact wrapper for sealed degree-24 seed workload shard252.
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD252_SEGMENT001_UNIT1_1831_POSTVERIFY_V7_GPT56SOL.txt";
STOP_AFTER_UNIT:=fail;
INTERNAL_GUARD_MS:=1320000; START_UNIT:=1;
INITIAL_COUNTERS:=[0,0,0,0,0,0,0,0,0,0,0,0];
PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";
PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0;
PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";
CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD252_CHECKPOINT_GPT56SOL.txt";
CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD252_CHECKPOINT_TMP_GPT56SOL.txt";
EXPECTED_PROFILE_SHA256:="1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2";
EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard252_v7_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="305579D4F07308E7AFDE3F4406C8F233DCBB96FF5DB8072DB2D36F4AE7CD8DE2";
S252_RECORDS:=[
rec(k:=13736,first:=177,last:=512,unitFirst:=1,unitLast:=336,order:=24576,autOrder:=393216,parity:=15,classes:=512,raw:=12582912,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=2259),
rec(k:=13737,first:=1,last:=292,unitFirst:=337,unitLast:=628,order:=24576,autOrder:=2359296,parity:=15,classes:=292,raw:=7176192,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1388),
rec(k:=13738,first:=1,last:=640,unitFirst:=629,unitLast:=1268,order:=24576,autOrder:=786432,parity:=15,classes:=640,raw:=15728640,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=2278),
rec(k:=13740,first:=1,last:=64,unitFirst:=1269,unitLast:=1332,order:=24576,autOrder:=786432,parity:=1,classes:=64,raw:=1572864,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1374),
rec(k:=13741,first:=1,last:=72,unitFirst:=1333,unitLast:=1404,order:=24576,autOrder:=1572864,parity:=1,classes:=72,raw:=1769472,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1794),
rec(k:=13742,first:=1,last:=427,unitFirst:=1405,unitLast:=1831,order:=24576,autOrder:=1572864,parity:=1,classes:=712,raw:=17498112,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=2265)
];
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard252_v7_gpt56sol.g");
