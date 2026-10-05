# Exact wrapper for sealed degree-24 seed workload shard207.
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD207_SEGMENT001_UNIT1_1831_POSTVERIFY_V7_GPT56SOL.txt";
STOP_AFTER_UNIT:=fail;
INTERNAL_GUARD_MS:=1320000; START_UNIT:=1;
INITIAL_COUNTERS:=[0,0,0,0,0,0,0,0,0,0,0,0];
PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";
PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0;
PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";
CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD207_CHECKPOINT_GPT56SOL.txt";
CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD207_CHECKPOINT_TMP_GPT56SOL.txt";
EXPECTED_PROFILE_SHA256:="1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2";
EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard207_v7_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="95086B47C8B1A1941A71D802F67377A9345BD32FD1AA272A3965121684AED1C5";
S207_RECORDS:=[
rec(k:=13484,first:=157,last:=208,unitFirst:=1,unitLast:=52,order:=24576,autOrder:=196608,parity:=3,classes:=208,raw:=5111808,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=936),
rec(k:=13485,first:=1,last:=420,unitFirst:=53,unitLast:=472,order:=24576,autOrder:=786432,parity:=3,classes:=420,raw:=10321920,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=2006),
rec(k:=13486,first:=1,last:=420,unitFirst:=473,unitLast:=892,order:=24576,autOrder:=786432,parity:=3,classes:=420,raw:=10321920,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=3487),
rec(k:=13489,first:=1,last:=939,unitFirst:=893,unitLast:=1831,order:=24576,autOrder:=3145728,parity:=1,classes:=1088,raw:=26738688,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=3492)
];
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard207_v7_gpt56sol.g");
