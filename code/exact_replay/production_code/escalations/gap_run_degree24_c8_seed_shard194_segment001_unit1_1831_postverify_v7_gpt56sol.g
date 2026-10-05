# Exact wrapper for sealed degree-24 seed workload shard194.
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD194_SEGMENT001_UNIT1_1831_POSTVERIFY_V7_GPT56SOL.txt";
STOP_AFTER_UNIT:=fail;
INTERNAL_GUARD_MS:=1320000; START_UNIT:=1;
INITIAL_COUNTERS:=[0,0,0,0,0,0,0,0,0,0,0,0];
PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";
PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0;
PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";
CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD194_CHECKPOINT_GPT56SOL.txt";
CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD194_CHECKPOINT_TMP_GPT56SOL.txt";
EXPECTED_PROFILE_SHA256:="1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2";
EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard194_v7_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="D51D042A0B1E9088BEBF7A51F4D86A1E40EC52F068D9BC7AC81A60AFEE90BDCF";
S194_RECORDS:=[
rec(k:=13417,first:=316,last:=448,unitFirst:=1,unitLast:=133,order:=24576,autOrder:=196608,parity:=15,classes:=448,raw:=11010048,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=869),
rec(k:=13418,first:=1,last:=128,unitFirst:=134,unitLast:=261,order:=24576,autOrder:=196608,parity:=15,classes:=128,raw:=3145728,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1107),
rec(k:=13419,first:=1,last:=850,unitFirst:=262,unitLast:=1111,order:=24576,autOrder:=1572864,parity:=15,classes:=850,raw:=20889600,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=2283),
rec(k:=13420,first:=1,last:=96,unitFirst:=1112,unitLast:=1207,order:=24576,autOrder:=393216,parity:=15,classes:=96,raw:=2359296,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=945),
rec(k:=13421,first:=1,last:=560,unitFirst:=1208,unitLast:=1767,order:=24576,autOrder:=786432,parity:=15,classes:=560,raw:=13762560,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1273),
rec(k:=13422,first:=1,last:=64,unitFirst:=1768,unitLast:=1831,order:=24576,autOrder:=1179648,parity:=15,classes:=344,raw:=8454144,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1934)
];
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard194_v7_gpt56sol.g");
