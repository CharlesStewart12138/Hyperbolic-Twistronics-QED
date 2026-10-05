# Exact wrapper for sealed degree-24 seed workload shard052.
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD052_SEGMENT001_UNIT1_3662_POSTVERIFY_V7_GPT56SOL.txt";
STOP_AFTER_UNIT:=fail;
INTERNAL_GUARD_MS:=1320000; START_UNIT:=1;
INITIAL_COUNTERS:=[0,0,0,0,0,0,0,0,0,0,0,0];
PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";
PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0;
PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";
CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD052_CHECKPOINT_GPT56SOL.txt";
CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD052_CHECKPOINT_TMP_GPT56SOL.txt";
EXPECTED_PROFILE_SHA256:="1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2";
EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard052_v7_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="74E56506B1A0B5499510016857948A9BE32157B71F2ABA10417964282DD7956A";
S052_RECORDS:=[
rec(k:=10832,first:=541,last:=624,unitFirst:=1,unitLast:=84,order:=12288,autOrder:=786432,parity:=7,classes:=624,raw:=7667712,method:="pc",representation:="legacy_sealed_pc",pcOrder:=12288,profileMs:=1903),
rec(k:=10833,first:=1,last:=84,unitFirst:=85,unitLast:=168,order:=12288,autOrder:=786432,parity:=7,classes:=84,raw:=1032192,method:="pc",representation:="legacy_sealed_pc",pcOrder:=12288,profileMs:=2241),
rec(k:=10834,first:=1,last:=132,unitFirst:=169,unitLast:=300,order:=12288,autOrder:=786432,parity:=7,classes:=132,raw:=1622016,method:="pc",representation:="legacy_sealed_pc",pcOrder:=12288,profileMs:=1222),
rec(k:=10835,first:=1,last:=272,unitFirst:=301,unitLast:=572,order:=12288,autOrder:=393216,parity:=7,classes:=272,raw:=3342336,method:="pc",representation:="legacy_sealed_pc",pcOrder:=12288,profileMs:=942),
rec(k:=10836,first:=1,last:=72,unitFirst:=573,unitLast:=644,order:=12288,autOrder:=196608,parity:=3,classes:=72,raw:=884736,method:="pc",representation:="legacy_sealed_pc",pcOrder:=12288,profileMs:=1195),
rec(k:=10837,first:=1,last:=360,unitFirst:=645,unitLast:=1004,order:=12288,autOrder:=393216,parity:=3,classes:=360,raw:=4423680,method:="pc",representation:="legacy_sealed_pc",pcOrder:=12288,profileMs:=1844),
rec(k:=10838,first:=1,last:=72,unitFirst:=1005,unitLast:=1076,order:=12288,autOrder:=196608,parity:=3,classes:=72,raw:=884736,method:="pc",representation:="legacy_sealed_pc",pcOrder:=12288,profileMs:=1091),
rec(k:=10839,first:=1,last:=120,unitFirst:=1077,unitLast:=1196,order:=12288,autOrder:=786432,parity:=3,classes:=120,raw:=1474560,method:="pc",representation:="legacy_sealed_pc",pcOrder:=12288,profileMs:=3259),
rec(k:=10840,first:=1,last:=384,unitFirst:=1197,unitLast:=1580,order:=12288,autOrder:=393216,parity:=3,classes:=384,raw:=4718592,method:="pc",representation:="legacy_sealed_pc",pcOrder:=12288,profileMs:=4164),
rec(k:=10841,first:=1,last:=256,unitFirst:=1581,unitLast:=1836,order:=12288,autOrder:=196608,parity:=7,classes:=256,raw:=3145728,method:="pc",representation:="legacy_sealed_pc",pcOrder:=12288,profileMs:=1195),
rec(k:=10842,first:=1,last:=128,unitFirst:=1837,unitLast:=1964,order:=12288,autOrder:=98304,parity:=7,classes:=128,raw:=1572864,method:="pc",representation:="legacy_sealed_pc",pcOrder:=12288,profileMs:=1320),
rec(k:=10843,first:=1,last:=384,unitFirst:=1965,unitLast:=2348,order:=12288,autOrder:=196608,parity:=7,classes:=384,raw:=4718592,method:="pc",representation:="legacy_sealed_pc",pcOrder:=12288,profileMs:=1695),
rec(k:=10844,first:=1,last:=256,unitFirst:=2349,unitLast:=2604,order:=12288,autOrder:=196608,parity:=7,classes:=256,raw:=3145728,method:="pc",representation:="legacy_sealed_pc",pcOrder:=12288,profileMs:=1356),
rec(k:=10845,first:=1,last:=192,unitFirst:=2605,unitLast:=2796,order:=12288,autOrder:=786432,parity:=7,classes:=192,raw:=2359296,method:="pc",representation:="legacy_sealed_pc",pcOrder:=12288,profileMs:=1583),
rec(k:=10846,first:=1,last:=128,unitFirst:=2797,unitLast:=2924,order:=12288,autOrder:=98304,parity:=7,classes:=128,raw:=1572864,method:="pc",representation:="legacy_sealed_pc",pcOrder:=12288,profileMs:=1435),
rec(k:=10847,first:=1,last:=384,unitFirst:=2925,unitLast:=3308,order:=12288,autOrder:=196608,parity:=7,classes:=384,raw:=4718592,method:="pc",representation:="legacy_sealed_pc",pcOrder:=12288,profileMs:=1628),
rec(k:=10848,first:=1,last:=354,unitFirst:=3309,unitLast:=3662,order:=12288,autOrder:=393216,parity:=7,classes:=384,raw:=4718592,method:="pc",representation:="legacy_sealed_pc",pcOrder:=12288,profileMs:=1170)
];
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard052_v7_gpt56sol.g");
