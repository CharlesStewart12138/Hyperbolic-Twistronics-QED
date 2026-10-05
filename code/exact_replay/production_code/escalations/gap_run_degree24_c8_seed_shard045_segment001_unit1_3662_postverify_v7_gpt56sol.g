# Exact wrapper for sealed degree-24 seed workload shard045.
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD045_SEGMENT001_UNIT1_3662_POSTVERIFY_V7_GPT56SOL.txt";
STOP_AFTER_UNIT:=fail;
INTERNAL_GUARD_MS:=1320000; START_UNIT:=1;
INITIAL_COUNTERS:=[0,0,0,0,0,0,0,0,0,0,0,0];
PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";
PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0;
PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";
CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD045_CHECKPOINT_GPT56SOL.txt";
CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD045_CHECKPOINT_TMP_GPT56SOL.txt";
EXPECTED_PROFILE_SHA256:="1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2";
EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard045_v7_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="38B2B9A073B55ACE2A0ED40E93F44C7562B754C1F4F2471F9FE6CDE7B30B80C9";
S045_RECORDS:=[
rec(k:=10710,first:=490,last:=764,unitFirst:=1,unitLast:=275,order:=12288,autOrder:=1572864,parity:=7,classes:=764,raw:=9388032,method:="pc",representation:="legacy_sealed_pc",pcOrder:=12288,profileMs:=2806),
rec(k:=10711,first:=1,last:=160,unitFirst:=276,unitLast:=435,order:=12288,autOrder:=1572864,parity:=3,classes:=160,raw:=1966080,method:="pc",representation:="legacy_sealed_pc",pcOrder:=12288,profileMs:=2096),
rec(k:=10712,first:=1,last:=128,unitFirst:=436,unitLast:=563,order:=12288,autOrder:=393216,parity:=3,classes:=128,raw:=1572864,method:="pc",representation:="legacy_sealed_pc",pcOrder:=12288,profileMs:=1779),
rec(k:=10713,first:=1,last:=80,unitFirst:=564,unitLast:=643,order:=12288,autOrder:=4718592,parity:=7,classes:=80,raw:=983040,method:="pc",representation:="legacy_sealed_pc",pcOrder:=12288,profileMs:=1261),
rec(k:=10714,first:=1,last:=352,unitFirst:=644,unitLast:=995,order:=12288,autOrder:=393216,parity:=3,classes:=352,raw:=4325376,method:="pc",representation:="legacy_sealed_pc",pcOrder:=12288,profileMs:=1589),
rec(k:=10715,first:=1,last:=224,unitFirst:=996,unitLast:=1219,order:=12288,autOrder:=1572864,parity:=3,classes:=224,raw:=2752512,method:="pc",representation:="legacy_sealed_pc",pcOrder:=12288,profileMs:=1272),
rec(k:=10716,first:=1,last:=290,unitFirst:=1220,unitLast:=1509,order:=12288,autOrder:=3145728,parity:=7,classes:=290,raw:=3563520,method:="pc",representation:="legacy_sealed_pc",pcOrder:=12288,profileMs:=1703),
rec(k:=10717,first:=1,last:=96,unitFirst:=1510,unitLast:=1605,order:=12288,autOrder:=786432,parity:=3,classes:=96,raw:=1179648,method:="pc",representation:="legacy_sealed_pc",pcOrder:=12288,profileMs:=1846),
rec(k:=10718,first:=1,last:=80,unitFirst:=1606,unitLast:=1685,order:=12288,autOrder:=393216,parity:=7,classes:=80,raw:=983040,method:="pc",representation:="legacy_sealed_pc",pcOrder:=12288,profileMs:=1453),
rec(k:=10719,first:=1,last:=280,unitFirst:=1686,unitLast:=1965,order:=12288,autOrder:=393216,parity:=7,classes:=280,raw:=3440640,method:="pc",representation:="legacy_sealed_pc",pcOrder:=12288,profileMs:=1742),
rec(k:=10720,first:=1,last:=790,unitFirst:=1966,unitLast:=2755,order:=12288,autOrder:=3145728,parity:=7,classes:=790,raw:=9707520,method:="pc",representation:="legacy_sealed_pc",pcOrder:=12288,profileMs:=2529),
rec(k:=10721,first:=1,last:=48,unitFirst:=2756,unitLast:=2803,order:=12288,autOrder:=98304,parity:=3,classes:=48,raw:=589824,method:="pc",representation:="legacy_sealed_pc",pcOrder:=12288,profileMs:=1001),
rec(k:=10722,first:=1,last:=114,unitFirst:=2804,unitLast:=2917,order:=12288,autOrder:=393216,parity:=3,classes:=114,raw:=1400832,method:="pc",representation:="legacy_sealed_pc",pcOrder:=12288,profileMs:=1824),
rec(k:=10723,first:=1,last:=20,unitFirst:=2918,unitLast:=2937,order:=12288,autOrder:=98304,parity:=3,classes:=20,raw:=245760,method:="pc",representation:="legacy_sealed_pc",pcOrder:=12288,profileMs:=626),
rec(k:=10725,first:=1,last:=326,unitFirst:=2938,unitLast:=3263,order:=12288,autOrder:=786432,parity:=7,classes:=326,raw:=4005888,method:="pc",representation:="legacy_sealed_pc",pcOrder:=12288,profileMs:=1637),
rec(k:=10726,first:=1,last:=100,unitFirst:=3264,unitLast:=3363,order:=12288,autOrder:=786432,parity:=7,classes:=100,raw:=1228800,method:="pc",representation:="legacy_sealed_pc",pcOrder:=12288,profileMs:=2658),
rec(k:=10727,first:=1,last:=270,unitFirst:=3364,unitLast:=3633,order:=12288,autOrder:=4718592,parity:=7,classes:=270,raw:=3317760,method:="pc",representation:="legacy_sealed_pc",pcOrder:=12288,profileMs:=1596),
rec(k:=10728,first:=1,last:=29,unitFirst:=3634,unitLast:=3662,order:=12288,autOrder:=786432,parity:=7,classes:=256,raw:=3145728,method:="pc",representation:="legacy_sealed_pc",pcOrder:=12288,profileMs:=2896)
];
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard045_v7_gpt56sol.g");
