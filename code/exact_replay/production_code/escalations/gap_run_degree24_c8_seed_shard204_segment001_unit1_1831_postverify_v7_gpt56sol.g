# Exact wrapper for sealed degree-24 seed workload shard204.
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD204_SEGMENT001_UNIT1_1831_POSTVERIFY_V7_GPT56SOL.txt";
STOP_AFTER_UNIT:=fail;
INTERNAL_GUARD_MS:=1320000; START_UNIT:=1;
INITIAL_COUNTERS:=[0,0,0,0,0,0,0,0,0,0,0,0];
PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";
PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0;
PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";
CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD204_CHECKPOINT_GPT56SOL.txt";
CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD204_CHECKPOINT_TMP_GPT56SOL.txt";
EXPECTED_PROFILE_SHA256:="1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2";
EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard204_v7_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="55ACCFDC9C0F5A498A9237C828F70246C195EF5C19DF3680B7B8A55863A2B569";
S204_RECORDS:=[
rec(k:=13467,first:=175,last:=880,unitFirst:=1,unitLast:=706,order:=24576,autOrder:=1572864,parity:=3,classes:=880,raw:=21626880,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=2600),
rec(k:=13468,first:=1,last:=685,unitFirst:=707,unitLast:=1391,order:=24576,autOrder:=1572864,parity:=7,classes:=685,raw:=16834560,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=3248),
rec(k:=13469,first:=1,last:=432,unitFirst:=1392,unitLast:=1823,order:=24576,autOrder:=1572864,parity:=7,classes:=432,raw:=10616832,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1632),
rec(k:=13470,first:=1,last:=8,unitFirst:=1824,unitLast:=1831,order:=24576,autOrder:=3145728,parity:=7,classes:=1180,raw:=28999680,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=3163)
];
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard204_v7_gpt56sol.g");
