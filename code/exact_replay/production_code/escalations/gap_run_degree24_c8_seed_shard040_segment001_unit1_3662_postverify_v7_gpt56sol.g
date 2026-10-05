# Exact wrapper for sealed degree-24 seed workload shard040.
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD040_SEGMENT001_UNIT1_3662_POSTVERIFY_V7_GPT56SOL.txt";
STOP_AFTER_UNIT:=fail;
INTERNAL_GUARD_MS:=1320000; START_UNIT:=1;
INITIAL_COUNTERS:=[0,0,0,0,0,0,0,0,0,0,0,0];
PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";
PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0;
PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";
CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD040_CHECKPOINT_GPT56SOL.txt";
CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD040_CHECKPOINT_TMP_GPT56SOL.txt";
EXPECTED_PROFILE_SHA256:="1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2";
EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard040_v7_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="7AC7C6D70C20BAF917E7C769071E0A4B2E9BAFFCDA8A038303C7CF8B471169E9";
S040_RECORDS:=[
rec(k:=10573,first:=117,last:=547,unitFirst:=1,unitLast:=431,order:=12288,autOrder:=1572864,parity:=7,classes:=547,raw:=6721536,method:="pc",representation:="legacy_sealed_pc",pcOrder:=12288,profileMs:=1754),
rec(k:=10574,first:=1,last:=64,unitFirst:=432,unitLast:=495,order:=12288,autOrder:=98304,parity:=3,classes:=64,raw:=786432,method:="pc",representation:="legacy_sealed_pc",pcOrder:=12288,profileMs:=671),
rec(k:=10575,first:=1,last:=100,unitFirst:=496,unitLast:=595,order:=12288,autOrder:=786432,parity:=7,classes:=100,raw:=1228800,method:="pc",representation:="legacy_sealed_pc",pcOrder:=12288,profileMs:=1083),
rec(k:=10576,first:=1,last:=171,unitFirst:=596,unitLast:=766,order:=12288,autOrder:=1572864,parity:=3,classes:=171,raw:=2101248,method:="pc",representation:="legacy_sealed_pc",pcOrder:=12288,profileMs:=2347),
rec(k:=10577,first:=1,last:=96,unitFirst:=767,unitLast:=862,order:=12288,autOrder:=786432,parity:=3,classes:=96,raw:=1179648,method:="pc",representation:="legacy_sealed_pc",pcOrder:=12288,profileMs:=1901),
rec(k:=10579,first:=1,last:=256,unitFirst:=863,unitLast:=1118,order:=12288,autOrder:=786432,parity:=7,classes:=256,raw:=3145728,method:="pc",representation:="legacy_sealed_pc",pcOrder:=12288,profileMs:=3358),
rec(k:=10580,first:=1,last:=112,unitFirst:=1119,unitLast:=1230,order:=12288,autOrder:=786432,parity:=7,classes:=112,raw:=1376256,method:="pc",representation:="legacy_sealed_pc",pcOrder:=12288,profileMs:=3401),
rec(k:=10581,first:=1,last:=344,unitFirst:=1231,unitLast:=1574,order:=12288,autOrder:=1572864,parity:=7,classes:=344,raw:=4227072,method:="pc",representation:="legacy_sealed_pc",pcOrder:=12288,profileMs:=2496),
rec(k:=10582,first:=1,last:=112,unitFirst:=1575,unitLast:=1686,order:=12288,autOrder:=786432,parity:=7,classes:=112,raw:=1376256,method:="pc",representation:="legacy_sealed_pc",pcOrder:=12288,profileMs:=1965),
rec(k:=10583,first:=1,last:=344,unitFirst:=1687,unitLast:=2030,order:=12288,autOrder:=1572864,parity:=7,classes:=344,raw:=4227072,method:="pc",representation:="legacy_sealed_pc",pcOrder:=12288,profileMs:=2583),
rec(k:=10584,first:=1,last:=604,unitFirst:=2031,unitLast:=2634,order:=12288,autOrder:=3145728,parity:=7,classes:=604,raw:=7421952,method:="pc",representation:="legacy_sealed_pc",pcOrder:=12288,profileMs:=3184),
rec(k:=10585,first:=1,last:=112,unitFirst:=2635,unitLast:=2746,order:=12288,autOrder:=786432,parity:=7,classes:=112,raw:=1376256,method:="pc",representation:="legacy_sealed_pc",pcOrder:=12288,profileMs:=3612),
rec(k:=10586,first:=1,last:=184,unitFirst:=2747,unitLast:=2930,order:=12288,autOrder:=1572864,parity:=7,classes:=184,raw:=2260992,method:="pc",representation:="legacy_sealed_pc",pcOrder:=12288,profileMs:=3158),
rec(k:=10587,first:=1,last:=276,unitFirst:=2931,unitLast:=3206,order:=12288,autOrder:=3145728,parity:=7,classes:=276,raw:=3391488,method:="pc",representation:="legacy_sealed_pc",pcOrder:=12288,profileMs:=2645),
rec(k:=10588,first:=1,last:=120,unitFirst:=3207,unitLast:=3326,order:=12288,autOrder:=1572864,parity:=7,classes:=120,raw:=1474560,method:="pc",representation:="legacy_sealed_pc",pcOrder:=12288,profileMs:=2553),
rec(k:=10590,first:=1,last:=215,unitFirst:=3327,unitLast:=3541,order:=12288,autOrder:=786432,parity:=3,classes:=215,raw:=2641920,method:="pc",representation:="legacy_sealed_pc",pcOrder:=12288,profileMs:=3797),
rec(k:=10592,first:=1,last:=121,unitFirst:=3542,unitLast:=3662,order:=12288,autOrder:=786432,parity:=3,classes:=179,raw:=2199552,method:="pc",representation:="legacy_sealed_pc",pcOrder:=12288,profileMs:=1224)
];
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard040_v7_gpt56sol.g");
