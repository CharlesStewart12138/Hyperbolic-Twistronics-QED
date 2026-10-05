# Exact wrapper for sealed degree-24 seed workload shard617.
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD617_SEGMENT001_UNIT1_915_POSTVERIFY_V7_GPT56SOL.txt";
STOP_AFTER_UNIT:=fail;
INTERNAL_GUARD_MS:=1320000; START_UNIT:=1;
INITIAL_COUNTERS:=[0,0,0,0,0,0,0,0,0,0,0,0];
PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";
PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0;
PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";
CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD617_CHECKPOINT_GPT56SOL.txt";
CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD617_CHECKPOINT_TMP_GPT56SOL.txt";
EXPECTED_PROFILE_SHA256:="1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2";
EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard617_v7_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="4198489829DF1EE533C1163899053F0CA459D1963B756EACB3D06B5BF9A5C1CF";
S617_RECORDS:=[
rec(k:=15596,first:=296,last:=368,unitFirst:=1,unitLast:=73,order:=49152,autOrder:=1572864,parity:=3,classes:=368,raw:=18087936,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=2014),
rec(k:=15597,first:=1,last:=444,unitFirst:=74,unitLast:=517,order:=49152,autOrder:=3145728,parity:=7,classes:=444,raw:=21823488,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1496),
rec(k:=15598,first:=1,last:=188,unitFirst:=518,unitLast:=705,order:=49152,autOrder:=1572864,parity:=3,classes:=188,raw:=9240576,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1684),
rec(k:=15599,first:=1,last:=160,unitFirst:=706,unitLast:=865,order:=49152,autOrder:=1572864,parity:=7,classes:=160,raw:=7864320,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1765),
rec(k:=15600,first:=1,last:=50,unitFirst:=866,unitLast:=915,order:=49152,autOrder:=1572864,parity:=3,classes:=184,raw:=9043968,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1909)
];
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard617_v7_gpt56sol.g");
