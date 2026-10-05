# Exact wrapper for sealed degree-24 seed workload shard206.
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD206_SEGMENT001_UNIT1_1831_POSTVERIFY_V7_GPT56SOL.txt";
STOP_AFTER_UNIT:=fail;
INTERNAL_GUARD_MS:=1320000; START_UNIT:=1;
INITIAL_COUNTERS:=[0,0,0,0,0,0,0,0,0,0,0,0];
PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";
PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0;
PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";
CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD206_CHECKPOINT_GPT56SOL.txt";
CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD206_CHECKPOINT_TMP_GPT56SOL.txt";
EXPECTED_PROFILE_SHA256:="1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2";
EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard206_v7_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="DD34F54CBDFEE4BFFCE37135F9295DBC2CD0365874662C13EECDCB7501BDA1B6";
S206_RECORDS:=[
rec(k:=13474,first:=260,last:=370,unitFirst:=1,unitLast:=111,order:=24576,autOrder:=1572864,parity:=7,classes:=370,raw:=9093120,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1514),
rec(k:=13475,first:=1,last:=336,unitFirst:=112,unitLast:=447,order:=24576,autOrder:=393216,parity:=3,classes:=336,raw:=8257536,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=2315),
rec(k:=13476,first:=1,last:=32,unitFirst:=448,unitLast:=479,order:=24576,autOrder:=393216,parity:=3,classes:=32,raw:=786432,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=847),
rec(k:=13477,first:=1,last:=152,unitFirst:=480,unitLast:=631,order:=24576,autOrder:=1572864,parity:=7,classes:=152,raw:=3735552,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1539),
rec(k:=13480,first:=1,last:=160,unitFirst:=632,unitLast:=791,order:=24576,autOrder:=393216,parity:=3,classes:=160,raw:=3932160,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1621),
rec(k:=13481,first:=1,last:=164,unitFirst:=792,unitLast:=955,order:=24576,autOrder:=393216,parity:=3,classes:=164,raw:=4030464,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1801),
rec(k:=13482,first:=1,last:=32,unitFirst:=956,unitLast:=987,order:=24576,autOrder:=786432,parity:=3,classes:=32,raw:=786432,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1205),
rec(k:=13483,first:=1,last:=688,unitFirst:=988,unitLast:=1675,order:=24576,autOrder:=786432,parity:=7,classes:=688,raw:=16908288,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1730),
rec(k:=13484,first:=1,last:=156,unitFirst:=1676,unitLast:=1831,order:=24576,autOrder:=196608,parity:=3,classes:=208,raw:=5111808,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=936)
];
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard206_v7_gpt56sol.g");
