# Exact wrapper for sealed degree-24 seed workload shard796.
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD796_SEGMENT001_UNIT1_915_POSTVERIFY_V7_GPT56SOL.txt";
STOP_AFTER_UNIT:=fail;
INTERNAL_GUARD_MS:=1320000; START_UNIT:=1;
INITIAL_COUNTERS:=[0,0,0,0,0,0,0,0,0,0,0,0];
PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";
PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0;
PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";
CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD796_CHECKPOINT_GPT56SOL.txt";
CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD796_CHECKPOINT_TMP_GPT56SOL.txt";
EXPECTED_PROFILE_SHA256:="1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2";
EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard796_v7_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="4CE651EEE0895F89202BE9F5A87199F81BC8200C6D424F005FA2A2594D1062AB";
S796_RECORDS:=[
rec(k:=15869,first:=703,last:=712,unitFirst:=1,unitLast:=10,order:=49152,autOrder:=786432,parity:=3,classes:=712,raw:=34996224,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1621),
rec(k:=15870,first:=1,last:=712,unitFirst:=11,unitLast:=722,order:=49152,autOrder:=786432,parity:=3,classes:=712,raw:=34996224,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1671),
rec(k:=15871,first:=1,last:=96,unitFirst:=723,unitLast:=818,order:=49152,autOrder:=393216,parity:=3,classes:=96,raw:=4718592,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=766),
rec(k:=15872,first:=1,last:=96,unitFirst:=819,unitLast:=914,order:=49152,autOrder:=393216,parity:=3,classes:=96,raw:=4718592,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1098),
rec(k:=15873,first:=1,last:=1,unitFirst:=915,unitLast:=915,order:=49152,autOrder:=393216,parity:=3,classes:=128,raw:=6291456,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1409)
];
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard796_v7_gpt56sol.g");
