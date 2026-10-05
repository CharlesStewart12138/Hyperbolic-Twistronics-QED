# Exact wrapper for sealed degree-24 seed workload shard234.
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD234_SEGMENT001_UNIT1_1831_POSTVERIFY_V7_GPT56SOL.txt";
STOP_AFTER_UNIT:=fail;
INTERNAL_GUARD_MS:=1320000; START_UNIT:=1;
INITIAL_COUNTERS:=[0,0,0,0,0,0,0,0,0,0,0,0];
PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";
PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0;
PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";
CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD234_CHECKPOINT_GPT56SOL.txt";
CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD234_CHECKPOINT_TMP_GPT56SOL.txt";
EXPECTED_PROFILE_SHA256:="1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2";
EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard234_v7_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="8CCEA0580B942B0BA779C191062679AE213678555DCD2944DF6BFCEDA5BB8AF4";
S234_RECORDS:=[
rec(k:=13649,first:=17,last:=280,unitFirst:=1,unitLast:=264,order:=24576,autOrder:=786432,parity:=7,classes:=280,raw:=6881280,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1691),
rec(k:=13650,first:=1,last:=72,unitFirst:=265,unitLast:=336,order:=24576,autOrder:=1179648,parity:=3,classes:=72,raw:=1769472,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=970),
rec(k:=13651,first:=1,last:=180,unitFirst:=337,unitLast:=516,order:=24576,autOrder:=1572864,parity:=1,classes:=180,raw:=4423680,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1435),
rec(k:=13652,first:=1,last:=157,unitFirst:=517,unitLast:=673,order:=24576,autOrder:=786432,parity:=3,classes:=157,raw:=3858432,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1207),
rec(k:=13653,first:=1,last:=951,unitFirst:=674,unitLast:=1624,order:=24576,autOrder:=226492416,parity:=3,classes:=951,raw:=23371776,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=3109),
rec(k:=13654,first:=1,last:=104,unitFirst:=1625,unitLast:=1728,order:=24576,autOrder:=393216,parity:=3,classes:=104,raw:=2555904,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1353),
rec(k:=13655,first:=1,last:=103,unitFirst:=1729,unitLast:=1831,order:=24576,autOrder:=393216,parity:=7,classes:=144,raw:=3538944,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1504)
];
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard234_v7_gpt56sol.g");
