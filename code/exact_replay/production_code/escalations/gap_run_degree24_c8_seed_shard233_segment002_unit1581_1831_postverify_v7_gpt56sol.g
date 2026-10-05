# Exact wrapper for sealed degree-24 seed workload shard233.
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD233_SEGMENT002_UNIT1581_1831_POSTVERIFY_V7_GPT56SOL.txt";
STOP_AFTER_UNIT:=fail;
INTERNAL_GUARD_MS:=1320000; START_UNIT:=1581;
INITIAL_COUNTERS:=[1580,38830080,1580,31,1833248,853152,221952,92160,0,0,0,0];
PREVIOUS_CHECKPOINT_SHA256:="0f10ac497383b5477e48e126666b5dbc86ebf9d2cd0f433dd8f35c5f59e67129";
PREVIOUS_OUTPUT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD233_SEGMENT001_UNIT1_1831_POSTVERIFY_V7_GPT56SOL.txt"; PREVIOUS_OUTPUT_PREFIX_BYTES:=1187130;
PREVIOUS_OUTPUT_PREFIX_SHA256:="8f4d57e551c344efaf32dfebcfc7581172964061853e2816fcc465740908f9ef";
CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD233_CHECKPOINT_GPT56SOL.txt";
CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD233_CHECKPOINT_TMP_GPT56SOL.txt";
EXPECTED_PROFILE_SHA256:="1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2";
EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard233_v7_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="32FAF2D6C556E97095EE93BFD33E7888BC05270340E3A0192AAB4D9B49ED7863";
S233_RECORDS:=[
rec(k:=13643,first:=568,last:=880,unitFirst:=1,unitLast:=313,order:=24576,autOrder:=1572864,parity:=1,classes:=880,raw:=21626880,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=2570),
rec(k:=13644,first:=1,last:=560,unitFirst:=314,unitLast:=873,order:=24576,autOrder:=3145728,parity:=3,classes:=560,raw:=13762560,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1676),
rec(k:=13645,first:=1,last:=170,unitFirst:=874,unitLast:=1043,order:=24576,autOrder:=3145728,parity:=3,classes:=170,raw:=4177920,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=2543),
rec(k:=13646,first:=1,last:=348,unitFirst:=1044,unitLast:=1391,order:=24576,autOrder:=786432,parity:=3,classes:=348,raw:=8552448,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1355),
rec(k:=13647,first:=1,last:=144,unitFirst:=1392,unitLast:=1535,order:=24576,autOrder:=393216,parity:=7,classes:=144,raw:=3538944,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1501),
rec(k:=13648,first:=1,last:=280,unitFirst:=1536,unitLast:=1815,order:=24576,autOrder:=786432,parity:=7,classes:=280,raw:=6881280,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1237),
rec(k:=13649,first:=1,last:=16,unitFirst:=1816,unitLast:=1831,order:=24576,autOrder:=786432,parity:=7,classes:=280,raw:=6881280,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1691)
];
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard233_v7_gpt56sol.g");
