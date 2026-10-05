# Exact wrapper for sealed degree-24 seed workload shard138.
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD138_SEGMENT001_UNIT1_1831_POSTVERIFY_V7_GPT56SOL.txt";
STOP_AFTER_UNIT:=fail;
INTERNAL_GUARD_MS:=1320000; START_UNIT:=1;
INITIAL_COUNTERS:=[0,0,0,0,0,0,0,0,0,0,0,0];
PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";
PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0;
PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";
CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD138_CHECKPOINT_GPT56SOL.txt";
CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD138_CHECKPOINT_TMP_GPT56SOL.txt";
EXPECTED_PROFILE_SHA256:="1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2";
EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard138_v7_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="0BED79BBE5ACD963CA0F6F0EAFEBAC911C21687E097C2B9598D925B5386DAED7";
S138_RECORDS:=[
rec(k:=12942,first:=15,last:=592,unitFirst:=1,unitLast:=578,order:=24576,autOrder:=786432,parity:=3,classes:=592,raw:=14548992,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1686),
rec(k:=12943,first:=1,last:=242,unitFirst:=579,unitLast:=820,order:=24576,autOrder:=1572864,parity:=1,classes:=242,raw:=5947392,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1099),
rec(k:=12944,first:=1,last:=160,unitFirst:=821,unitLast:=980,order:=24576,autOrder:=786432,parity:=1,classes:=160,raw:=3932160,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1547),
rec(k:=12945,first:=1,last:=104,unitFirst:=981,unitLast:=1084,order:=24576,autOrder:=1572864,parity:=1,classes:=104,raw:=2555904,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1327),
rec(k:=12946,first:=1,last:=560,unitFirst:=1085,unitLast:=1644,order:=24576,autOrder:=6291456,parity:=3,classes:=560,raw:=13762560,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1671),
rec(k:=12947,first:=1,last:=137,unitFirst:=1645,unitLast:=1781,order:=24576,autOrder:=1572864,parity:=1,classes:=137,raw:=3366912,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=797),
rec(k:=12948,first:=1,last:=50,unitFirst:=1782,unitLast:=1831,order:=24576,autOrder:=1572864,parity:=1,classes:=180,raw:=4423680,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1376)
];
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard138_v7_gpt56sol.g");
