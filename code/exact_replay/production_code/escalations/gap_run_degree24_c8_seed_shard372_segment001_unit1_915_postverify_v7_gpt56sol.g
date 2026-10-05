# Exact wrapper for sealed degree-24 seed workload shard372.
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD372_SEGMENT001_UNIT1_915_POSTVERIFY_V7_GPT56SOL.txt";
STOP_AFTER_UNIT:=fail;
INTERNAL_GUARD_MS:=1320000; START_UNIT:=1;
INITIAL_COUNTERS:=[0,0,0,0,0,0,0,0,0,0,0,0];
PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";
PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0;
PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";
CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD372_CHECKPOINT_GPT56SOL.txt";
CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD372_CHECKPOINT_TMP_GPT56SOL.txt";
EXPECTED_PROFILE_SHA256:="1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2";
EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard372_v7_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="5A22A5BDDB00199FD6A035457CC5CA84FBBD1C31A356702D1ECE3AAB61943613";
S372_RECORDS:=[
rec(k:=14939,first:=26,last:=320,unitFirst:=1,unitLast:=295,order:=49152,autOrder:=1572864,parity:=3,classes:=320,raw:=15728640,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=2246),
rec(k:=14940,first:=1,last:=96,unitFirst:=296,unitLast:=391,order:=49152,autOrder:=786432,parity:=1,classes:=96,raw:=4718592,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=784),
rec(k:=14941,first:=1,last:=96,unitFirst:=392,unitLast:=487,order:=49152,autOrder:=393216,parity:=1,classes:=96,raw:=4718592,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1132),
rec(k:=14942,first:=1,last:=140,unitFirst:=488,unitLast:=627,order:=49152,autOrder:=3145728,parity:=3,classes:=140,raw:=6881280,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1585),
rec(k:=14943,first:=1,last:=288,unitFirst:=628,unitLast:=915,order:=49152,autOrder:=3145728,parity:=3,classes:=348,raw:=17104896,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1967)
];
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard372_v7_gpt56sol.g");
