# Exact wrapper for sealed degree-24 seed workload shard131.
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD131_SEGMENT001_UNIT1_1831_POSTVERIFY_V7_GPT56SOL.txt";
STOP_AFTER_UNIT:=fail;
INTERNAL_GUARD_MS:=1320000; START_UNIT:=1;
INITIAL_COUNTERS:=[0,0,0,0,0,0,0,0,0,0,0,0];
PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";
PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0;
PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";
CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD131_CHECKPOINT_GPT56SOL.txt";
CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD131_CHECKPOINT_TMP_GPT56SOL.txt";
EXPECTED_PROFILE_SHA256:="1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2";
EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard131_v7_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="7611DC30AEFF0826FF370A351A2AB91B888B57CC034FC986198F604D5321EACD";
S131_RECORDS:=[
rec(k:=12858,first:=120,last:=142,unitFirst:=1,unitLast:=23,order:=24576,autOrder:=6291456,parity:=1,classes:=142,raw:=3489792,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1437),
rec(k:=12861,first:=1,last:=160,unitFirst:=24,unitLast:=183,order:=24576,autOrder:=393216,parity:=15,classes:=160,raw:=3932160,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=720),
rec(k:=12862,first:=1,last:=160,unitFirst:=184,unitLast:=343,order:=24576,autOrder:=393216,parity:=7,classes:=160,raw:=3932160,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=811),
rec(k:=12863,first:=1,last:=160,unitFirst:=344,unitLast:=503,order:=24576,autOrder:=393216,parity:=7,classes:=160,raw:=3932160,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=763),
rec(k:=12864,first:=1,last:=160,unitFirst:=504,unitLast:=663,order:=24576,autOrder:=393216,parity:=7,classes:=160,raw:=3932160,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=775),
rec(k:=12865,first:=1,last:=48,unitFirst:=664,unitLast:=711,order:=24576,autOrder:=196608,parity:=7,classes:=48,raw:=1179648,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=715),
rec(k:=12866,first:=1,last:=48,unitFirst:=712,unitLast:=759,order:=24576,autOrder:=196608,parity:=7,classes:=48,raw:=1179648,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=743),
rec(k:=12867,first:=1,last:=48,unitFirst:=760,unitLast:=807,order:=24576,autOrder:=196608,parity:=7,classes:=48,raw:=1179648,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=752),
rec(k:=12868,first:=1,last:=48,unitFirst:=808,unitLast:=855,order:=24576,autOrder:=196608,parity:=7,classes:=48,raw:=1179648,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=676),
rec(k:=12869,first:=1,last:=144,unitFirst:=856,unitLast:=999,order:=24576,autOrder:=196608,parity:=7,classes:=144,raw:=3538944,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=981),
rec(k:=12870,first:=1,last:=134,unitFirst:=1000,unitLast:=1133,order:=24576,autOrder:=4718592,parity:=7,classes:=134,raw:=3293184,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1004),
rec(k:=12871,first:=1,last:=144,unitFirst:=1134,unitLast:=1277,order:=24576,autOrder:=196608,parity:=15,classes:=144,raw:=3538944,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1016),
rec(k:=12872,first:=1,last:=112,unitFirst:=1278,unitLast:=1389,order:=24576,autOrder:=786432,parity:=7,classes:=112,raw:=2752512,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1082),
rec(k:=12873,first:=1,last:=64,unitFirst:=1390,unitLast:=1453,order:=24576,autOrder:=393216,parity:=3,classes:=64,raw:=1572864,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=868),
rec(k:=12874,first:=1,last:=64,unitFirst:=1454,unitLast:=1517,order:=24576,autOrder:=1179648,parity:=3,classes:=64,raw:=1572864,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=942),
rec(k:=12875,first:=1,last:=144,unitFirst:=1518,unitLast:=1661,order:=24576,autOrder:=196608,parity:=7,classes:=144,raw:=3538944,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=983),
rec(k:=12876,first:=1,last:=170,unitFirst:=1662,unitLast:=1831,order:=24576,autOrder:=1572864,parity:=7,classes:=176,raw:=4325376,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1290)
];
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard131_v7_gpt56sol.g");
