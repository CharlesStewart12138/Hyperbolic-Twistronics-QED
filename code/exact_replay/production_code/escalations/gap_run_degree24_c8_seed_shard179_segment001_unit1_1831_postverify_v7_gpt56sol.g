# Exact wrapper for sealed degree-24 seed workload shard179.
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD179_SEGMENT001_UNIT1_1831_POSTVERIFY_V7_GPT56SOL.txt";
STOP_AFTER_UNIT:=fail;
INTERNAL_GUARD_MS:=1320000; START_UNIT:=1;
INITIAL_COUNTERS:=[0,0,0,0,0,0,0,0,0,0,0,0];
PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";
PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0;
PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";
CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD179_CHECKPOINT_GPT56SOL.txt";
CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD179_CHECKPOINT_TMP_GPT56SOL.txt";
EXPECTED_PROFILE_SHA256:="1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2";
EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard179_v7_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="1F4CAB8C98EBE93C395D49B01B49B4F49BFF8AAD9F89303AF5E4964BF27A0632";
S179_RECORDS:=[
rec(k:=13304,first:=55,last:=64,unitFirst:=1,unitLast:=10,order:=24576,autOrder:=98304,parity:=3,classes:=64,raw:=1572864,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=796),
rec(k:=13305,first:=1,last:=128,unitFirst:=11,unitLast:=138,order:=24576,autOrder:=393216,parity:=7,classes:=128,raw:=3145728,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=868),
rec(k:=13306,first:=1,last:=512,unitFirst:=139,unitLast:=650,order:=24576,autOrder:=393216,parity:=7,classes:=512,raw:=12582912,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1828),
rec(k:=13307,first:=1,last:=128,unitFirst:=651,unitLast:=778,order:=24576,autOrder:=393216,parity:=7,classes:=128,raw:=3145728,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1265),
rec(k:=13308,first:=1,last:=448,unitFirst:=779,unitLast:=1226,order:=24576,autOrder:=393216,parity:=7,classes:=448,raw:=11010048,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1074),
rec(k:=13309,first:=1,last:=128,unitFirst:=1227,unitLast:=1354,order:=24576,autOrder:=393216,parity:=7,classes:=128,raw:=3145728,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=884),
rec(k:=13310,first:=1,last:=448,unitFirst:=1355,unitLast:=1802,order:=24576,autOrder:=393216,parity:=7,classes:=448,raw:=11010048,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1088),
rec(k:=13311,first:=1,last:=29,unitFirst:=1803,unitLast:=1831,order:=24576,autOrder:=393216,parity:=7,classes:=128,raw:=3145728,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1409)
];
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard179_v7_gpt56sol.g");
