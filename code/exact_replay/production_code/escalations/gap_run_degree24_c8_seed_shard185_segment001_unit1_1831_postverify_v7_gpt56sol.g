# Exact wrapper for sealed degree-24 seed workload shard185.
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD185_SEGMENT001_UNIT1_1831_POSTVERIFY_V7_GPT56SOL.txt";
STOP_AFTER_UNIT:=fail;
INTERNAL_GUARD_MS:=1320000; START_UNIT:=1;
INITIAL_COUNTERS:=[0,0,0,0,0,0,0,0,0,0,0,0];
PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";
PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0;
PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";
CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD185_CHECKPOINT_GPT56SOL.txt";
CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD185_CHECKPOINT_TMP_GPT56SOL.txt";
EXPECTED_PROFILE_SHA256:="1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2";
EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard185_v7_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="E90F4CC11621185AF8F2567F363E55A624DAC70B65B166152A8163471B0F8AED";
S185_RECORDS:=[
rec(k:=13365,first:=213,last:=290,unitFirst:=1,unitLast:=78,order:=24576,autOrder:=1572864,parity:=7,classes:=290,raw:=7127040,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1617),
rec(k:=13366,first:=1,last:=206,unitFirst:=79,unitLast:=284,order:=24576,autOrder:=1572864,parity:=7,classes:=206,raw:=5062656,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1455),
rec(k:=13367,first:=1,last:=128,unitFirst:=285,unitLast:=412,order:=24576,autOrder:=393216,parity:=3,classes:=128,raw:=3145728,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1239),
rec(k:=13368,first:=1,last:=96,unitFirst:=413,unitLast:=508,order:=24576,autOrder:=393216,parity:=3,classes:=96,raw:=2359296,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1342),
rec(k:=13369,first:=1,last:=226,unitFirst:=509,unitLast:=734,order:=24576,autOrder:=1572864,parity:=7,classes:=226,raw:=5554176,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1812),
rec(k:=13370,first:=1,last:=491,unitFirst:=735,unitLast:=1225,order:=24576,autOrder:=3145728,parity:=7,classes:=491,raw:=12066816,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=2221),
rec(k:=13371,first:=1,last:=94,unitFirst:=1226,unitLast:=1319,order:=24576,autOrder:=2359296,parity:=3,classes:=94,raw:=2310144,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1331),
rec(k:=13372,first:=1,last:=110,unitFirst:=1320,unitLast:=1429,order:=24576,autOrder:=2359296,parity:=3,classes:=110,raw:=2703360,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1232),
rec(k:=13373,first:=1,last:=64,unitFirst:=1430,unitLast:=1493,order:=24576,autOrder:=1179648,parity:=3,classes:=64,raw:=1572864,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1232),
rec(k:=13374,first:=1,last:=96,unitFirst:=1494,unitLast:=1589,order:=24576,autOrder:=2359296,parity:=3,classes:=96,raw:=2359296,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1400),
rec(k:=13375,first:=1,last:=242,unitFirst:=1590,unitLast:=1831,order:=24576,autOrder:=4718592,parity:=3,classes:=420,raw:=10321920,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=2641)
];
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard185_v7_gpt56sol.g");
