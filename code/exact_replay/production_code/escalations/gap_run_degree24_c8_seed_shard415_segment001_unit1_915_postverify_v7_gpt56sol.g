# Exact wrapper for sealed degree-24 seed workload shard415.
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD415_SEGMENT001_UNIT1_915_POSTVERIFY_V7_GPT56SOL.txt";
STOP_AFTER_UNIT:=fail;
INTERNAL_GUARD_MS:=1320000; START_UNIT:=1;
INITIAL_COUNTERS:=[0,0,0,0,0,0,0,0,0,0,0,0];
PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";
PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0;
PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";
CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD415_CHECKPOINT_GPT56SOL.txt";
CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD415_CHECKPOINT_TMP_GPT56SOL.txt";
EXPECTED_PROFILE_SHA256:="1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2";
EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard415_v7_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="933A32D13122C867D82150FD490D4FE63CBE825E767D446FF14FB228250E342A";
S415_RECORDS:=[
rec(k:=15092,first:=89,last:=320,unitFirst:=1,unitLast:=232,order:=49152,autOrder:=1572864,parity:=3,classes:=320,raw:=15728640,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1156),
rec(k:=15093,first:=1,last:=208,unitFirst:=233,unitLast:=440,order:=49152,autOrder:=3145728,parity:=3,classes:=208,raw:=10223616,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=2433),
rec(k:=15094,first:=1,last:=288,unitFirst:=441,unitLast:=728,order:=49152,autOrder:=1572864,parity:=3,classes:=288,raw:=14155776,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1572),
rec(k:=15095,first:=1,last:=187,unitFirst:=729,unitLast:=915,order:=49152,autOrder:=6291456,parity:=3,classes:=509,raw:=25018368,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1366)
];
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard415_v7_gpt56sol.g");
