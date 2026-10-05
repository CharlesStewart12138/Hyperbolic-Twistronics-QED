# Exact wrapper for sealed degree-24 seed workload shard190.
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD190_SEGMENT001_UNIT1_1831_POSTVERIFY_V7_GPT56SOL.txt";
STOP_AFTER_UNIT:=fail;
INTERNAL_GUARD_MS:=1320000; START_UNIT:=1;
INITIAL_COUNTERS:=[0,0,0,0,0,0,0,0,0,0,0,0];
PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";
PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0;
PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";
CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD190_CHECKPOINT_GPT56SOL.txt";
CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD190_CHECKPOINT_TMP_GPT56SOL.txt";
EXPECTED_PROFILE_SHA256:="1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2";
EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard190_v7_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="E10A64DF104C83CBCBDD8B9D887D0A72E81046451C7FF281407104C06DB6C019";
S190_RECORDS:=[
rec(k:=13398,first:=92,last:=128,unitFirst:=1,unitLast:=37,order:=24576,autOrder:=393216,parity:=7,classes:=128,raw:=3145728,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1769),
rec(k:=13399,first:=1,last:=576,unitFirst:=38,unitLast:=613,order:=24576,autOrder:=393216,parity:=7,classes:=576,raw:=14155776,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1881),
rec(k:=13400,first:=1,last:=376,unitFirst:=614,unitLast:=989,order:=24576,autOrder:=786432,parity:=7,classes:=376,raw:=9240576,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1335),
rec(k:=13401,first:=1,last:=576,unitFirst:=990,unitLast:=1565,order:=24576,autOrder:=393216,parity:=7,classes:=576,raw:=14155776,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1341),
rec(k:=13402,first:=1,last:=266,unitFirst:=1566,unitLast:=1831,order:=24576,autOrder:=786432,parity:=7,classes:=328,raw:=8060928,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1183)
];
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard190_v7_gpt56sol.g");
