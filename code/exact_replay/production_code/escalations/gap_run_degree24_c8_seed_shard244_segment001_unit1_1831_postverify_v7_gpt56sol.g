# Exact wrapper for sealed degree-24 seed workload shard244.
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD244_SEGMENT001_UNIT1_1831_POSTVERIFY_V7_GPT56SOL.txt";
STOP_AFTER_UNIT:=fail;
INTERNAL_GUARD_MS:=1320000; START_UNIT:=1;
INITIAL_COUNTERS:=[0,0,0,0,0,0,0,0,0,0,0,0];
PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";
PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0;
PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";
CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD244_CHECKPOINT_GPT56SOL.txt";
CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD244_CHECKPOINT_TMP_GPT56SOL.txt";
EXPECTED_PROFILE_SHA256:="1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2";
EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard244_v7_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="BF6B071C4CC9BF00DD2711DED65C622750E25A49F45CD671EC077090D12CE642";
S244_RECORDS:=[
rec(k:=13695,first:=1,last:=640,unitFirst:=1,unitLast:=640,order:=24576,autOrder:=393216,parity:=15,classes:=640,raw:=15728640,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1827),
rec(k:=13696,first:=1,last:=440,unitFirst:=641,unitLast:=1080,order:=24576,autOrder:=786432,parity:=15,classes:=440,raw:=10813440,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1199),
rec(k:=13697,first:=1,last:=440,unitFirst:=1081,unitLast:=1520,order:=24576,autOrder:=786432,parity:=15,classes:=440,raw:=10813440,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=835),
rec(k:=13698,first:=1,last:=311,unitFirst:=1521,unitLast:=1831,order:=24576,autOrder:=393216,parity:=15,classes:=640,raw:=15728640,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1400)
];
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard244_v7_gpt56sol.g");
