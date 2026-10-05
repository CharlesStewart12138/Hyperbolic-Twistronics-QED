# Exact wrapper for sealed degree-24 seed workload shard341.
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD341_SEGMENT001_UNIT1_915_POSTVERIFY_V7_GPT56SOL.txt";
STOP_AFTER_UNIT:=fail;
INTERNAL_GUARD_MS:=1320000; START_UNIT:=1;
INITIAL_COUNTERS:=[0,0,0,0,0,0,0,0,0,0,0,0];
PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";
PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0;
PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";
CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD341_CHECKPOINT_GPT56SOL.txt";
CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD341_CHECKPOINT_TMP_GPT56SOL.txt";
EXPECTED_PROFILE_SHA256:="1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2";
EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard341_v7_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="FFA5BE878DEFE31F06B1C466F378F8C39C49ED42B5B1E73A939AD24B762C4EC9";
S341_RECORDS:=[
rec(k:=14811,first:=131,last:=240,unitFirst:=1,unitLast:=110,order:=49152,autOrder:=3145728,parity:=7,classes:=240,raw:=11796480,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1928),
rec(k:=14812,first:=1,last:=236,unitFirst:=111,unitLast:=346,order:=49152,autOrder:=3145728,parity:=7,classes:=236,raw:=11599872,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=2569),
rec(k:=14813,first:=1,last:=64,unitFirst:=347,unitLast:=410,order:=49152,autOrder:=1572864,parity:=7,classes:=64,raw:=3145728,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1511),
rec(k:=14814,first:=1,last:=128,unitFirst:=411,unitLast:=538,order:=49152,autOrder:=4718592,parity:=7,classes:=128,raw:=6291456,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1018),
rec(k:=14815,first:=1,last:=40,unitFirst:=539,unitLast:=578,order:=49152,autOrder:=393216,parity:=7,classes:=40,raw:=1966080,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=842),
rec(k:=14816,first:=1,last:=96,unitFirst:=579,unitLast:=674,order:=49152,autOrder:=393216,parity:=3,classes:=96,raw:=4718592,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=883),
rec(k:=14817,first:=1,last:=48,unitFirst:=675,unitLast:=722,order:=49152,autOrder:=393216,parity:=3,classes:=48,raw:=2359296,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1611),
rec(k:=14818,first:=1,last:=32,unitFirst:=723,unitLast:=754,order:=49152,autOrder:=393216,parity:=15,classes:=32,raw:=1572864,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1044),
rec(k:=14819,first:=1,last:=161,unitFirst:=755,unitLast:=915,order:=49152,autOrder:=3145728,parity:=3,classes:=240,raw:=11796480,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=2711)
];
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard341_v7_gpt56sol.g");
