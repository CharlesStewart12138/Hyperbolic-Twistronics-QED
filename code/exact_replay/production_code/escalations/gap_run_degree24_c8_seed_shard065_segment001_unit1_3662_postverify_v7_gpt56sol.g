# Exact wrapper for sealed degree-24 seed workload shard065.
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD065_SEGMENT001_UNIT1_3662_POSTVERIFY_V7_GPT56SOL.txt";
STOP_AFTER_UNIT:=fail;
INTERNAL_GUARD_MS:=1320000; START_UNIT:=1;
INITIAL_COUNTERS:=[0,0,0,0,0,0,0,0,0,0,0,0];
PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";
PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0;
PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";
CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD065_CHECKPOINT_GPT56SOL.txt";
CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD065_CHECKPOINT_TMP_GPT56SOL.txt";
EXPECTED_PROFILE_SHA256:="1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2";
EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard065_v7_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="090FD36F4634DA778C850547DD0400548375548069DEE5BDC7D4D6A49FA2E9EC";
S065_RECORDS:=[
rec(k:=11152,first:=234,last:=326,unitFirst:=1,unitLast:=93,order:=12288,autOrder:=786432,parity:=7,classes:=326,raw:=4005888,method:="pc",representation:="legacy_sealed_pc",pcOrder:=12288,profileMs:=3094),
rec(k:=11153,first:=1,last:=184,unitFirst:=94,unitLast:=277,order:=12288,autOrder:=1572864,parity:=7,classes:=184,raw:=2260992,method:="pc",representation:="legacy_sealed_pc",pcOrder:=12288,profileMs:=3621),
rec(k:=11154,first:=1,last:=344,unitFirst:=278,unitLast:=621,order:=12288,autOrder:=1572864,parity:=7,classes:=344,raw:=4227072,method:="pc",representation:="legacy_sealed_pc",pcOrder:=12288,profileMs:=2816),
rec(k:=11155,first:=1,last:=344,unitFirst:=622,unitLast:=965,order:=12288,autOrder:=1572864,parity:=7,classes:=344,raw:=4227072,method:="pc",representation:="legacy_sealed_pc",pcOrder:=12288,profileMs:=3084),
rec(k:=11156,first:=1,last:=496,unitFirst:=966,unitLast:=1461,order:=12288,autOrder:=3145728,parity:=7,classes:=496,raw:=6094848,method:="pc",representation:="legacy_sealed_pc",pcOrder:=12288,profileMs:=4050),
rec(k:=11157,first:=1,last:=112,unitFirst:=1462,unitLast:=1573,order:=12288,autOrder:=786432,parity:=7,classes:=112,raw:=1376256,method:="pc",representation:="legacy_sealed_pc",pcOrder:=12288,profileMs:=4992),
rec(k:=11159,first:=1,last:=256,unitFirst:=1574,unitLast:=1829,order:=12288,autOrder:=786432,parity:=7,classes:=256,raw:=3145728,method:="pc",representation:="legacy_sealed_pc",pcOrder:=12288,profileMs:=2788),
rec(k:=11160,first:=1,last:=288,unitFirst:=1830,unitLast:=2117,order:=12288,autOrder:=1572864,parity:=7,classes:=288,raw:=3538944,method:="pc",representation:="legacy_sealed_pc",pcOrder:=12288,profileMs:=1931),
rec(k:=11161,first:=1,last:=720,unitFirst:=2118,unitLast:=2837,order:=12288,autOrder:=3145728,parity:=7,classes:=720,raw:=8847360,method:="pc",representation:="legacy_sealed_pc",pcOrder:=12288,profileMs:=2725),
rec(k:=11162,first:=1,last:=344,unitFirst:=2838,unitLast:=3181,order:=12288,autOrder:=1572864,parity:=7,classes:=344,raw:=4227072,method:="pc",representation:="legacy_sealed_pc",pcOrder:=12288,profileMs:=2214),
rec(k:=11163,first:=1,last:=270,unitFirst:=3182,unitLast:=3451,order:=12288,autOrder:=4718592,parity:=7,classes:=270,raw:=3317760,method:="pc",representation:="legacy_sealed_pc",pcOrder:=12288,profileMs:=1317),
rec(k:=11164,first:=1,last:=211,unitFirst:=3452,unitLast:=3662,order:=12288,autOrder:=3145728,parity:=7,classes:=604,raw:=7421952,method:="pc",representation:="legacy_sealed_pc",pcOrder:=12288,profileMs:=2625)
];
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard065_v7_gpt56sol.g");
