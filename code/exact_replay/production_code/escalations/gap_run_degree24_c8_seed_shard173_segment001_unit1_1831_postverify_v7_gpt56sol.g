# Exact wrapper for sealed degree-24 seed workload shard173.
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD173_SEGMENT001_UNIT1_1831_POSTVERIFY_V7_GPT56SOL.txt";
STOP_AFTER_UNIT:=fail;
INTERNAL_GUARD_MS:=1320000; START_UNIT:=1;
INITIAL_COUNTERS:=[0,0,0,0,0,0,0,0,0,0,0,0];
PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";
PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0;
PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";
CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD173_CHECKPOINT_GPT56SOL.txt";
CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD173_CHECKPOINT_TMP_GPT56SOL.txt";
EXPECTED_PROFILE_SHA256:="1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2";
EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard173_v7_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="EC2ADA0F41AE08FA6B86BD7777CB62AD09268EEB54B466D7BB4528AEA3297706";
S173_RECORDS:=[
rec(k:=13244,first:=105,last:=154,unitFirst:=1,unitLast:=50,order:=24576,autOrder:=9437184,parity:=3,classes:=154,raw:=3784704,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=2265),
rec(k:=13245,first:=1,last:=112,unitFirst:=51,unitLast:=162,order:=24576,autOrder:=786432,parity:=3,classes:=112,raw:=2752512,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=2044),
rec(k:=13246,first:=1,last:=355,unitFirst:=163,unitLast:=517,order:=24576,autOrder:=18874368,parity:=3,classes:=355,raw:=8724480,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=2466),
rec(k:=13247,first:=1,last:=309,unitFirst:=518,unitLast:=826,order:=24576,autOrder:=6291456,parity:=3,classes:=309,raw:=7593984,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=2390),
rec(k:=13248,first:=1,last:=48,unitFirst:=827,unitLast:=874,order:=24576,autOrder:=2359296,parity:=3,classes:=48,raw:=1179648,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=3292),
rec(k:=13249,first:=1,last:=220,unitFirst:=875,unitLast:=1094,order:=24576,autOrder:=3145728,parity:=3,classes:=220,raw:=5406720,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=2636),
rec(k:=13250,first:=1,last:=112,unitFirst:=1095,unitLast:=1206,order:=24576,autOrder:=786432,parity:=3,classes:=112,raw:=2752512,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=2709),
rec(k:=13251,first:=1,last:=226,unitFirst:=1207,unitLast:=1432,order:=24576,autOrder:=3145728,parity:=3,classes:=226,raw:=5554176,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=2334),
rec(k:=13252,first:=1,last:=174,unitFirst:=1433,unitLast:=1606,order:=24576,autOrder:=9437184,parity:=3,classes:=174,raw:=4276224,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1700),
rec(k:=13253,first:=1,last:=214,unitFirst:=1607,unitLast:=1820,order:=24576,autOrder:=3145728,parity:=3,classes:=214,raw:=5259264,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=2801),
rec(k:=13254,first:=1,last:=11,unitFirst:=1821,unitLast:=1831,order:=24576,autOrder:=9437184,parity:=3,classes:=154,raw:=3784704,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=2444)
];
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard173_v7_gpt56sol.g");
