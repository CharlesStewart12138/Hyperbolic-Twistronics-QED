# Exact wrapper for sealed degree-24 seed workload shard428.
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD428_SEGMENT001_UNIT1_915_POSTVERIFY_V7_GPT56SOL.txt";
STOP_AFTER_UNIT:=fail;
INTERNAL_GUARD_MS:=1320000; START_UNIT:=1;
INITIAL_COUNTERS:=[0,0,0,0,0,0,0,0,0,0,0,0];
PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";
PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0;
PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";
CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD428_CHECKPOINT_GPT56SOL.txt";
CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD428_CHECKPOINT_TMP_GPT56SOL.txt";
EXPECTED_PROFILE_SHA256:="1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2";
EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard428_v7_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="C4A6C52511F3FB3B2919A67A41E71FD40B3D7BB6D3D766116A5E6BEAEF018B55";
S428_RECORDS:=[
rec(k:=15122,first:=218,last:=288,unitFirst:=1,unitLast:=71,order:=49152,autOrder:=1572864,parity:=3,classes:=288,raw:=14155776,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=2196),
rec(k:=15123,first:=1,last:=94,unitFirst:=72,unitLast:=165,order:=49152,autOrder:=786432,parity:=1,classes:=94,raw:=4620288,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1512),
rec(k:=15124,first:=1,last:=750,unitFirst:=166,unitLast:=915,order:=49152,autOrder:=12582912,parity:=1,classes:=1020,raw:=50135040,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=3342)
];
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard428_v7_gpt56sol.g");
