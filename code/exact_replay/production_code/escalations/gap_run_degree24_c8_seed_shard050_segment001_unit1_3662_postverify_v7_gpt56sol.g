# Exact wrapper for sealed degree-24 seed workload shard050.
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD050_SEGMENT001_UNIT1_3662_POSTVERIFY_V7_GPT56SOL.txt";
STOP_AFTER_UNIT:=fail;
INTERNAL_GUARD_MS:=1320000; START_UNIT:=1;
INITIAL_COUNTERS:=[0,0,0,0,0,0,0,0,0,0,0,0];
PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";
PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0;
PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";
CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD050_CHECKPOINT_GPT56SOL.txt";
CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD050_CHECKPOINT_TMP_GPT56SOL.txt";
EXPECTED_PROFILE_SHA256:="1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2";
EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard050_v7_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="D3742629C5739CC1174F02330A08F26C0653E1BE267765B445C16A031426D2D8";
S050_RECORDS:=[
rec(k:=10802,first:=13,last:=440,unitFirst:=1,unitLast:=428,order:=12288,autOrder:=786432,parity:=3,classes:=440,raw:=5406720,method:="pc",representation:="legacy_sealed_pc",pcOrder:=12288,profileMs:=1667),
rec(k:=10803,first:=1,last:=160,unitFirst:=429,unitLast:=588,order:=12288,autOrder:=1572864,parity:=3,classes:=160,raw:=1966080,method:="pc",representation:="legacy_sealed_pc",pcOrder:=12288,profileMs:=1478),
rec(k:=10804,first:=1,last:=256,unitFirst:=589,unitLast:=844,order:=12288,autOrder:=786432,parity:=3,classes:=256,raw:=3145728,method:="pc",representation:="legacy_sealed_pc",pcOrder:=12288,profileMs:=1703),
rec(k:=10805,first:=1,last:=96,unitFirst:=845,unitLast:=940,order:=12288,autOrder:=786432,parity:=3,classes:=96,raw:=1179648,method:="pc",representation:="legacy_sealed_pc",pcOrder:=12288,profileMs:=1191),
rec(k:=10806,first:=1,last:=472,unitFirst:=941,unitLast:=1412,order:=12288,autOrder:=786432,parity:=3,classes:=472,raw:=5799936,method:="pc",representation:="legacy_sealed_pc",pcOrder:=12288,profileMs:=1889),
rec(k:=10807,first:=1,last:=64,unitFirst:=1413,unitLast:=1476,order:=12288,autOrder:=196608,parity:=3,classes:=64,raw:=786432,method:="pc",representation:="legacy_sealed_pc",pcOrder:=12288,profileMs:=1094),
rec(k:=10808,first:=1,last:=176,unitFirst:=1477,unitLast:=1652,order:=12288,autOrder:=786432,parity:=7,classes:=176,raw:=2162688,method:="pc",representation:="legacy_sealed_pc",pcOrder:=12288,profileMs:=1337),
rec(k:=10809,first:=1,last:=288,unitFirst:=1653,unitLast:=1940,order:=12288,autOrder:=196608,parity:=3,classes:=288,raw:=3538944,method:="pc",representation:="legacy_sealed_pc",pcOrder:=12288,profileMs:=996),
rec(k:=10810,first:=1,last:=64,unitFirst:=1941,unitLast:=2004,order:=12288,autOrder:=393216,parity:=3,classes:=64,raw:=786432,method:="pc",representation:="legacy_sealed_pc",pcOrder:=12288,profileMs:=946),
rec(k:=10811,first:=1,last:=64,unitFirst:=2005,unitLast:=2068,order:=12288,autOrder:=196608,parity:=3,classes:=64,raw:=786432,method:="pc",representation:="legacy_sealed_pc",pcOrder:=12288,profileMs:=867),
rec(k:=10812,first:=1,last:=288,unitFirst:=2069,unitLast:=2356,order:=12288,autOrder:=196608,parity:=3,classes:=288,raw:=3538944,method:="pc",representation:="legacy_sealed_pc",pcOrder:=12288,profileMs:=1179),
rec(k:=10813,first:=1,last:=360,unitFirst:=2357,unitLast:=2716,order:=12288,autOrder:=393216,parity:=3,classes:=360,raw:=4423680,method:="pc",representation:="legacy_sealed_pc",pcOrder:=12288,profileMs:=1353),
rec(k:=10814,first:=1,last:=624,unitFirst:=2717,unitLast:=3340,order:=12288,autOrder:=786432,parity:=7,classes:=624,raw:=7667712,method:="pc",representation:="legacy_sealed_pc",pcOrder:=12288,profileMs:=2116),
rec(k:=10815,first:=1,last:=84,unitFirst:=3341,unitLast:=3424,order:=12288,autOrder:=786432,parity:=7,classes:=84,raw:=1032192,method:="pc",representation:="legacy_sealed_pc",pcOrder:=12288,profileMs:=1264),
rec(k:=10816,first:=1,last:=176,unitFirst:=3425,unitLast:=3600,order:=12288,autOrder:=393216,parity:=3,classes:=176,raw:=2162688,method:="pc",representation:="legacy_sealed_pc",pcOrder:=12288,profileMs:=1229),
rec(k:=10817,first:=1,last:=62,unitFirst:=3601,unitLast:=3662,order:=12288,autOrder:=786432,parity:=3,classes:=120,raw:=1474560,method:="pc",representation:="legacy_sealed_pc",pcOrder:=12288,profileMs:=1321)
];
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard050_v7_gpt56sol.g");
