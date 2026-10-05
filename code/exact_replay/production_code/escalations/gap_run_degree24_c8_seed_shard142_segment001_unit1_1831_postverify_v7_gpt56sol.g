# Exact wrapper for sealed degree-24 seed workload shard142.
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD142_SEGMENT001_UNIT1_1831_POSTVERIFY_V7_GPT56SOL.txt";
STOP_AFTER_UNIT:=fail;
INTERNAL_GUARD_MS:=1320000; START_UNIT:=1;
INITIAL_COUNTERS:=[0,0,0,0,0,0,0,0,0,0,0,0];
PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";
PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0;
PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";
CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD142_CHECKPOINT_GPT56SOL.txt";
CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD142_CHECKPOINT_TMP_GPT56SOL.txt";
EXPECTED_PROFILE_SHA256:="1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2";
EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard142_v7_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="3AC28895DFB196E464C26644B62F21E923434D380FCB4C7B1662E3A6DC2677E1";
S142_RECORDS:=[
rec(k:=12972,first:=1218,last:=1700,unitFirst:=1,unitLast:=483,order:=24576,autOrder:=50331648,parity:=3,classes:=1700,raw:=41779200,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=5550),
rec(k:=12973,first:=1,last:=156,unitFirst:=484,unitLast:=639,order:=24576,autOrder:=3145728,parity:=1,classes:=156,raw:=3833856,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1610),
rec(k:=12974,first:=1,last:=206,unitFirst:=640,unitLast:=845,order:=24576,autOrder:=1572864,parity:=7,classes:=206,raw:=5062656,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1239),
rec(k:=12975,first:=1,last:=148,unitFirst:=846,unitLast:=993,order:=24576,autOrder:=786432,parity:=7,classes:=148,raw:=3637248,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1116),
rec(k:=12976,first:=1,last:=144,unitFirst:=994,unitLast:=1137,order:=24576,autOrder:=786432,parity:=1,classes:=144,raw:=3538944,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1710),
rec(k:=12977,first:=1,last:=164,unitFirst:=1138,unitLast:=1301,order:=24576,autOrder:=786432,parity:=7,classes:=164,raw:=4030464,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1295),
rec(k:=12978,first:=1,last:=96,unitFirst:=1302,unitLast:=1397,order:=24576,autOrder:=393216,parity:=3,classes:=96,raw:=2359296,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1567),
rec(k:=12979,first:=1,last:=136,unitFirst:=1398,unitLast:=1533,order:=24576,autOrder:=1572864,parity:=1,classes:=136,raw:=3342336,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=2082),
rec(k:=12980,first:=1,last:=60,unitFirst:=1534,unitLast:=1593,order:=24576,autOrder:=393216,parity:=1,classes:=60,raw:=1474560,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=919),
rec(k:=12981,first:=1,last:=238,unitFirst:=1594,unitLast:=1831,order:=24576,autOrder:=3145728,parity:=1,classes:=420,raw:=10321920,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1563)
];
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard142_v7_gpt56sol.g");
