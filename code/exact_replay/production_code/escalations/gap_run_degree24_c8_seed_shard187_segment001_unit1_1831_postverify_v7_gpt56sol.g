# Exact wrapper for sealed degree-24 seed workload shard187.
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD187_SEGMENT001_UNIT1_1831_POSTVERIFY_V7_GPT56SOL.txt";
STOP_AFTER_UNIT:=fail;
INTERNAL_GUARD_MS:=1320000; START_UNIT:=1;
INITIAL_COUNTERS:=[0,0,0,0,0,0,0,0,0,0,0,0];
PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";
PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0;
PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";
CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD187_CHECKPOINT_GPT56SOL.txt";
CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD187_CHECKPOINT_TMP_GPT56SOL.txt";
EXPECTED_PROFILE_SHA256:="1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2";
EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard187_v7_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="C1FE581E572664F9FAF4E8DAB172B1902205D39A65A3B04D4C13978E295AA81F";
S187_RECORDS:=[
rec(k:=13380,first:=556,last:=640,unitFirst:=1,unitLast:=85,order:=24576,autOrder:=393216,parity:=15,classes:=640,raw:=15728640,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1415),
rec(k:=13381,first:=1,last:=128,unitFirst:=86,unitLast:=213,order:=24576,autOrder:=786432,parity:=15,classes:=128,raw:=3145728,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1087),
rec(k:=13382,first:=1,last:=220,unitFirst:=214,unitLast:=433,order:=24576,autOrder:=786432,parity:=15,classes:=220,raw:=5406720,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=995),
rec(k:=13383,first:=1,last:=48,unitFirst:=434,unitLast:=481,order:=24576,autOrder:=393216,parity:=15,classes:=48,raw:=1179648,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=885),
rec(k:=13384,first:=1,last:=148,unitFirst:=482,unitLast:=629,order:=24576,autOrder:=9437184,parity:=15,classes:=148,raw:=3637248,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=809),
rec(k:=13385,first:=1,last:=745,unitFirst:=630,unitLast:=1374,order:=24576,autOrder:=1572864,parity:=15,classes:=745,raw:=18309120,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1849),
rec(k:=13386,first:=1,last:=156,unitFirst:=1375,unitLast:=1530,order:=24576,autOrder:=786432,parity:=15,classes:=156,raw:=3833856,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=965),
rec(k:=13387,first:=1,last:=288,unitFirst:=1531,unitLast:=1818,order:=24576,autOrder:=393216,parity:=15,classes:=288,raw:=7077888,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=706),
rec(k:=13388,first:=1,last:=13,unitFirst:=1819,unitLast:=1831,order:=24576,autOrder:=786432,parity:=15,classes:=800,raw:=19660800,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=2472)
];
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard187_v7_gpt56sol.g");
