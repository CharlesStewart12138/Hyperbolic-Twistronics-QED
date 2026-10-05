# Exact wrapper for sealed degree-24 seed workload shard257.
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD257_SEGMENT001_UNIT1_1831_POSTVERIFY_V7_GPT56SOL.txt";
STOP_AFTER_UNIT:=fail;
INTERNAL_GUARD_MS:=1320000; START_UNIT:=1;
INITIAL_COUNTERS:=[0,0,0,0,0,0,0,0,0,0,0,0];
PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";
PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0;
PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";
CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD257_CHECKPOINT_GPT56SOL.txt";
CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD257_CHECKPOINT_TMP_GPT56SOL.txt";
EXPECTED_PROFILE_SHA256:="1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2";
EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard257_v7_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="F41D7DED50314AEA26A908EE759B3619B942924882EF50E711BE1BDA75F471AE";
S257_RECORDS:=[
rec(k:=13761,first:=246,last:=880,unitFirst:=1,unitLast:=635,order:=24576,autOrder:=393216,parity:=7,classes:=880,raw:=21626880,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=2030),
rec(k:=13762,first:=1,last:=880,unitFirst:=636,unitLast:=1515,order:=24576,autOrder:=393216,parity:=7,classes:=880,raw:=21626880,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=2315),
rec(k:=13763,first:=1,last:=316,unitFirst:=1516,unitLast:=1831,order:=24576,autOrder:=393216,parity:=7,classes:=880,raw:=21626880,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=2346)
];
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard257_v7_gpt56sol.g");
