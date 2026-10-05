# Exact wrapper for sealed degree-24 seed workload shard143.
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD143_SEGMENT001_UNIT1_1831_POSTVERIFY_V7_GPT56SOL.txt";
STOP_AFTER_UNIT:=fail;
INTERNAL_GUARD_MS:=1320000; START_UNIT:=1;
INITIAL_COUNTERS:=[0,0,0,0,0,0,0,0,0,0,0,0];
PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";
PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0;
PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";
CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD143_CHECKPOINT_GPT56SOL.txt";
CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD143_CHECKPOINT_TMP_GPT56SOL.txt";
EXPECTED_PROFILE_SHA256:="1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2";
EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard143_v7_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="49FE1038A0396FFBA6B53F3D128DCFE7FA274573DED70C6799EE743855B74800";
S143_RECORDS:=[
rec(k:=12981,first:=239,last:=420,unitFirst:=1,unitLast:=182,order:=24576,autOrder:=3145728,parity:=1,classes:=420,raw:=10321920,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1563),
rec(k:=12982,first:=1,last:=96,unitFirst:=183,unitLast:=278,order:=24576,autOrder:=393216,parity:=3,classes:=96,raw:=2359296,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1338),
rec(k:=12986,first:=1,last:=560,unitFirst:=279,unitLast:=838,order:=24576,autOrder:=3145728,parity:=3,classes:=560,raw:=13762560,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1629),
rec(k:=12987,first:=1,last:=277,unitFirst:=839,unitLast:=1115,order:=24576,autOrder:=3145728,parity:=1,classes:=277,raw:=6807552,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=952),
rec(k:=12988,first:=1,last:=376,unitFirst:=1116,unitLast:=1491,order:=24576,autOrder:=3145728,parity:=1,classes:=376,raw:=9240576,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=2039),
rec(k:=12989,first:=1,last:=160,unitFirst:=1492,unitLast:=1651,order:=24576,autOrder:=786432,parity:=1,classes:=160,raw:=3932160,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1194),
rec(k:=12990,first:=1,last:=160,unitFirst:=1652,unitLast:=1811,order:=24576,autOrder:=786432,parity:=1,classes:=160,raw:=3932160,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1982),
rec(k:=12991,first:=1,last:=20,unitFirst:=1812,unitLast:=1831,order:=24576,autOrder:=6291456,parity:=1,classes:=142,raw:=3489792,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=2061)
];
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard143_v7_gpt56sol.g");
