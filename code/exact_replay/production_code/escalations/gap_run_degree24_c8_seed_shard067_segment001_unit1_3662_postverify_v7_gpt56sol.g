# Exact wrapper for sealed degree-24 seed workload shard067.
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD067_SEGMENT001_UNIT1_3662_POSTVERIFY_V7_GPT56SOL.txt";
STOP_AFTER_UNIT:=fail;
INTERNAL_GUARD_MS:=1320000; START_UNIT:=1;
INITIAL_COUNTERS:=[0,0,0,0,0,0,0,0,0,0,0,0];
PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";
PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0;
PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";
CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD067_CHECKPOINT_GPT56SOL.txt";
CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD067_CHECKPOINT_TMP_GPT56SOL.txt";
EXPECTED_PROFILE_SHA256:="1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2";
EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard067_v7_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="7ACC59692998B3B824963FB106A5E1805F7CC28950CDF9E53363DF4B864DAE79";
S067_RECORDS:=[
rec(k:=11188,first:=102,last:=280,unitFirst:=1,unitLast:=179,order:=12288,autOrder:=196608,parity:=7,classes:=280,raw:=3440640,method:="pc",representation:="legacy_sealed_pc",pcOrder:=12288,profileMs:=815),
rec(k:=11189,first:=1,last:=64,unitFirst:=180,unitLast:=243,order:=12288,autOrder:=98304,parity:=7,classes:=64,raw:=786432,method:="pc",representation:="legacy_sealed_pc",pcOrder:=12288,profileMs:=1021),
rec(k:=11190,first:=1,last:=64,unitFirst:=244,unitLast:=307,order:=12288,autOrder:=98304,parity:=7,classes:=64,raw:=786432,method:="pc",representation:="legacy_sealed_pc",pcOrder:=12288,profileMs:=1034),
rec(k:=11191,first:=1,last:=64,unitFirst:=308,unitLast:=371,order:=12288,autOrder:=98304,parity:=7,classes:=64,raw:=786432,method:="pc",representation:="legacy_sealed_pc",pcOrder:=12288,profileMs:=969),
rec(k:=11192,first:=1,last:=64,unitFirst:=372,unitLast:=435,order:=12288,autOrder:=98304,parity:=7,classes:=64,raw:=786432,method:="pc",representation:="legacy_sealed_pc",pcOrder:=12288,profileMs:=1256),
rec(k:=11193,first:=1,last:=224,unitFirst:=436,unitLast:=659,order:=12288,autOrder:=196608,parity:=7,classes:=224,raw:=2752512,method:="pc",representation:="legacy_sealed_pc",pcOrder:=12288,profileMs:=1035),
rec(k:=11194,first:=1,last:=280,unitFirst:=660,unitLast:=939,order:=12288,autOrder:=196608,parity:=7,classes:=280,raw:=3440640,method:="pc",representation:="legacy_sealed_pc",pcOrder:=12288,profileMs:=1241),
rec(k:=11195,first:=1,last:=224,unitFirst:=940,unitLast:=1163,order:=12288,autOrder:=196608,parity:=7,classes:=224,raw:=2752512,method:="pc",representation:="legacy_sealed_pc",pcOrder:=12288,profileMs:=1056),
rec(k:=11196,first:=1,last:=280,unitFirst:=1164,unitLast:=1443,order:=12288,autOrder:=196608,parity:=7,classes:=280,raw:=3440640,method:="pc",representation:="legacy_sealed_pc",pcOrder:=12288,profileMs:=668),
rec(k:=11197,first:=1,last:=128,unitFirst:=1444,unitLast:=1571,order:=12288,autOrder:=98304,parity:=7,classes:=128,raw:=1572864,method:="pc",representation:="legacy_sealed_pc",pcOrder:=12288,profileMs:=903),
rec(k:=11198,first:=1,last:=320,unitFirst:=1572,unitLast:=1891,order:=12288,autOrder:=393216,parity:=7,classes:=320,raw:=3932160,method:="pc",representation:="legacy_sealed_pc",pcOrder:=12288,profileMs:=968),
rec(k:=11199,first:=1,last:=128,unitFirst:=1892,unitLast:=2019,order:=12288,autOrder:=98304,parity:=7,classes:=128,raw:=1572864,method:="pc",representation:="legacy_sealed_pc",pcOrder:=12288,profileMs:=897),
rec(k:=11200,first:=1,last:=320,unitFirst:=2020,unitLast:=2339,order:=12288,autOrder:=393216,parity:=7,classes:=320,raw:=3932160,method:="pc",representation:="legacy_sealed_pc",pcOrder:=12288,profileMs:=1329),
rec(k:=11201,first:=1,last:=384,unitFirst:=2340,unitLast:=2723,order:=12288,autOrder:=196608,parity:=7,classes:=384,raw:=4718592,method:="pc",representation:="legacy_sealed_pc",pcOrder:=12288,profileMs:=1007),
rec(k:=11202,first:=1,last:=256,unitFirst:=2724,unitLast:=2979,order:=12288,autOrder:=196608,parity:=7,classes:=256,raw:=3145728,method:="pc",representation:="legacy_sealed_pc",pcOrder:=12288,profileMs:=1161),
rec(k:=11203,first:=1,last:=384,unitFirst:=2980,unitLast:=3363,order:=12288,autOrder:=196608,parity:=7,classes:=384,raw:=4718592,method:="pc",representation:="legacy_sealed_pc",pcOrder:=12288,profileMs:=1025),
rec(k:=11204,first:=1,last:=256,unitFirst:=3364,unitLast:=3619,order:=12288,autOrder:=196608,parity:=7,classes:=256,raw:=3145728,method:="pc",representation:="legacy_sealed_pc",pcOrder:=12288,profileMs:=788),
rec(k:=11205,first:=1,last:=43,unitFirst:=3620,unitLast:=3662,order:=12288,autOrder:=786432,parity:=7,classes:=84,raw:=1032192,method:="pc",representation:="legacy_sealed_pc",pcOrder:=12288,profileMs:=978)
];
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard067_v7_gpt56sol.g");
