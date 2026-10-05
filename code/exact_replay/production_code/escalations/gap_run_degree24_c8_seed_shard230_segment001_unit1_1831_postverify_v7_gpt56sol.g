# Exact wrapper for sealed degree-24 seed workload shard230.
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD230_SEGMENT001_UNIT1_1831_POSTVERIFY_V7_GPT56SOL.txt";
STOP_AFTER_UNIT:=fail;
INTERNAL_GUARD_MS:=1320000; START_UNIT:=1;
INITIAL_COUNTERS:=[0,0,0,0,0,0,0,0,0,0,0,0];
PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";
PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0;
PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";
CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD230_CHECKPOINT_GPT56SOL.txt";
CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD230_CHECKPOINT_TMP_GPT56SOL.txt";
EXPECTED_PROFILE_SHA256:="1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2";
EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard230_v7_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="3266797CFEE34F065EC173F5FE0308870534744EC8B67D7D8377E8DF3AB1869A";
S230_RECORDS:=[
rec(k:=13634,first:=253,last:=560,unitFirst:=1,unitLast:=308,order:=24576,autOrder:=6291456,parity:=3,classes:=560,raw:=13762560,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=2257),
rec(k:=13635,first:=1,last:=560,unitFirst:=309,unitLast:=868,order:=24576,autOrder:=6291456,parity:=3,classes:=560,raw:=13762560,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1569),
rec(k:=13636,first:=1,last:=348,unitFirst:=869,unitLast:=1216,order:=24576,autOrder:=393216,parity:=7,classes:=348,raw:=8552448,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1205),
rec(k:=13637,first:=1,last:=560,unitFirst:=1217,unitLast:=1776,order:=24576,autOrder:=6291456,parity:=3,classes:=560,raw:=13762560,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1912),
rec(k:=13638,first:=1,last:=55,unitFirst:=1777,unitLast:=1831,order:=24576,autOrder:=9437184,parity:=3,classes:=774,raw:=19021824,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=2521)
];
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard230_v7_gpt56sol.g");
