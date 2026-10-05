# Exact wrapper for sealed degree-24 seed workload shard231.
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD231_SEGMENT001_UNIT1_1831_POSTVERIFY_V7_GPT56SOL.txt";
STOP_AFTER_UNIT:=fail;
INTERNAL_GUARD_MS:=1320000; START_UNIT:=1;
INITIAL_COUNTERS:=[0,0,0,0,0,0,0,0,0,0,0,0];
PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";
PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0;
PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";
CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD231_CHECKPOINT_GPT56SOL.txt";
CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD231_CHECKPOINT_TMP_GPT56SOL.txt";
EXPECTED_PROFILE_SHA256:="1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2";
EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard231_v7_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="AE5FB1E213C8EB95BC0D7D35978B767960919441C3C5ABF870E02A90EE13A7E8";
S231_RECORDS:=[
rec(k:=13638,first:=56,last:=774,unitFirst:=1,unitLast:=719,order:=24576,autOrder:=9437184,parity:=3,classes:=774,raw:=19021824,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=2521),
rec(k:=13639,first:=1,last:=728,unitFirst:=720,unitLast:=1447,order:=24576,autOrder:=4718592,parity:=3,classes:=728,raw:=17891328,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=2060),
rec(k:=13640,first:=1,last:=348,unitFirst:=1448,unitLast:=1795,order:=24576,autOrder:=786432,parity:=3,classes:=348,raw:=8552448,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1449),
rec(k:=13641,first:=1,last:=36,unitFirst:=1796,unitLast:=1831,order:=24576,autOrder:=3145728,parity:=3,classes:=1164,raw:=28606464,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=3177)
];
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard231_v7_gpt56sol.g");
