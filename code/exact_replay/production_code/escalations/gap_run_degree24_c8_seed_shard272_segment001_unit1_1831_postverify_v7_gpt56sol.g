# Exact wrapper for sealed degree-24 seed workload shard272.
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD272_SEGMENT001_UNIT1_1831_POSTVERIFY_V7_GPT56SOL.txt";
STOP_AFTER_UNIT:=fail;
INTERNAL_GUARD_MS:=1320000; START_UNIT:=1;
INITIAL_COUNTERS:=[0,0,0,0,0,0,0,0,0,0,0,0];
PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";
PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0;
PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";
CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD272_CHECKPOINT_GPT56SOL.txt";
CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD272_CHECKPOINT_TMP_GPT56SOL.txt";
EXPECTED_PROFILE_SHA256:="1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2";
EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard272_v7_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="0A0F64D828AEFDD8936B47B9A133AE3E3F00C2CF55AF168121591F05DEE6ED42";
S272_RECORDS:=[
rec(k:=13799,first:=105,last:=428,unitFirst:=1,unitLast:=324,order:=24576,autOrder:=786432,parity:=1,classes:=428,raw:=10518528,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1099),
rec(k:=13800,first:=1,last:=585,unitFirst:=325,unitLast:=909,order:=24576,autOrder:=1572864,parity:=1,classes:=585,raw:=14376960,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1488),
rec(k:=13801,first:=1,last:=137,unitFirst:=910,unitLast:=1046,order:=24576,autOrder:=1572864,parity:=1,classes:=137,raw:=3366912,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1204),
rec(k:=13802,first:=1,last:=428,unitFirst:=1047,unitLast:=1474,order:=24576,autOrder:=786432,parity:=1,classes:=428,raw:=10518528,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1765),
rec(k:=13803,first:=1,last:=356,unitFirst:=1475,unitLast:=1830,order:=24576,autOrder:=393216,parity:=1,classes:=356,raw:=8749056,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1001),
rec(k:=13804,first:=1,last:=1,unitFirst:=1831,unitLast:=1831,order:=24576,autOrder:=786432,parity:=1,classes:=428,raw:=10518528,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1151)
];
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard272_v7_gpt56sol.g");
