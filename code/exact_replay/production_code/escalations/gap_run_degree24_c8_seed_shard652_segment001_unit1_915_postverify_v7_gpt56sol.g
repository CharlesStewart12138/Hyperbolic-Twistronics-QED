# Exact wrapper for sealed degree-24 seed workload shard652.
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD652_SEGMENT001_UNIT1_915_POSTVERIFY_V7_GPT56SOL.txt";
STOP_AFTER_UNIT:=fail;
INTERNAL_GUARD_MS:=1320000; START_UNIT:=1;
INITIAL_COUNTERS:=[0,0,0,0,0,0,0,0,0,0,0,0];
PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";
PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0;
PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";
CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD652_CHECKPOINT_GPT56SOL.txt";
CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD652_CHECKPOINT_TMP_GPT56SOL.txt";
EXPECTED_PROFILE_SHA256:="1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2";
EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard652_v7_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="93EBFD5BD4E1647AC3637841297C92F29AE7956AF7F4AC3FAEBCDE8FC33C1056";
S652_RECORDS:=[
rec(k:=15686,first:=423,last:=1040,unitFirst:=1,unitLast:=618,order:=49152,autOrder:=1572864,parity:=7,classes:=1040,raw:=51118080,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=2213),
rec(k:=15687,first:=1,last:=128,unitFirst:=619,unitLast:=746,order:=49152,autOrder:=393216,parity:=7,classes:=128,raw:=6291456,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1610),
rec(k:=15688,first:=1,last:=168,unitFirst:=747,unitLast:=914,order:=49152,autOrder:=1572864,parity:=7,classes:=168,raw:=8257536,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1874),
rec(k:=15689,first:=1,last:=1,unitFirst:=915,unitLast:=915,order:=49152,autOrder:=3145728,parity:=7,classes:=334,raw:=16416768,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=2676)
];
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard652_v7_gpt56sol.g");
