# Exact wrapper for sealed degree-24 seed workload shard223.
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD223_SEGMENT002_UNIT758_1831_POSTVERIFY_V7_GPT56SOL.txt";
STOP_AFTER_UNIT:=fail;
INTERNAL_GUARD_MS:=1320000; START_UNIT:=758;
INITIAL_COUNTERS:=[757,18604032,757,18,510400,432512,297152,88384,0,0,0,0];
PREVIOUS_CHECKPOINT_SHA256:="34935c93107dfba57b1cb10a12bdb64f5cc259b22658043025eacca406b93148";
PREVIOUS_OUTPUT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD223_SEGMENT001_UNIT1_1831_POSTVERIFY_V7_GPT56SOL.txt"; PREVIOUS_OUTPUT_PREFIX_BYTES:=568604;
PREVIOUS_OUTPUT_PREFIX_SHA256:="d5f143d093c78772368090b82363e090e3638318c7b5455bca4c53e7b677d85c";
CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD223_CHECKPOINT_GPT56SOL.txt";
CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD223_CHECKPOINT_TMP_GPT56SOL.txt";
EXPECTED_PROFILE_SHA256:="1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2";
EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard223_v7_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="024C474994FF8672965D3E99BF145E2B02401A59B86F426F5F885D51C664FF54";
S223_RECORDS:=[
rec(k:=13579,first:=48,last:=92,unitFirst:=1,unitLast:=45,order:=24576,autOrder:=393216,parity:=3,classes:=92,raw:=2260992,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=919),
rec(k:=13580,first:=1,last:=800,unitFirst:=46,unitLast:=845,order:=24576,autOrder:=786432,parity:=7,classes:=800,raw:=19660800,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1804),
rec(k:=13581,first:=1,last:=128,unitFirst:=846,unitLast:=973,order:=24576,autOrder:=393216,parity:=3,classes:=128,raw:=3145728,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=868),
rec(k:=13582,first:=1,last:=116,unitFirst:=974,unitLast:=1089,order:=24576,autOrder:=786432,parity:=7,classes:=116,raw:=2850816,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1212),
rec(k:=13583,first:=1,last:=98,unitFirst:=1090,unitLast:=1187,order:=24576,autOrder:=4718592,parity:=3,classes:=98,raw:=2408448,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1192),
rec(k:=13584,first:=1,last:=168,unitFirst:=1188,unitLast:=1355,order:=24576,autOrder:=786432,parity:=7,classes:=168,raw:=4128768,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=984),
rec(k:=13585,first:=1,last:=476,unitFirst:=1356,unitLast:=1831,order:=24576,autOrder:=393216,parity:=3,classes:=640,raw:=15728640,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1982)
];
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard223_v7_gpt56sol.g");
