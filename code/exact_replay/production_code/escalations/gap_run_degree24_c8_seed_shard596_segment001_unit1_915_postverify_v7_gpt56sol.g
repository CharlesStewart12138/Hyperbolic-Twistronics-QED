# Exact wrapper for sealed degree-24 seed workload shard596.
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD596_SEGMENT001_UNIT1_915_POSTVERIFY_V7_GPT56SOL.txt";
STOP_AFTER_UNIT:=fail;
INTERNAL_GUARD_MS:=1320000; START_UNIT:=1;
INITIAL_COUNTERS:=[0,0,0,0,0,0,0,0,0,0,0,0];
PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";
PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0;
PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";
CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD596_CHECKPOINT_GPT56SOL.txt";
CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD596_CHECKPOINT_TMP_GPT56SOL.txt";
EXPECTED_PROFILE_SHA256:="1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2";
EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard596_v7_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="29A3679DD818442DC611F16192932E183490550C2097B7FB0869805B5505304D";
S596_RECORDS:=[
rec(k:=15556,first:=448,last:=476,unitFirst:=1,unitLast:=29,order:=49152,autOrder:=3145728,parity:=31,classes:=476,raw:=23396352,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=2718),
rec(k:=15557,first:=1,last:=192,unitFirst:=30,unitLast:=221,order:=49152,autOrder:=1572864,parity:=15,classes:=192,raw:=9437184,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1792),
rec(k:=15558,first:=1,last:=694,unitFirst:=222,unitLast:=915,order:=49152,autOrder:=3145728,parity:=15,classes:=1110,raw:=54558720,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=2363)
];
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard596_v7_gpt56sol.g");
