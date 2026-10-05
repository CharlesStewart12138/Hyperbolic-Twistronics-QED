# Exact wrapper for sealed degree-24 seed workload shard048.
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD048_SEGMENT001_UNIT1_3662_POSTVERIFY_V7_GPT56SOL.txt";
STOP_AFTER_UNIT:=fail;
INTERNAL_GUARD_MS:=1320000; START_UNIT:=1;
INITIAL_COUNTERS:=[0,0,0,0,0,0,0,0,0,0,0,0];
PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";
PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0;
PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";
CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD048_CHECKPOINT_GPT56SOL.txt";
CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD048_CHECKPOINT_TMP_GPT56SOL.txt";
EXPECTED_PROFILE_SHA256:="1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2";
EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard048_v7_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="D408A3B86C0F375DC680B24661EB5CD8349CEF220F68A0116B6F6A918E1178DB";
S048_RECORDS:=[
rec(k:=10765,first:=70,last:=320,unitFirst:=1,unitLast:=251,order:=12288,autOrder:=786432,parity:=3,classes:=320,raw:=3932160,method:="pc",representation:="legacy_sealed_pc",pcOrder:=12288,profileMs:=1372),
rec(k:=10766,first:=1,last:=97,unitFirst:=252,unitLast:=348,order:=12288,autOrder:=393216,parity:=1,classes:=97,raw:=1191936,method:="pc",representation:="legacy_sealed_pc",pcOrder:=12288,profileMs:=841),
rec(k:=10768,first:=1,last:=544,unitFirst:=349,unitLast:=892,order:=12288,autOrder:=1572864,parity:=3,classes:=544,raw:=6684672,method:="pc",representation:="legacy_sealed_pc",pcOrder:=12288,profileMs:=1899),
rec(k:=10769,first:=1,last:=100,unitFirst:=893,unitLast:=992,order:=12288,autOrder:=786432,parity:=3,classes:=100,raw:=1228800,method:="pc",representation:="legacy_sealed_pc",pcOrder:=12288,profileMs:=1289),
rec(k:=10770,first:=1,last:=340,unitFirst:=993,unitLast:=1332,order:=12288,autOrder:=393216,parity:=7,classes:=340,raw:=4177920,method:="pc",representation:="legacy_sealed_pc",pcOrder:=12288,profileMs:=1368),
rec(k:=10771,first:=1,last:=246,unitFirst:=1333,unitLast:=1578,order:=12288,autOrder:=393216,parity:=7,classes:=246,raw:=3022848,method:="pc",representation:="legacy_sealed_pc",pcOrder:=12288,profileMs:=828),
rec(k:=10772,first:=1,last:=64,unitFirst:=1579,unitLast:=1642,order:=12288,autOrder:=393216,parity:=7,classes:=64,raw:=786432,method:="pc",representation:="legacy_sealed_pc",pcOrder:=12288,profileMs:=794),
rec(k:=10773,first:=1,last:=224,unitFirst:=1643,unitLast:=1866,order:=12288,autOrder:=196608,parity:=3,classes:=224,raw:=2752512,method:="pc",representation:="legacy_sealed_pc",pcOrder:=12288,profileMs:=1450),
rec(k:=10774,first:=1,last:=224,unitFirst:=1867,unitLast:=2090,order:=12288,autOrder:=196608,parity:=3,classes:=224,raw:=2752512,method:="pc",representation:="legacy_sealed_pc",pcOrder:=12288,profileMs:=737),
rec(k:=10775,first:=1,last:=64,unitFirst:=2091,unitLast:=2154,order:=12288,autOrder:=196608,parity:=3,classes:=64,raw:=786432,method:="pc",representation:="legacy_sealed_pc",pcOrder:=12288,profileMs:=1246),
rec(k:=10776,first:=1,last:=64,unitFirst:=2155,unitLast:=2218,order:=12288,autOrder:=196608,parity:=3,classes:=64,raw:=786432,method:="pc",representation:="legacy_sealed_pc",pcOrder:=12288,profileMs:=1377),
rec(k:=10777,first:=1,last:=554,unitFirst:=2219,unitLast:=2772,order:=12288,autOrder:=786432,parity:=7,classes:=554,raw:=6807552,method:="pc",representation:="legacy_sealed_pc",pcOrder:=12288,profileMs:=2497),
rec(k:=10778,first:=1,last:=246,unitFirst:=2773,unitLast:=3018,order:=12288,autOrder:=393216,parity:=7,classes:=246,raw:=3022848,method:="pc",representation:="legacy_sealed_pc",pcOrder:=12288,profileMs:=803),
rec(k:=10779,first:=1,last:=64,unitFirst:=3019,unitLast:=3082,order:=12288,autOrder:=393216,parity:=7,classes:=64,raw:=786432,method:="pc",representation:="legacy_sealed_pc",pcOrder:=12288,profileMs:=1172),
rec(k:=10780,first:=1,last:=166,unitFirst:=3083,unitLast:=3248,order:=12288,autOrder:=786432,parity:=7,classes:=166,raw:=2039808,method:="pc",representation:="legacy_sealed_pc",pcOrder:=12288,profileMs:=1854),
rec(k:=10781,first:=1,last:=48,unitFirst:=3249,unitLast:=3296,order:=12288,autOrder:=393216,parity:=3,classes:=48,raw:=589824,method:="pc",representation:="legacy_sealed_pc",pcOrder:=12288,profileMs:=1030),
rec(k:=10782,first:=1,last:=64,unitFirst:=3297,unitLast:=3360,order:=12288,autOrder:=196608,parity:=3,classes:=64,raw:=786432,method:="pc",representation:="legacy_sealed_pc",pcOrder:=12288,profileMs:=1545),
rec(k:=10783,first:=1,last:=302,unitFirst:=3361,unitLast:=3662,order:=12288,autOrder:=786432,parity:=7,classes:=554,raw:=6807552,method:="pc",representation:="legacy_sealed_pc",pcOrder:=12288,profileMs:=1853)
];
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard048_v7_gpt56sol.g");
