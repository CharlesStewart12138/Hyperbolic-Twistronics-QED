# Exact wrapper for sealed degree-24 seed workload shard201.
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD201_SEGMENT001_UNIT1_1831_POSTVERIFY_V7_GPT56SOL.txt";
STOP_AFTER_UNIT:=fail;
INTERNAL_GUARD_MS:=1320000; START_UNIT:=1;
INITIAL_COUNTERS:=[0,0,0,0,0,0,0,0,0,0,0,0];
PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";
PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0;
PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";
CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD201_CHECKPOINT_GPT56SOL.txt";
CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD201_CHECKPOINT_TMP_GPT56SOL.txt";
EXPECTED_PROFILE_SHA256:="1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2";
EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard201_v7_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="C6A4D4F1B501F07F488407B07E0C466BD839C681A9A35323EBB97973119852C5";
S201_RECORDS:=[
rec(k:=13449,first:=101,last:=128,unitFirst:=1,unitLast:=28,order:=24576,autOrder:=393216,parity:=7,classes:=128,raw:=3145728,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1163),
rec(k:=13450,first:=1,last:=226,unitFirst:=29,unitLast:=254,order:=24576,autOrder:=1572864,parity:=7,classes:=226,raw:=5554176,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1676),
rec(k:=13451,first:=1,last:=120,unitFirst:=255,unitLast:=374,order:=24576,autOrder:=786432,parity:=7,classes:=120,raw:=2949120,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1377),
rec(k:=13452,first:=1,last:=525,unitFirst:=375,unitLast:=899,order:=24576,autOrder:=1572864,parity:=7,classes:=525,raw:=12902400,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=2224),
rec(k:=13453,first:=1,last:=148,unitFirst:=900,unitLast:=1047,order:=24576,autOrder:=393216,parity:=3,classes:=148,raw:=3637248,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1596),
rec(k:=13454,first:=1,last:=784,unitFirst:=1048,unitLast:=1831,order:=24576,autOrder:=6291456,parity:=7,classes:=1360,raw:=33423360,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=2416)
];
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard201_v7_gpt56sol.g");
