# Exact wrapper for sealed degree-24 seed workload shard208.
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD208_SEGMENT001_UNIT1_1831_POSTVERIFY_V7_GPT56SOL.txt";
STOP_AFTER_UNIT:=fail;
INTERNAL_GUARD_MS:=1320000; START_UNIT:=1;
INITIAL_COUNTERS:=[0,0,0,0,0,0,0,0,0,0,0,0];
PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";
PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0;
PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";
CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD208_CHECKPOINT_GPT56SOL.txt";
CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD208_CHECKPOINT_TMP_GPT56SOL.txt";
EXPECTED_PROFILE_SHA256:="1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2";
EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard208_v7_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="81FE5FC1422E20F5D53C9D77E5CF290120FF311A779C5B9203C8EA5880542501";
S208_RECORDS:=[
rec(k:=13489,first:=940,last:=1088,unitFirst:=1,unitLast:=149,order:=24576,autOrder:=3145728,parity:=1,classes:=1088,raw:=26738688,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=3492),
rec(k:=13490,first:=1,last:=142,unitFirst:=150,unitLast:=291,order:=24576,autOrder:=6291456,parity:=1,classes:=142,raw:=3489792,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1994),
rec(k:=13493,first:=1,last:=1540,unitFirst:=292,unitLast:=1831,order:=24576,autOrder:=6291456,parity:=1,classes:=1976,raw:=48562176,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=3075)
];
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard208_v7_gpt56sol.g");
