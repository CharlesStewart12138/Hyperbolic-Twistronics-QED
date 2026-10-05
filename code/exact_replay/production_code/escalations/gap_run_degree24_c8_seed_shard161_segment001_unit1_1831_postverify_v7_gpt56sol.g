# Exact wrapper for sealed degree-24 seed workload shard161.
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD161_SEGMENT001_UNIT1_1831_POSTVERIFY_V7_GPT56SOL.txt";
STOP_AFTER_UNIT:=fail;
INTERNAL_GUARD_MS:=1320000; START_UNIT:=1;
INITIAL_COUNTERS:=[0,0,0,0,0,0,0,0,0,0,0,0];
PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";
PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0;
PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";
CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD161_CHECKPOINT_GPT56SOL.txt";
CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD161_CHECKPOINT_TMP_GPT56SOL.txt";
EXPECTED_PROFILE_SHA256:="1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2";
EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard161_v7_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="16DBEEE3CE40995ADD6AFE1FD3BE6D406598926831CD803B86561C6B5A293F77";
S161_RECORDS:=[
rec(k:=13140,first:=47,last:=403,unitFirst:=1,unitLast:=357,order:=24576,autOrder:=12582912,parity:=15,classes:=403,raw:=9904128,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=3255),
rec(k:=13141,first:=1,last:=32,unitFirst:=358,unitLast:=389,order:=24576,autOrder:=786432,parity:=7,classes:=32,raw:=786432,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1653),
rec(k:=13142,first:=1,last:=420,unitFirst:=390,unitLast:=809,order:=24576,autOrder:=786432,parity:=7,classes:=420,raw:=10321920,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=2454),
rec(k:=13143,first:=1,last:=40,unitFirst:=810,unitLast:=849,order:=24576,autOrder:=393216,parity:=7,classes:=40,raw:=983040,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=955),
rec(k:=13144,first:=1,last:=272,unitFirst:=850,unitLast:=1121,order:=24576,autOrder:=393216,parity:=7,classes:=272,raw:=6684672,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1082),
rec(k:=13145,first:=1,last:=152,unitFirst:=1122,unitLast:=1273,order:=24576,autOrder:=1572864,parity:=7,classes:=152,raw:=3735552,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1094),
rec(k:=13146,first:=1,last:=140,unitFirst:=1274,unitLast:=1413,order:=24576,autOrder:=1572864,parity:=7,classes:=140,raw:=3440640,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=2017),
rec(k:=13147,first:=1,last:=418,unitFirst:=1414,unitLast:=1831,order:=24576,autOrder:=3145728,parity:=7,classes:=743,raw:=18259968,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=2471)
];
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard161_v7_gpt56sol.g");
