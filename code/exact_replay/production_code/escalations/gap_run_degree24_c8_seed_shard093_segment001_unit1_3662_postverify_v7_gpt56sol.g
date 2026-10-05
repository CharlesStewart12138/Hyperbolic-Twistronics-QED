# Exact wrapper for sealed degree-24 seed workload shard093.
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD093_SEGMENT001_UNIT1_3662_POSTVERIFY_V7_GPT56SOL.txt";
STOP_AFTER_UNIT:=fail;
INTERNAL_GUARD_MS:=1320000; START_UNIT:=1;
INITIAL_COUNTERS:=[0,0,0,0,0,0,0,0,0,0,0,0];
PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";
PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0;
PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";
CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD093_CHECKPOINT_GPT56SOL.txt";
CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD093_CHECKPOINT_TMP_GPT56SOL.txt";
EXPECTED_PROFILE_SHA256:="1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2";
EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard093_v7_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="7CA17D2E1C971174C35A47DF666DB2A3E2CC0E2DED94E899EF903F07F2035A35";
S093_RECORDS:=[
rec(k:=11684,first:=210,last:=240,unitFirst:=1,unitLast:=31,order:=12288,autOrder:=196608,parity:=3,classes:=240,raw:=2949120,method:="pc",representation:="pc_transport",pcOrder:=12288,profileMs:=811),
rec(k:=11685,first:=1,last:=400,unitFirst:=32,unitLast:=431,order:=12288,autOrder:=196608,parity:=3,classes:=400,raw:=4915200,method:="pc",representation:="pc_transport",pcOrder:=12288,profileMs:=679),
rec(k:=11686,first:=1,last:=240,unitFirst:=432,unitLast:=671,order:=12288,autOrder:=196608,parity:=3,classes:=240,raw:=2949120,method:="pc",representation:="pc_transport",pcOrder:=12288,profileMs:=836),
rec(k:=11687,first:=1,last:=400,unitFirst:=672,unitLast:=1071,order:=12288,autOrder:=196608,parity:=3,classes:=400,raw:=4915200,method:="pc",representation:="pc_transport",pcOrder:=12288,profileMs:=796),
rec(k:=11688,first:=1,last:=64,unitFirst:=1072,unitLast:=1135,order:=12288,autOrder:=393216,parity:=3,classes:=64,raw:=786432,method:="pc",representation:="pc_transport",pcOrder:=12288,profileMs:=841),
rec(k:=11689,first:=1,last:=64,unitFirst:=1136,unitLast:=1199,order:=12288,autOrder:=196608,parity:=3,classes:=64,raw:=786432,method:="pc",representation:="pc_transport",pcOrder:=12288,profileMs:=645),
rec(k:=11690,first:=1,last:=192,unitFirst:=1200,unitLast:=1391,order:=12288,autOrder:=98304,parity:=3,classes:=192,raw:=2359296,method:="pc",representation:="pc_transport",pcOrder:=12288,profileMs:=812),
rec(k:=11691,first:=1,last:=192,unitFirst:=1392,unitLast:=1583,order:=12288,autOrder:=98304,parity:=3,classes:=192,raw:=2359296,method:="pc",representation:="pc_transport",pcOrder:=12288,profileMs:=618),
rec(k:=11692,first:=1,last:=320,unitFirst:=1584,unitLast:=1903,order:=12288,autOrder:=98304,parity:=3,classes:=320,raw:=3932160,method:="pc",representation:="pc_transport",pcOrder:=12288,profileMs:=1000),
rec(k:=11693,first:=1,last:=320,unitFirst:=1904,unitLast:=2223,order:=12288,autOrder:=98304,parity:=3,classes:=320,raw:=3932160,method:="pc",representation:="pc_transport",pcOrder:=12288,profileMs:=715),
rec(k:=11694,first:=1,last:=64,unitFirst:=2224,unitLast:=2287,order:=12288,autOrder:=196608,parity:=3,classes:=64,raw:=786432,method:="pc",representation:="pc_transport",pcOrder:=12288,profileMs:=1183),
rec(k:=11695,first:=1,last:=64,unitFirst:=2288,unitLast:=2351,order:=12288,autOrder:=196608,parity:=3,classes:=64,raw:=786432,method:="pc",representation:="pc_transport",pcOrder:=12288,profileMs:=1373),
rec(k:=11696,first:=1,last:=232,unitFirst:=2352,unitLast:=2583,order:=12288,autOrder:=393216,parity:=3,classes:=232,raw:=2850816,method:="pc",representation:="pc_transport",pcOrder:=12288,profileMs:=786),
rec(k:=11697,first:=1,last:=320,unitFirst:=2584,unitLast:=2903,order:=12288,autOrder:=196608,parity:=3,classes:=320,raw:=3932160,method:="pc",representation:="pc_transport",pcOrder:=12288,profileMs:=1030),
rec(k:=11698,first:=1,last:=306,unitFirst:=2904,unitLast:=3209,order:=12288,autOrder:=393216,parity:=3,classes:=306,raw:=3760128,method:="pc",representation:="pc_transport",pcOrder:=12288,profileMs:=977),
rec(k:=11699,first:=1,last:=306,unitFirst:=3210,unitLast:=3515,order:=12288,autOrder:=393216,parity:=3,classes:=306,raw:=3760128,method:="pc",representation:="pc_transport",pcOrder:=12288,profileMs:=1405),
rec(k:=11700,first:=1,last:=64,unitFirst:=3516,unitLast:=3579,order:=12288,autOrder:=393216,parity:=7,classes:=64,raw:=786432,method:="pc",representation:="pc_transport",pcOrder:=12288,profileMs:=458),
rec(k:=11701,first:=1,last:=80,unitFirst:=3580,unitLast:=3659,order:=12288,autOrder:=196608,parity:=3,classes:=80,raw:=983040,method:="pc",representation:="pc_transport",pcOrder:=12288,profileMs:=748),
rec(k:=11702,first:=1,last:=3,unitFirst:=3660,unitLast:=3662,order:=12288,autOrder:=196608,parity:=3,classes:=96,raw:=1179648,method:="pc",representation:="pc_transport",pcOrder:=12288,profileMs:=817)
];
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard093_v7_gpt56sol.g");
