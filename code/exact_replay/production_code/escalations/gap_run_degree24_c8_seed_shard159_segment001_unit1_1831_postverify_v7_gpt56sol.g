# Exact wrapper for sealed degree-24 seed workload shard159.
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD159_SEGMENT001_UNIT1_1831_POSTVERIFY_V7_GPT56SOL.txt";
STOP_AFTER_UNIT:=fail;
INTERNAL_GUARD_MS:=1320000; START_UNIT:=1;
INITIAL_COUNTERS:=[0,0,0,0,0,0,0,0,0,0,0,0];
PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";
PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0;
PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";
CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD159_CHECKPOINT_GPT56SOL.txt";
CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD159_CHECKPOINT_TMP_GPT56SOL.txt";
EXPECTED_PROFILE_SHA256:="1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2";
EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard159_v7_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="8BC8E993F5C5BF5B29A686D730A4AE60C07B167E5FC54B3DB19356E3F67CA663";
S159_RECORDS:=[
rec(k:=13130,first:=252,last:=972,unitFirst:=1,unitLast:=721,order:=24576,autOrder:=3145728,parity:=7,classes:=972,raw:=23887872,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=3465),
rec(k:=13131,first:=1,last:=188,unitFirst:=722,unitLast:=909,order:=24576,autOrder:=3145728,parity:=15,classes:=188,raw:=4620288,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1925),
rec(k:=13132,first:=1,last:=40,unitFirst:=910,unitLast:=949,order:=24576,autOrder:=393216,parity:=7,classes:=40,raw:=983040,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1064),
rec(k:=13133,first:=1,last:=114,unitFirst:=950,unitLast:=1063,order:=24576,autOrder:=786432,parity:=7,classes:=114,raw:=2801664,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1566),
rec(k:=13134,first:=1,last:=768,unitFirst:=1064,unitLast:=1831,order:=24576,autOrder:=3145728,parity:=15,classes:=815,raw:=20029440,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=3127)
];
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard159_v7_gpt56sol.g");
