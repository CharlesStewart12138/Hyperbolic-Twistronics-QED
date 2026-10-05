# Exact wrapper for sealed degree-24 seed workload shard297.
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD297_SEGMENT001_UNIT1_1831_POSTVERIFY_V7_GPT56SOL.txt";
STOP_AFTER_UNIT:=fail;
INTERNAL_GUARD_MS:=1320000; START_UNIT:=1;
INITIAL_COUNTERS:=[0,0,0,0,0,0,0,0,0,0,0,0];
PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";
PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0;
PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";
CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD297_CHECKPOINT_GPT56SOL.txt";
CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD297_CHECKPOINT_TMP_GPT56SOL.txt";
EXPECTED_PROFILE_SHA256:="1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2";
EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard297_v7_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="02DDE25911FDFB2BE3E1EE6A348086C17109AE1C1D7B745F7D395C72836791F3";
S297_RECORDS:=[
rec(k:=13933,first:=485,last:=876,unitFirst:=1,unitLast:=392,order:=24576,autOrder:=12582912,parity:=15,classes:=876,raw:=21528576,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=2853),
rec(k:=13934,first:=1,last:=592,unitFirst:=393,unitLast:=984,order:=24576,autOrder:=3145728,parity:=7,classes:=592,raw:=14548992,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=4573),
rec(k:=13935,first:=1,last:=847,unitFirst:=985,unitLast:=1831,order:=24576,autOrder:=6291456,parity:=15,classes:=1012,raw:=24870912,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=2589)
];
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard297_v7_gpt56sol.g");
