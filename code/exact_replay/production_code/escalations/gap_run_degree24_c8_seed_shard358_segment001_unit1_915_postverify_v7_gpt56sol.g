# Exact wrapper for sealed degree-24 seed workload shard358.
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD358_SEGMENT001_UNIT1_915_POSTVERIFY_V7_GPT56SOL.txt";
STOP_AFTER_UNIT:=fail;
INTERNAL_GUARD_MS:=1320000; START_UNIT:=1;
INITIAL_COUNTERS:=[0,0,0,0,0,0,0,0,0,0,0,0];
PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";
PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0;
PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";
CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD358_CHECKPOINT_GPT56SOL.txt";
CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD358_CHECKPOINT_TMP_GPT56SOL.txt";
EXPECTED_PROFILE_SHA256:="1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2";
EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard358_v7_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="633D9DE12DC03A72B6A3979E452FCD27F0A42D8D9DE861E8C741F729EAFD52A6";
S358_RECORDS:=[
rec(k:=14893,first:=2,last:=444,unitFirst:=1,unitLast:=443,order:=49152,autOrder:=3145728,parity:=7,classes:=444,raw:=21823488,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=2197),
rec(k:=14894,first:=1,last:=212,unitFirst:=444,unitLast:=655,order:=49152,autOrder:=1572864,parity:=7,classes:=212,raw:=10420224,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=2795),
rec(k:=14895,first:=1,last:=176,unitFirst:=656,unitLast:=831,order:=49152,autOrder:=1572864,parity:=7,classes:=176,raw:=8650752,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=2018),
rec(k:=14896,first:=1,last:=84,unitFirst:=832,unitLast:=915,order:=49152,autOrder:=1572864,parity:=7,classes:=224,raw:=11010048,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=2286)
];
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard358_v7_gpt56sol.g");
