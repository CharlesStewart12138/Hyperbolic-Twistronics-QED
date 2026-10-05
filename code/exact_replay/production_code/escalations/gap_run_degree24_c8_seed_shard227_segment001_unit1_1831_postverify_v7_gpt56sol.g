# Exact wrapper for sealed degree-24 seed workload shard227.
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD227_SEGMENT001_UNIT1_1831_POSTVERIFY_V7_GPT56SOL.txt";
STOP_AFTER_UNIT:=fail;
INTERNAL_GUARD_MS:=1320000; START_UNIT:=1;
INITIAL_COUNTERS:=[0,0,0,0,0,0,0,0,0,0,0,0];
PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";
PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0;
PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";
CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD227_CHECKPOINT_GPT56SOL.txt";
CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD227_CHECKPOINT_TMP_GPT56SOL.txt";
EXPECTED_PROFILE_SHA256:="1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2";
EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard227_v7_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="C63FA1107151B3496D491412D017AAEF4E12749F2EA5DC000E8FA5537CD89997";
S227_RECORDS:=[
rec(k:=13606,first:=27,last:=156,unitFirst:=1,unitLast:=130,order:=24576,autOrder:=786432,parity:=3,classes:=156,raw:=3833856,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1304),
rec(k:=13607,first:=1,last:=707,unitFirst:=131,unitLast:=837,order:=24576,autOrder:=1572864,parity:=3,classes:=707,raw:=17375232,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=2170),
rec(k:=13608,first:=1,last:=132,unitFirst:=838,unitLast:=969,order:=24576,autOrder:=786432,parity:=3,classes:=132,raw:=3244032,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1606),
rec(k:=13609,first:=1,last:=192,unitFirst:=970,unitLast:=1161,order:=24576,autOrder:=393216,parity:=7,classes:=192,raw:=4718592,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1494),
rec(k:=13610,first:=1,last:=160,unitFirst:=1162,unitLast:=1321,order:=24576,autOrder:=393216,parity:=7,classes:=160,raw:=3932160,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1138),
rec(k:=13611,first:=1,last:=160,unitFirst:=1322,unitLast:=1481,order:=24576,autOrder:=393216,parity:=15,classes:=160,raw:=3932160,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1038),
rec(k:=13612,first:=1,last:=192,unitFirst:=1482,unitLast:=1673,order:=24576,autOrder:=393216,parity:=7,classes:=192,raw:=4718592,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1365),
rec(k:=13613,first:=1,last:=158,unitFirst:=1674,unitLast:=1831,order:=24576,autOrder:=393216,parity:=7,classes:=160,raw:=3932160,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=909)
];
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard227_v7_gpt56sol.g");
