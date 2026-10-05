# Exact wrapper for sealed degree-24 seed workload shard154.
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD154_SEGMENT001_UNIT1_1831_POSTVERIFY_V7_GPT56SOL.txt";
STOP_AFTER_UNIT:=fail;
INTERNAL_GUARD_MS:=1320000; START_UNIT:=1;
INITIAL_COUNTERS:=[0,0,0,0,0,0,0,0,0,0,0,0];
PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";
PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0;
PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";
CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD154_CHECKPOINT_GPT56SOL.txt";
CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD154_CHECKPOINT_TMP_GPT56SOL.txt";
EXPECTED_PROFILE_SHA256:="1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2";
EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard154_v7_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="2A0CF81BC5EB5211D0D32598BA86D8FEA3FE79F96294BEDD179691363A3EB0F2";
S154_RECORDS:=[
rec(k:=13063,first:=38,last:=239,unitFirst:=1,unitLast:=202,order:=24576,autOrder:=3145728,parity:=3,classes:=239,raw:=5873664,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1914),
rec(k:=13064,first:=1,last:=137,unitFirst:=203,unitLast:=339,order:=24576,autOrder:=1572864,parity:=1,classes:=137,raw:=3366912,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=826),
rec(k:=13065,first:=1,last:=160,unitFirst:=340,unitLast:=499,order:=24576,autOrder:=786432,parity:=1,classes:=160,raw:=3932160,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1166),
rec(k:=13066,first:=1,last:=88,unitFirst:=500,unitLast:=587,order:=24576,autOrder:=393216,parity:=3,classes:=88,raw:=2162688,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1353),
rec(k:=13067,first:=1,last:=96,unitFirst:=588,unitLast:=683,order:=24576,autOrder:=786432,parity:=3,classes:=96,raw:=2359296,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1479),
rec(k:=13068,first:=1,last:=96,unitFirst:=684,unitLast:=779,order:=24576,autOrder:=196608,parity:=3,classes:=96,raw:=2359296,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1181),
rec(k:=13069,first:=1,last:=178,unitFirst:=780,unitLast:=957,order:=24576,autOrder:=1572864,parity:=1,classes:=178,raw:=4374528,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=949),
rec(k:=13070,first:=1,last:=172,unitFirst:=958,unitLast:=1129,order:=24576,autOrder:=786432,parity:=7,classes:=172,raw:=4227072,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1451),
rec(k:=13071,first:=1,last:=40,unitFirst:=1130,unitLast:=1169,order:=24576,autOrder:=98304,parity:=3,classes:=40,raw:=983040,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=656),
rec(k:=13072,first:=1,last:=344,unitFirst:=1170,unitLast:=1513,order:=24576,autOrder:=786432,parity:=15,classes:=344,raw:=8454144,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=2043),
rec(k:=13073,first:=1,last:=176,unitFirst:=1514,unitLast:=1689,order:=24576,autOrder:=786432,parity:=15,classes:=176,raw:=4325376,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1069),
rec(k:=13074,first:=1,last:=136,unitFirst:=1690,unitLast:=1825,order:=24576,autOrder:=1572864,parity:=1,classes:=136,raw:=3342336,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1968),
rec(k:=13075,first:=1,last:=6,unitFirst:=1826,unitLast:=1831,order:=24576,autOrder:=393216,parity:=15,classes:=384,raw:=9437184,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1854)
];
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard154_v7_gpt56sol.g");
