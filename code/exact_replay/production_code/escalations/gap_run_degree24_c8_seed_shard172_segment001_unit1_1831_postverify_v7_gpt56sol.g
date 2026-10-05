# Exact wrapper for sealed degree-24 seed workload shard172.
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD172_SEGMENT001_UNIT1_1831_POSTVERIFY_V7_GPT56SOL.txt";
STOP_AFTER_UNIT:=fail;
INTERNAL_GUARD_MS:=1320000; START_UNIT:=1;
INITIAL_COUNTERS:=[0,0,0,0,0,0,0,0,0,0,0,0];
PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";
PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0;
PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";
CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD172_CHECKPOINT_GPT56SOL.txt";
CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD172_CHECKPOINT_TMP_GPT56SOL.txt";
EXPECTED_PROFILE_SHA256:="1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2";
EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard172_v7_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="138C302405AFF4648807D9A17F4EC430C46243E9E0C81036A06938B3FC66ED7A";
S172_RECORDS:=[
rec(k:=13232,first:=240,last:=347,unitFirst:=1,unitLast:=108,order:=24576,autOrder:=6291456,parity:=15,classes:=347,raw:=8527872,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1696),
rec(k:=13233,first:=1,last:=78,unitFirst:=109,unitLast:=186,order:=24576,autOrder:=2359296,parity:=3,classes:=78,raw:=1916928,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1359),
rec(k:=13234,first:=1,last:=148,unitFirst:=187,unitLast:=334,order:=24576,autOrder:=9437184,parity:=15,classes:=148,raw:=3637248,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1019),
rec(k:=13235,first:=1,last:=64,unitFirst:=335,unitLast:=398,order:=24576,autOrder:=1179648,parity:=3,classes:=64,raw:=1572864,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1235),
rec(k:=13236,first:=1,last:=66,unitFirst:=399,unitLast:=464,order:=24576,autOrder:=4718592,parity:=7,classes:=66,raw:=1622016,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1641),
rec(k:=13237,first:=1,last:=110,unitFirst:=465,unitLast:=574,order:=24576,autOrder:=2359296,parity:=3,classes:=110,raw:=2703360,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1555),
rec(k:=13238,first:=1,last:=355,unitFirst:=575,unitLast:=929,order:=24576,autOrder:=18874368,parity:=15,classes:=355,raw:=8724480,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1702),
rec(k:=13239,first:=1,last:=112,unitFirst:=930,unitLast:=1041,order:=24576,autOrder:=786432,parity:=3,classes:=112,raw:=2752512,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=2656),
rec(k:=13240,first:=1,last:=238,unitFirst:=1042,unitLast:=1279,order:=24576,autOrder:=3145728,parity:=3,classes:=238,raw:=5849088,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=2389),
rec(k:=13241,first:=1,last:=226,unitFirst:=1280,unitLast:=1505,order:=24576,autOrder:=3145728,parity:=3,classes:=226,raw:=5554176,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=2766),
rec(k:=13242,first:=1,last:=174,unitFirst:=1506,unitLast:=1679,order:=24576,autOrder:=9437184,parity:=3,classes:=174,raw:=4276224,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1637),
rec(k:=13243,first:=1,last:=48,unitFirst:=1680,unitLast:=1727,order:=24576,autOrder:=2359296,parity:=3,classes:=48,raw:=1179648,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=2331),
rec(k:=13244,first:=1,last:=104,unitFirst:=1728,unitLast:=1831,order:=24576,autOrder:=9437184,parity:=3,classes:=154,raw:=3784704,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=2265)
];
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard172_v7_gpt56sol.g");
