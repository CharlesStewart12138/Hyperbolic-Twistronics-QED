# Exact wrapper for sealed degree-24 seed workload shard183.
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD183_SEGMENT001_UNIT1_1831_POSTVERIFY_V7_GPT56SOL.txt";
STOP_AFTER_UNIT:=fail;
INTERNAL_GUARD_MS:=1320000; START_UNIT:=1;
INITIAL_COUNTERS:=[0,0,0,0,0,0,0,0,0,0,0,0];
PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";
PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0;
PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";
CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD183_CHECKPOINT_GPT56SOL.txt";
CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD183_CHECKPOINT_TMP_GPT56SOL.txt";
EXPECTED_PROFILE_SHA256:="1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2";
EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard183_v7_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="61650E67912758557374184C6730E4A57BEE40108B65FE27E627565AC3424879";
S183_RECORDS:=[
rec(k:=13347,first:=12,last:=476,unitFirst:=1,unitLast:=465,order:=24576,autOrder:=6291456,parity:=7,classes:=476,raw:=11698176,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1844),
rec(k:=13348,first:=1,last:=202,unitFirst:=466,unitLast:=667,order:=24576,autOrder:=6291456,parity:=3,classes:=202,raw:=4964352,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1874),
rec(k:=13349,first:=1,last:=204,unitFirst:=668,unitLast:=871,order:=24576,autOrder:=1572864,parity:=7,classes:=204,raw:=5013504,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1606),
rec(k:=13350,first:=1,last:=124,unitFirst:=872,unitLast:=995,order:=24576,autOrder:=786432,parity:=3,classes:=124,raw:=3047424,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1377),
rec(k:=13351,first:=1,last:=162,unitFirst:=996,unitLast:=1157,order:=24576,autOrder:=1572864,parity:=7,classes:=162,raw:=3981312,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1010),
rec(k:=13352,first:=1,last:=128,unitFirst:=1158,unitLast:=1285,order:=24576,autOrder:=786432,parity:=3,classes:=128,raw:=3145728,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1237),
rec(k:=13353,first:=1,last:=96,unitFirst:=1286,unitLast:=1381,order:=24576,autOrder:=11890851840,parity:=7,classes:=96,raw:=2359296,method:="native",representation:="pc_transport",pcOrder:=24576,profileMs:=17649),
rec(k:=13354,first:=1,last:=390,unitFirst:=1382,unitLast:=1771,order:=24576,autOrder:=1572864,parity:=3,classes:=390,raw:=9584640,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=2230),
rec(k:=13355,first:=1,last:=60,unitFirst:=1772,unitLast:=1831,order:=24576,autOrder:=9437184,parity:=7,classes:=525,raw:=12902400,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=2135)
];
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard183_v7_gpt56sol.g");
