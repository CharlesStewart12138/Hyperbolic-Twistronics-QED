# Exact wrapper for sealed degree-24 seed workload shard196.
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD196_SEGMENT001_UNIT1_1831_POSTVERIFY_V7_GPT56SOL.txt";
STOP_AFTER_UNIT:=fail;
INTERNAL_GUARD_MS:=1320000; START_UNIT:=1;
INITIAL_COUNTERS:=[0,0,0,0,0,0,0,0,0,0,0,0];
PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";
PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0;
PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";
CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD196_CHECKPOINT_GPT56SOL.txt";
CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD196_CHECKPOINT_TMP_GPT56SOL.txt";
EXPECTED_PROFILE_SHA256:="1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2";
EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard196_v7_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="2286D2D1C3593ED036DDC054AF6216FC792A9543EFF03391A4342FA5BE231609";
S196_RECORDS:=[
rec(k:=13425,first:=792,last:=960,unitFirst:=1,unitLast:=169,order:=24576,autOrder:=786432,parity:=15,classes:=960,raw:=23592960,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=2356),
rec(k:=13426,first:=1,last:=144,unitFirst:=170,unitLast:=313,order:=24576,autOrder:=786432,parity:=15,classes:=144,raw:=3538944,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1626),
rec(k:=13427,first:=1,last:=430,unitFirst:=314,unitLast:=743,order:=24576,autOrder:=2359296,parity:=15,classes:=430,raw:=10567680,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1631),
rec(k:=13428,first:=1,last:=344,unitFirst:=744,unitLast:=1087,order:=24576,autOrder:=786432,parity:=15,classes:=344,raw:=8454144,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1633),
rec(k:=13429,first:=1,last:=316,unitFirst:=1088,unitLast:=1403,order:=24576,autOrder:=6291456,parity:=15,classes:=316,raw:=7766016,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1866),
rec(k:=13430,first:=1,last:=428,unitFirst:=1404,unitLast:=1831,order:=24576,autOrder:=393216,parity:=15,classes:=512,raw:=12582912,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1939)
];
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard196_v7_gpt56sol.g");
