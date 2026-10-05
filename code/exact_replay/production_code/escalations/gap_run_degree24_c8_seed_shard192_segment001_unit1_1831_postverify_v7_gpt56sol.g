# Exact wrapper for sealed degree-24 seed workload shard192.
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD192_SEGMENT001_UNIT1_1831_POSTVERIFY_V7_GPT56SOL.txt";
STOP_AFTER_UNIT:=fail;
INTERNAL_GUARD_MS:=1320000; START_UNIT:=1;
INITIAL_COUNTERS:=[0,0,0,0,0,0,0,0,0,0,0,0];
PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";
PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0;
PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";
CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD192_CHECKPOINT_GPT56SOL.txt";
CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD192_CHECKPOINT_TMP_GPT56SOL.txt";
EXPECTED_PROFILE_SHA256:="1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2";
EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard192_v7_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="839EB9455735ECDAF0A420411A0380AC10F1404DE26EB0292209601CD3F82471";
S192_RECORDS:=[
rec(k:=13408,first:=630,last:=816,unitFirst:=1,unitLast:=187,order:=24576,autOrder:=1572864,parity:=7,classes:=816,raw:=20054016,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=2431),
rec(k:=13409,first:=1,last:=812,unitFirst:=188,unitLast:=999,order:=24576,autOrder:=1572864,parity:=7,classes:=812,raw:=19955712,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=2017),
rec(k:=13410,first:=1,last:=120,unitFirst:=1000,unitLast:=1119,order:=24576,autOrder:=786432,parity:=7,classes:=120,raw:=2949120,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1948),
rec(k:=13411,first:=1,last:=128,unitFirst:=1120,unitLast:=1247,order:=24576,autOrder:=196608,parity:=15,classes:=128,raw:=3145728,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1021),
rec(k:=13412,first:=1,last:=584,unitFirst:=1248,unitLast:=1831,order:=24576,autOrder:=786432,parity:=15,classes:=840,raw:=20643840,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=2028)
];
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard192_v7_gpt56sol.g");
