# Exact wrapper for sealed degree-24 seed workload shard226.
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD226_SEGMENT001_UNIT1_1831_POSTVERIFY_V7_GPT56SOL.txt";
STOP_AFTER_UNIT:=fail;
INTERNAL_GUARD_MS:=1320000; START_UNIT:=1;
INITIAL_COUNTERS:=[0,0,0,0,0,0,0,0,0,0,0,0];
PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";
PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0;
PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";
CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD226_CHECKPOINT_GPT56SOL.txt";
CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD226_CHECKPOINT_TMP_GPT56SOL.txt";
EXPECTED_PROFILE_SHA256:="1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2";
EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard226_v7_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="3482A68AD1BCF4B52AAF18D5559690483D910B36AB8AF57CC4739B382EE741FF";
S226_RECORDS:=[
rec(k:=13602,first:=296,last:=640,unitFirst:=1,unitLast:=345,order:=24576,autOrder:=393216,parity:=7,classes:=640,raw:=15728640,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1409),
rec(k:=13603,first:=1,last:=60,unitFirst:=346,unitLast:=405,order:=24576,autOrder:=393216,parity:=7,classes:=60,raw:=1474560,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1500),
rec(k:=13604,first:=1,last:=600,unitFirst:=406,unitLast:=1005,order:=24576,autOrder:=786432,parity:=7,classes:=600,raw:=14745600,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1718),
rec(k:=13605,first:=1,last:=800,unitFirst:=1006,unitLast:=1805,order:=24576,autOrder:=786432,parity:=3,classes:=800,raw:=19660800,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1761),
rec(k:=13606,first:=1,last:=26,unitFirst:=1806,unitLast:=1831,order:=24576,autOrder:=786432,parity:=3,classes:=156,raw:=3833856,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1304)
];
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard226_v7_gpt56sol.g");
