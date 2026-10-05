# Exact wrapper for sealed degree-24 seed workload shard255.
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD255_SEGMENT001_UNIT1_1831_POSTVERIFY_V7_GPT56SOL.txt";
STOP_AFTER_UNIT:=fail;
INTERNAL_GUARD_MS:=1320000; START_UNIT:=1;
INITIAL_COUNTERS:=[0,0,0,0,0,0,0,0,0,0,0,0];
PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";
PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0;
PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";
CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD255_CHECKPOINT_GPT56SOL.txt";
CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD255_CHECKPOINT_TMP_GPT56SOL.txt";
EXPECTED_PROFILE_SHA256:="1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2";
EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard255_v7_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="207C09781F511AB4308AD7EF7BE2BBF54871A71DB3DC0DA58DA23DEC1FDE040A";
S255_RECORDS:=[
rec(k:=13749,first:=186,last:=476,unitFirst:=1,unitLast:=291,order:=24576,autOrder:=786432,parity:=1,classes:=476,raw:=11698176,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=936),
rec(k:=13750,first:=1,last:=212,unitFirst:=292,unitLast:=503,order:=24576,autOrder:=9437184,parity:=1,classes:=212,raw:=5210112,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=977),
rec(k:=13751,first:=1,last:=144,unitFirst:=504,unitLast:=647,order:=24576,autOrder:=1572864,parity:=1,classes:=144,raw:=3538944,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=947),
rec(k:=13752,first:=1,last:=212,unitFirst:=648,unitLast:=859,order:=24576,autOrder:=9437184,parity:=1,classes:=212,raw:=5210112,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1167),
rec(k:=13753,first:=1,last:=137,unitFirst:=860,unitLast:=996,order:=24576,autOrder:=1572864,parity:=1,classes:=137,raw:=3366912,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=758),
rec(k:=13754,first:=1,last:=60,unitFirst:=997,unitLast:=1056,order:=24576,autOrder:=393216,parity:=1,classes:=60,raw:=1474560,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=711),
rec(k:=13755,first:=1,last:=137,unitFirst:=1057,unitLast:=1193,order:=24576,autOrder:=1572864,parity:=1,classes:=137,raw:=3366912,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=684),
rec(k:=13756,first:=1,last:=336,unitFirst:=1194,unitLast:=1529,order:=24576,autOrder:=196608,parity:=7,classes:=336,raw:=8257536,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1149),
rec(k:=13757,first:=1,last:=302,unitFirst:=1530,unitLast:=1831,order:=24576,autOrder:=196608,parity:=7,classes:=336,raw:=8257536,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1434)
];
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard255_v7_gpt56sol.g");
