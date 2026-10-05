# Exact wrapper for sealed degree-24 seed workload shard284.
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD284_SEGMENT001_UNIT1_1831_POSTVERIFY_V7_GPT56SOL.txt";
STOP_AFTER_UNIT:=fail;
INTERNAL_GUARD_MS:=1320000; START_UNIT:=1;
INITIAL_COUNTERS:=[0,0,0,0,0,0,0,0,0,0,0,0];
PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";
PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0;
PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";
CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD284_CHECKPOINT_GPT56SOL.txt";
CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD284_CHECKPOINT_TMP_GPT56SOL.txt";
EXPECTED_PROFILE_SHA256:="1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2";
EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard284_v7_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="BAE1E46D04344557CF78B42ED306FBEB034AFD0B17EDA68AF3A8F48304B00670";
S284_RECORDS:=[
rec(k:=13875,first:=647,last:=868,unitFirst:=1,unitLast:=222,order:=24576,autOrder:=786432,parity:=7,classes:=868,raw:=21331968,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1782),
rec(k:=13876,first:=1,last:=288,unitFirst:=223,unitLast:=510,order:=24576,autOrder:=25165824,parity:=7,classes:=288,raw:=7077888,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=37255),
rec(k:=13877,first:=1,last:=378,unitFirst:=511,unitLast:=888,order:=24576,autOrder:=393216,parity:=7,classes:=378,raw:=9289728,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=827),
rec(k:=13878,first:=1,last:=288,unitFirst:=889,unitLast:=1176,order:=24576,autOrder:=75497472,parity:=7,classes:=288,raw:=7077888,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=6619),
rec(k:=13879,first:=1,last:=366,unitFirst:=1177,unitLast:=1542,order:=24576,autOrder:=393216,parity:=7,classes:=366,raw:=8994816,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1345),
rec(k:=13880,first:=1,last:=96,unitFirst:=1543,unitLast:=1638,order:=24576,autOrder:=393216,parity:=3,classes:=96,raw:=2359296,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1349),
rec(k:=13881,first:=1,last:=96,unitFirst:=1639,unitLast:=1734,order:=24576,autOrder:=393216,parity:=3,classes:=96,raw:=2359296,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1322),
rec(k:=13882,first:=1,last:=97,unitFirst:=1735,unitLast:=1831,order:=24576,autOrder:=393216,parity:=7,classes:=1280,raw:=31457280,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=2350)
];
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard284_v7_gpt56sol.g");
