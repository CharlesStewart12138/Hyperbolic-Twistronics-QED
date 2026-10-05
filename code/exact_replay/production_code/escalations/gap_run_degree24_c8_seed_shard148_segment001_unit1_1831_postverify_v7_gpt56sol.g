# Exact wrapper for sealed degree-24 seed workload shard148.
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD148_SEGMENT001_UNIT1_1831_POSTVERIFY_V7_GPT56SOL.txt";
STOP_AFTER_UNIT:=fail;
INTERNAL_GUARD_MS:=1320000; START_UNIT:=1;
INITIAL_COUNTERS:=[0,0,0,0,0,0,0,0,0,0,0,0];
PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";
PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0;
PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";
CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD148_CHECKPOINT_GPT56SOL.txt";
CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD148_CHECKPOINT_TMP_GPT56SOL.txt";
EXPECTED_PROFILE_SHA256:="1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2";
EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard148_v7_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="463E9899DAE5BD7EAFAFDB9D4B630AB9B9E0E7A5262B6AA0BFDCB5587D2082B2";
S148_RECORDS:=[
rec(k:=13017,first:=273,last:=278,unitFirst:=1,unitLast:=6,order:=24576,autOrder:=1572864,parity:=1,classes:=278,raw:=6832128,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1268),
rec(k:=13018,first:=1,last:=160,unitFirst:=7,unitLast:=166,order:=24576,autOrder:=786432,parity:=1,classes:=160,raw:=3932160,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=920),
rec(k:=13019,first:=1,last:=176,unitFirst:=167,unitLast:=342,order:=24576,autOrder:=786432,parity:=7,classes:=176,raw:=4325376,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1874),
rec(k:=13020,first:=1,last:=137,unitFirst:=343,unitLast:=479,order:=24576,autOrder:=1572864,parity:=1,classes:=137,raw:=3366912,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=752),
rec(k:=13021,first:=1,last:=174,unitFirst:=480,unitLast:=653,order:=24576,autOrder:=786432,parity:=3,classes:=174,raw:=4276224,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1363),
rec(k:=13022,first:=1,last:=162,unitFirst:=654,unitLast:=815,order:=24576,autOrder:=1572864,parity:=7,classes:=162,raw:=3981312,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1484),
rec(k:=13023,first:=1,last:=128,unitFirst:=816,unitLast:=943,order:=24576,autOrder:=786432,parity:=3,classes:=128,raw:=3145728,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1334),
rec(k:=13024,first:=1,last:=92,unitFirst:=944,unitLast:=1035,order:=24576,autOrder:=786432,parity:=3,classes:=92,raw:=2260992,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1022),
rec(k:=13025,first:=1,last:=124,unitFirst:=1036,unitLast:=1159,order:=24576,autOrder:=786432,parity:=3,classes:=124,raw:=3047424,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1121),
rec(k:=13026,first:=1,last:=137,unitFirst:=1160,unitLast:=1296,order:=24576,autOrder:=1572864,parity:=1,classes:=137,raw:=3366912,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1076),
rec(k:=13027,first:=1,last:=136,unitFirst:=1297,unitLast:=1432,order:=24576,autOrder:=786432,parity:=3,classes:=136,raw:=3342336,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1207),
rec(k:=13028,first:=1,last:=128,unitFirst:=1433,unitLast:=1560,order:=24576,autOrder:=196608,parity:=15,classes:=128,raw:=3145728,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1083),
rec(k:=13029,first:=1,last:=128,unitFirst:=1561,unitLast:=1688,order:=24576,autOrder:=393216,parity:=3,classes:=128,raw:=3145728,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1467),
rec(k:=13030,first:=1,last:=143,unitFirst:=1689,unitLast:=1831,order:=24576,autOrder:=1572864,parity:=15,classes:=752,raw:=18481152,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=2084)
];
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard148_v7_gpt56sol.g");
