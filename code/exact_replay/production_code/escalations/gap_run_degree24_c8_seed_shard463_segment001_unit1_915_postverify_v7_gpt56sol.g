# Exact wrapper for sealed degree-24 seed workload shard463.
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD463_SEGMENT001_UNIT1_915_POSTVERIFY_V7_GPT56SOL.txt";
STOP_AFTER_UNIT:=fail;
INTERNAL_GUARD_MS:=1320000; START_UNIT:=1;
INITIAL_COUNTERS:=[0,0,0,0,0,0,0,0,0,0,0,0];
PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";
PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0;
PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";
CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD463_CHECKPOINT_GPT56SOL.txt";
CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD463_CHECKPOINT_TMP_GPT56SOL.txt";
EXPECTED_PROFILE_SHA256:="1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2";
EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard463_v7_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="4DF6C2E069874839C0B0C677B3B3A81A0FB4CC6991EF70A162825DB506971B1C";
S463_RECORDS:=[
rec(k:=15200,first:=333,last:=653,unitFirst:=1,unitLast:=321,order:=49152,autOrder:=25165824,parity:=3,classes:=653,raw:=32096256,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=3464),
rec(k:=15201,first:=1,last:=448,unitFirst:=322,unitLast:=769,order:=49152,autOrder:=3145728,parity:=3,classes:=448,raw:=22020096,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=2197),
rec(k:=15202,first:=1,last:=146,unitFirst:=770,unitLast:=915,order:=49152,autOrder:=12582912,parity:=3,classes:=890,raw:=43745280,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=3815)
];
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard463_v7_gpt56sol.g");
