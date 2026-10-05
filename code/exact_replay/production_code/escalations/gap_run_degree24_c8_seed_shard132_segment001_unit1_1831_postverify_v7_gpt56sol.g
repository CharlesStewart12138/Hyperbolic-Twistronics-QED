# Exact wrapper for sealed degree-24 seed workload shard132.
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD132_SEGMENT001_UNIT1_1831_POSTVERIFY_V7_GPT56SOL.txt";
STOP_AFTER_UNIT:=fail;
INTERNAL_GUARD_MS:=1320000; START_UNIT:=1;
INITIAL_COUNTERS:=[0,0,0,0,0,0,0,0,0,0,0,0];
PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";
PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0;
PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";
CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD132_CHECKPOINT_GPT56SOL.txt";
CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD132_CHECKPOINT_TMP_GPT56SOL.txt";
EXPECTED_PROFILE_SHA256:="1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2";
EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard132_v7_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="31809B4D8DFAF9189667AFD54D1E0D77EC0D5FECFFE85EC2FC6746A8EBD6E29A";
S132_RECORDS:=[
rec(k:=12876,first:=171,last:=176,unitFirst:=1,unitLast:=6,order:=24576,autOrder:=1572864,parity:=7,classes:=176,raw:=4325376,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1290),
rec(k:=12877,first:=1,last:=64,unitFirst:=7,unitLast:=70,order:=24576,autOrder:=393216,parity:=3,classes:=64,raw:=1572864,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1020),
rec(k:=12878,first:=1,last:=204,unitFirst:=71,unitLast:=274,order:=24576,autOrder:=1572864,parity:=7,classes:=204,raw:=5013504,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1182),
rec(k:=12879,first:=1,last:=290,unitFirst:=275,unitLast:=564,order:=24576,autOrder:=1572864,parity:=7,classes:=290,raw:=7127040,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1321),
rec(k:=12880,first:=1,last:=162,unitFirst:=565,unitLast:=726,order:=24576,autOrder:=4718592,parity:=7,classes:=162,raw:=3981312,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1234),
rec(k:=12881,first:=1,last:=64,unitFirst:=727,unitLast:=790,order:=24576,autOrder:=393216,parity:=3,classes:=64,raw:=1572864,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=880),
rec(k:=12882,first:=1,last:=262,unitFirst:=791,unitLast:=1052,order:=24576,autOrder:=1572864,parity:=7,classes:=262,raw:=6438912,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=775),
rec(k:=12883,first:=1,last:=123,unitFirst:=1053,unitLast:=1175,order:=24576,autOrder:=786432,parity:=7,classes:=123,raw:=3022848,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=812),
rec(k:=12884,first:=1,last:=16,unitFirst:=1176,unitLast:=1191,order:=24576,autOrder:=196608,parity:=15,classes:=16,raw:=393216,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=725),
rec(k:=12885,first:=1,last:=32,unitFirst:=1192,unitLast:=1223,order:=24576,autOrder:=393216,parity:=7,classes:=32,raw:=786432,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=870),
rec(k:=12886,first:=1,last:=80,unitFirst:=1224,unitLast:=1303,order:=24576,autOrder:=393216,parity:=7,classes:=80,raw:=1966080,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=678),
rec(k:=12887,first:=1,last:=176,unitFirst:=1304,unitLast:=1479,order:=24576,autOrder:=1572864,parity:=7,classes:=176,raw:=4325376,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=850),
rec(k:=12888,first:=1,last:=204,unitFirst:=1480,unitLast:=1683,order:=24576,autOrder:=1572864,parity:=7,classes:=204,raw:=5013504,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=716),
rec(k:=12889,first:=1,last:=32,unitFirst:=1684,unitLast:=1715,order:=24576,autOrder:=393216,parity:=3,classes:=32,raw:=786432,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=792),
rec(k:=12890,first:=1,last:=116,unitFirst:=1716,unitLast:=1831,order:=24576,autOrder:=393216,parity:=3,classes:=128,raw:=3145728,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=980)
];
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard132_v7_gpt56sol.g");
