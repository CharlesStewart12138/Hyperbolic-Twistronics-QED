# Exact wrapper for sealed degree-24 seed workload shard147.
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD147_SEGMENT002_UNIT657_1831_POSTVERIFY_V7_GPT56SOL.txt";
STOP_AFTER_UNIT:=fail;
INTERNAL_GUARD_MS:=1320000; START_UNIT:=657;
INITIAL_COUNTERS:=[656,16121856,656,13,808960,404544,103936,31232,0,0,0,0];
PREVIOUS_CHECKPOINT_SHA256:="3a88cb419d2bc80254a3c28dc64c324eaf243c140ab0f25ea1e293c0a54217bb";
PREVIOUS_OUTPUT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD147_SEGMENT001_UNIT1_1831_POSTVERIFY_V7_GPT56SOL.txt"; PREVIOUS_OUTPUT_PREFIX_BYTES:=491105;
PREVIOUS_OUTPUT_PREFIX_SHA256:="0cd48e00cd213a25fa3624bce383535ac2c5d998a8140164b5fcce3f2db401e7";
CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD147_CHECKPOINT_GPT56SOL.txt";
CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD147_CHECKPOINT_TMP_GPT56SOL.txt";
EXPECTED_PROFILE_SHA256:="1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2";
EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard147_v7_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="1C84632CBC5400537A5BFE0B49EBA868A138D17C1622E876DD925C06D8D968B8";
S147_RECORDS:=[
rec(k:=13010,first:=281,last:=392,unitFirst:=1,unitLast:=112,order:=24576,autOrder:=1572864,parity:=3,classes:=392,raw:=9633792,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1513),
rec(k:=13011,first:=1,last:=32,unitFirst:=113,unitLast:=144,order:=24576,autOrder:=393216,parity:=3,classes:=32,raw:=786432,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1078),
rec(k:=13012,first:=1,last:=116,unitFirst:=145,unitLast:=260,order:=24576,autOrder:=393216,parity:=3,classes:=116,raw:=2850816,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=2219),
rec(k:=13013,first:=1,last:=750,unitFirst:=261,unitLast:=1010,order:=24576,autOrder:=1572864,parity:=7,classes:=750,raw:=18432000,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=2380),
rec(k:=13014,first:=1,last:=277,unitFirst:=1011,unitLast:=1287,order:=24576,autOrder:=3145728,parity:=1,classes:=277,raw:=6807552,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=942),
rec(k:=13015,first:=1,last:=128,unitFirst:=1288,unitLast:=1415,order:=24576,autOrder:=393216,parity:=3,classes:=128,raw:=3145728,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=940),
rec(k:=13016,first:=1,last:=144,unitFirst:=1416,unitLast:=1559,order:=24576,autOrder:=1572864,parity:=1,classes:=144,raw:=3538944,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=892),
rec(k:=13017,first:=1,last:=272,unitFirst:=1560,unitLast:=1831,order:=24576,autOrder:=1572864,parity:=1,classes:=278,raw:=6832128,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1268)
];
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard147_v7_gpt56sol.g");
