# Exact wrapper for sealed degree-24 seed workload shard635.
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD635_SEGMENT001_UNIT1_915_POSTVERIFY_V7_GPT56SOL.txt";
STOP_AFTER_UNIT:=fail;
INTERNAL_GUARD_MS:=1320000; START_UNIT:=1;
INITIAL_COUNTERS:=[0,0,0,0,0,0,0,0,0,0,0,0];
PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";
PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0;
PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";
CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD635_CHECKPOINT_GPT56SOL.txt";
CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD635_CHECKPOINT_TMP_GPT56SOL.txt";
EXPECTED_PROFILE_SHA256:="1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2";
EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard635_v7_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="6CA8CB2CF5D9547DAFEB4F07764CB87C15534CF80D680AC1EB9D38FA8CE0905B";
S635_RECORDS:=[
rec(k:=15652,first:=130,last:=200,unitFirst:=1,unitLast:=71,order:=49152,autOrder:=1572864,parity:=3,classes:=200,raw:=9830400,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=2173),
rec(k:=15653,first:=1,last:=164,unitFirst:=72,unitLast:=235,order:=49152,autOrder:=1572864,parity:=3,classes:=164,raw:=8060928,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=2488),
rec(k:=15654,first:=1,last:=132,unitFirst:=236,unitLast:=367,order:=49152,autOrder:=1572864,parity:=3,classes:=132,raw:=6488064,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=2293),
rec(k:=15655,first:=1,last:=368,unitFirst:=368,unitLast:=735,order:=49152,autOrder:=1572864,parity:=7,classes:=368,raw:=18087936,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=3355),
rec(k:=15656,first:=1,last:=180,unitFirst:=736,unitLast:=915,order:=49152,autOrder:=1572864,parity:=7,classes:=212,raw:=10420224,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1551)
];
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard635_v7_gpt56sol.g");
