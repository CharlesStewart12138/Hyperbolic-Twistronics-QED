# Exact wrapper for sealed degree-24 seed workload shard229.
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD229_SEGMENT001_UNIT1_1831_POSTVERIFY_V7_GPT56SOL.txt";
STOP_AFTER_UNIT:=fail;
INTERNAL_GUARD_MS:=1320000; START_UNIT:=1;
INITIAL_COUNTERS:=[0,0,0,0,0,0,0,0,0,0,0,0];
PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";
PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0;
PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";
CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD229_CHECKPOINT_GPT56SOL.txt";
CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD229_CHECKPOINT_TMP_GPT56SOL.txt";
EXPECTED_PROFILE_SHA256:="1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2";
EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard229_v7_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="E683C17574C9A7FAE679F9E68F94457BBD593D74EA873676483A184C8F55B3C2";
S229_RECORDS:=[
rec(k:=13624,first:=38,last:=160,unitFirst:=1,unitLast:=123,order:=24576,autOrder:=393216,parity:=7,classes:=160,raw:=3932160,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=946),
rec(k:=13625,first:=1,last:=72,unitFirst:=124,unitLast:=195,order:=24576,autOrder:=1179648,parity:=3,classes:=72,raw:=1769472,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=967),
rec(k:=13626,first:=1,last:=72,unitFirst:=196,unitLast:=267,order:=24576,autOrder:=1179648,parity:=3,classes:=72,raw:=1769472,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=894),
rec(k:=13627,first:=1,last:=104,unitFirst:=268,unitLast:=371,order:=24576,autOrder:=393216,parity:=3,classes:=104,raw:=2555904,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=833),
rec(k:=13628,first:=1,last:=138,unitFirst:=372,unitLast:=509,order:=24576,autOrder:=786432,parity:=3,classes:=138,raw:=3391488,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1357),
rec(k:=13629,first:=1,last:=48,unitFirst:=510,unitLast:=557,order:=24576,autOrder:=98304,parity:=7,classes:=48,raw:=1179648,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=889),
rec(k:=13630,first:=1,last:=48,unitFirst:=558,unitLast:=605,order:=24576,autOrder:=98304,parity:=7,classes:=48,raw:=1179648,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=914),
rec(k:=13631,first:=1,last:=72,unitFirst:=606,unitLast:=677,order:=24576,autOrder:=1179648,parity:=3,classes:=72,raw:=1769472,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=969),
rec(k:=13632,first:=1,last:=774,unitFirst:=678,unitLast:=1451,order:=24576,autOrder:=9437184,parity:=3,classes:=774,raw:=19021824,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1881),
rec(k:=13633,first:=1,last:=128,unitFirst:=1452,unitLast:=1579,order:=24576,autOrder:=393216,parity:=7,classes:=128,raw:=3145728,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1733),
rec(k:=13634,first:=1,last:=252,unitFirst:=1580,unitLast:=1831,order:=24576,autOrder:=6291456,parity:=3,classes:=560,raw:=13762560,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=2257)
];
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard229_v7_gpt56sol.g");
