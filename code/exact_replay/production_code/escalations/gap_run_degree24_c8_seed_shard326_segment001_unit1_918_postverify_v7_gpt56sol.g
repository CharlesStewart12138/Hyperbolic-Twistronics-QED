# Exact wrapper for sealed degree-24 seed workload shard326.
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD326_SEGMENT001_UNIT1_918_POSTVERIFY_V7_GPT56SOL.txt";
STOP_AFTER_UNIT:=fail;
INTERNAL_GUARD_MS:=1320000; START_UNIT:=1;
INITIAL_COUNTERS:=[0,0,0,0,0,0,0,0,0,0,0,0];
PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";
PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0;
PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";
CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD326_CHECKPOINT_GPT56SOL.txt";
CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD326_CHECKPOINT_TMP_GPT56SOL.txt";
EXPECTED_PROFILE_SHA256:="1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2";
EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard326_v7_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="8D583C3A65D2919B87CADD5B45CFA376684916CB9BA545AA7315732778333FD1";
S326_RECORDS:=[
rec(k:=14743,first:=22,last:=85,unitFirst:=1,unitLast:=64,order:=46656,autOrder:=2985984,parity:=15,classes:=85,raw:=3965760,method:="pc",representation:="pc_transport",pcOrder:=46656,profileMs:=866),
rec(k:=14744,first:=1,last:=588,unitFirst:=65,unitLast:=652,order:=49152,autOrder:=12582912,parity:=3,classes:=588,raw:=28901376,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1588),
rec(k:=14745,first:=1,last:=266,unitFirst:=653,unitLast:=918,order:=49152,autOrder:=37748736,parity:=7,classes:=284,raw:=13959168,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1260)
];
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard326_v7_gpt56sol.g");
