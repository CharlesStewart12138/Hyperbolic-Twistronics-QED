# Exact wrapper for sealed degree-24 seed workload shard205.
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD205_SEGMENT001_UNIT1_1831_POSTVERIFY_V7_GPT56SOL.txt";
STOP_AFTER_UNIT:=fail;
INTERNAL_GUARD_MS:=1320000; START_UNIT:=1;
INITIAL_COUNTERS:=[0,0,0,0,0,0,0,0,0,0,0,0];
PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";
PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0;
PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";
CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD205_CHECKPOINT_GPT56SOL.txt";
CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD205_CHECKPOINT_TMP_GPT56SOL.txt";
EXPECTED_PROFILE_SHA256:="1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2";
EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard205_v7_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="ED75EEBDF85A255D9547D5A9C41BE7C0BB3B86375F9165AECB6E37146FA57D29";
S205_RECORDS:=[
rec(k:=13470,first:=9,last:=1180,unitFirst:=1,unitLast:=1172,order:=24576,autOrder:=3145728,parity:=7,classes:=1180,raw:=28999680,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=3163),
rec(k:=13471,first:=1,last:=200,unitFirst:=1173,unitLast:=1372,order:=24576,autOrder:=6291456,parity:=3,classes:=200,raw:=4915200,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1926),
rec(k:=13472,first:=1,last:=64,unitFirst:=1373,unitLast:=1436,order:=24576,autOrder:=786432,parity:=3,classes:=64,raw:=1572864,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1244),
rec(k:=13473,first:=1,last:=136,unitFirst:=1437,unitLast:=1572,order:=24576,autOrder:=786432,parity:=3,classes:=136,raw:=3342336,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1836),
rec(k:=13474,first:=1,last:=259,unitFirst:=1573,unitLast:=1831,order:=24576,autOrder:=1572864,parity:=7,classes:=370,raw:=9093120,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1514)
];
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard205_v7_gpt56sol.g");
