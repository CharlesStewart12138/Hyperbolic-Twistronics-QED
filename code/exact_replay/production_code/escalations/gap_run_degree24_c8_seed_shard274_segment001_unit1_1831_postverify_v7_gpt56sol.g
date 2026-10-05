# Exact wrapper for sealed degree-24 seed workload shard274.
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD274_SEGMENT001_UNIT1_1831_POSTVERIFY_V7_GPT56SOL.txt";
STOP_AFTER_UNIT:=fail;
INTERNAL_GUARD_MS:=1320000; START_UNIT:=1;
INITIAL_COUNTERS:=[0,0,0,0,0,0,0,0,0,0,0,0];
PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";
PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0;
PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";
CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD274_CHECKPOINT_GPT56SOL.txt";
CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD274_CHECKPOINT_TMP_GPT56SOL.txt";
EXPECTED_PROFILE_SHA256:="1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2";
EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard274_v7_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="7E794FC48B9A7EA37B65897CA994BB4FB9927E19B85FBE2F64B99EB5F24B3E80";
S274_RECORDS:=[
rec(k:=13807,first:=320,last:=585,unitFirst:=1,unitLast:=266,order:=24576,autOrder:=1572864,parity:=1,classes:=585,raw:=14376960,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1524),
rec(k:=13808,first:=1,last:=137,unitFirst:=267,unitLast:=403,order:=24576,autOrder:=1572864,parity:=1,classes:=137,raw:=3366912,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1045),
rec(k:=13809,first:=1,last:=60,unitFirst:=404,unitLast:=463,order:=24576,autOrder:=393216,parity:=1,classes:=60,raw:=1474560,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=791),
rec(k:=13810,first:=1,last:=137,unitFirst:=464,unitLast:=600,order:=24576,autOrder:=1572864,parity:=1,classes:=137,raw:=3366912,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=896),
rec(k:=13811,first:=1,last:=212,unitFirst:=601,unitLast:=812,order:=24576,autOrder:=9437184,parity:=1,classes:=212,raw:=5210112,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1347),
rec(k:=13812,first:=1,last:=144,unitFirst:=813,unitLast:=956,order:=24576,autOrder:=1572864,parity:=1,classes:=144,raw:=3538944,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1125),
rec(k:=13813,first:=1,last:=468,unitFirst:=957,unitLast:=1424,order:=24576,autOrder:=3145728,parity:=1,classes:=468,raw:=11501568,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=2928),
rec(k:=13814,first:=1,last:=356,unitFirst:=1425,unitLast:=1780,order:=24576,autOrder:=393216,parity:=1,classes:=356,raw:=8749056,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=935),
rec(k:=13815,first:=1,last:=51,unitFirst:=1781,unitLast:=1831,order:=24576,autOrder:=786432,parity:=1,classes:=476,raw:=11698176,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1013)
];
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard274_v7_gpt56sol.g");
