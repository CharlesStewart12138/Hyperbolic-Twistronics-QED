# Exact wrapper for sealed degree-24 seed workload shard145.
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD145_SEGMENT001_UNIT1_1831_POSTVERIFY_V7_GPT56SOL.txt";
STOP_AFTER_UNIT:=fail;
INTERNAL_GUARD_MS:=1320000; START_UNIT:=1;
INITIAL_COUNTERS:=[0,0,0,0,0,0,0,0,0,0,0,0];
PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";
PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0;
PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";
CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD145_CHECKPOINT_GPT56SOL.txt";
CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD145_CHECKPOINT_TMP_GPT56SOL.txt";
EXPECTED_PROFILE_SHA256:="1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2";
EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard145_v7_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="D4C82D5A06498A8CA12EA06B041674B11853C6904ACD561AE7A36C5CC15F0555";
S145_RECORDS:=[
rec(k:=12996,first:=299,last:=560,unitFirst:=1,unitLast:=262,order:=24576,autOrder:=6291456,parity:=3,classes:=560,raw:=13762560,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1386),
rec(k:=12997,first:=1,last:=160,unitFirst:=263,unitLast:=422,order:=24576,autOrder:=786432,parity:=1,classes:=160,raw:=3932160,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1568),
rec(k:=12998,first:=1,last:=708,unitFirst:=423,unitLast:=1130,order:=24576,autOrder:=1572864,parity:=3,classes:=708,raw:=17399808,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=2418),
rec(k:=12999,first:=1,last:=160,unitFirst:=1131,unitLast:=1290,order:=24576,autOrder:=786432,parity:=1,classes:=160,raw:=3932160,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=857),
rec(k:=13000,first:=1,last:=120,unitFirst:=1291,unitLast:=1410,order:=24576,autOrder:=1572864,parity:=1,classes:=120,raw:=2949120,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1349),
rec(k:=13001,first:=1,last:=180,unitFirst:=1411,unitLast:=1590,order:=24576,autOrder:=1572864,parity:=1,classes:=180,raw:=4423680,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1368),
rec(k:=13002,first:=1,last:=241,unitFirst:=1591,unitLast:=1831,order:=24576,autOrder:=3145728,parity:=1,classes:=366,raw:=8994816,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1192)
];
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard145_v7_gpt56sol.g");
