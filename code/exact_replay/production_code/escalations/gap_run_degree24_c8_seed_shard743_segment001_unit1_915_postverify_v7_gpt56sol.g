# Exact wrapper for sealed degree-24 seed workload shard743.
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD743_SEGMENT001_UNIT1_915_POSTVERIFY_V7_GPT56SOL.txt";
STOP_AFTER_UNIT:=fail;
INTERNAL_GUARD_MS:=1320000; START_UNIT:=1;
INITIAL_COUNTERS:=[0,0,0,0,0,0,0,0,0,0,0,0];
PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";
PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0;
PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";
CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD743_CHECKPOINT_GPT56SOL.txt";
CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD743_CHECKPOINT_TMP_GPT56SOL.txt";
EXPECTED_PROFILE_SHA256:="1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2";
EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard743_v7_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="9CED2CC552856AC31D8C33EE67C018884042423B960AAD6E0D75D73B397617CE";
S743_RECORDS:=[
rec(k:=15789,first:=539,last:=1054,unitFirst:=1,unitLast:=516,order:=49152,autOrder:=3145728,parity:=3,classes:=1054,raw:=51806208,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=2323),
rec(k:=15790,first:=1,last:=108,unitFirst:=517,unitLast:=624,order:=49152,autOrder:=1572864,parity:=1,classes:=108,raw:=5308416,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1750),
rec(k:=15791,first:=1,last:=291,unitFirst:=625,unitLast:=915,order:=49152,autOrder:=6291456,parity:=1,classes:=358,raw:=17596416,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1717)
];
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard743_v7_gpt56sol.g");
