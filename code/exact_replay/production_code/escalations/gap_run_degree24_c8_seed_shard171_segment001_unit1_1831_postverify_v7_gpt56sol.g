# Exact wrapper for sealed degree-24 seed workload shard171.
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD171_SEGMENT001_UNIT1_1831_POSTVERIFY_V7_GPT56SOL.txt";
STOP_AFTER_UNIT:=fail;
INTERNAL_GUARD_MS:=1320000; START_UNIT:=1;
INITIAL_COUNTERS:=[0,0,0,0,0,0,0,0,0,0,0,0];
PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";
PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0;
PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";
CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD171_CHECKPOINT_GPT56SOL.txt";
CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD171_CHECKPOINT_TMP_GPT56SOL.txt";
EXPECTED_PROFILE_SHA256:="1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2";
EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard171_v7_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="036C94F7E462E5280A9DC58E336D1B9794AD01E860357FF679BFEDB0FE25217F";
S171_RECORDS:=[
rec(k:=13222,first:=12,last:=188,unitFirst:=1,unitLast:=177,order:=24576,autOrder:=3145728,parity:=3,classes:=188,raw:=4620288,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1340),
rec(k:=13223,first:=1,last:=48,unitFirst:=178,unitLast:=225,order:=24576,autOrder:=786432,parity:=3,classes:=48,raw:=1179648,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1607),
rec(k:=13224,first:=1,last:=202,unitFirst:=226,unitLast:=427,order:=24576,autOrder:=6291456,parity:=3,classes:=202,raw:=4964352,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1750),
rec(k:=13225,first:=1,last:=48,unitFirst:=428,unitLast:=475,order:=24576,autOrder:=786432,parity:=3,classes:=48,raw:=1179648,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=2677),
rec(k:=13226,first:=1,last:=261,unitFirst:=476,unitLast:=736,order:=24576,autOrder:=6291456,parity:=3,classes:=261,raw:=6414336,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=2407),
rec(k:=13227,first:=1,last:=128,unitFirst:=737,unitLast:=864,order:=24576,autOrder:=393216,parity:=3,classes:=128,raw:=3145728,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1324),
rec(k:=13228,first:=1,last:=112,unitFirst:=865,unitLast:=976,order:=24576,autOrder:=786432,parity:=7,classes:=112,raw:=2752512,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1541),
rec(k:=13229,first:=1,last:=174,unitFirst:=977,unitLast:=1150,order:=24576,autOrder:=786432,parity:=3,classes:=174,raw:=4276224,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1107),
rec(k:=13230,first:=1,last:=236,unitFirst:=1151,unitLast:=1386,order:=24576,autOrder:=3145728,parity:=15,classes:=236,raw:=5799936,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1772),
rec(k:=13231,first:=1,last:=206,unitFirst:=1387,unitLast:=1592,order:=24576,autOrder:=786432,parity:=3,classes:=206,raw:=5062656,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=2059),
rec(k:=13232,first:=1,last:=239,unitFirst:=1593,unitLast:=1831,order:=24576,autOrder:=6291456,parity:=15,classes:=347,raw:=8527872,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1696)
];
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard171_v7_gpt56sol.g");
