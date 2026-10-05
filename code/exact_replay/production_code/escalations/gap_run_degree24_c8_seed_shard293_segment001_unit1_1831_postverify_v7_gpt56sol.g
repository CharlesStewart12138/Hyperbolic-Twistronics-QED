# Exact wrapper for sealed degree-24 seed workload shard293.
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD293_SEGMENT001_UNIT1_1831_POSTVERIFY_V7_GPT56SOL.txt";
STOP_AFTER_UNIT:=fail;
INTERNAL_GUARD_MS:=1320000; START_UNIT:=1;
INITIAL_COUNTERS:=[0,0,0,0,0,0,0,0,0,0,0,0];
PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";
PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0;
PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";
CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD293_CHECKPOINT_GPT56SOL.txt";
CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD293_CHECKPOINT_TMP_GPT56SOL.txt";
EXPECTED_PROFILE_SHA256:="1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2";
EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard293_v7_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="AE3231457EB3601833F719F2EACA893225515D03BA827EFB5684D0EBB25902D8";
S293_RECORDS:=[
rec(k:=13913,first:=13,last:=112,unitFirst:=1,unitLast:=100,order:=24576,autOrder:=786432,parity:=7,classes:=112,raw:=2752512,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1389),
rec(k:=13914,first:=1,last:=292,unitFirst:=101,unitLast:=392,order:=24576,autOrder:=196608,parity:=3,classes:=292,raw:=7176192,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=962),
rec(k:=13915,first:=1,last:=112,unitFirst:=393,unitLast:=504,order:=24576,autOrder:=786432,parity:=3,classes:=112,raw:=2752512,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1945),
rec(k:=13916,first:=1,last:=366,unitFirst:=505,unitLast:=870,order:=24576,autOrder:=393216,parity:=7,classes:=366,raw:=8994816,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1322),
rec(k:=13917,first:=1,last:=112,unitFirst:=871,unitLast:=982,order:=24576,autOrder:=786432,parity:=3,classes:=112,raw:=2752512,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1579),
rec(k:=13918,first:=1,last:=268,unitFirst:=983,unitLast:=1250,order:=24576,autOrder:=196608,parity:=3,classes:=268,raw:=6586368,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=947),
rec(k:=13919,first:=1,last:=96,unitFirst:=1251,unitLast:=1346,order:=24576,autOrder:=393216,parity:=3,classes:=96,raw:=2359296,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1495),
rec(k:=13920,first:=1,last:=96,unitFirst:=1347,unitLast:=1442,order:=24576,autOrder:=393216,parity:=3,classes:=96,raw:=2359296,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=2015),
rec(k:=13921,first:=1,last:=389,unitFirst:=1443,unitLast:=1831,order:=24576,autOrder:=196608,parity:=7,classes:=392,raw:=9633792,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1086)
];
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard293_v7_gpt56sol.g");
