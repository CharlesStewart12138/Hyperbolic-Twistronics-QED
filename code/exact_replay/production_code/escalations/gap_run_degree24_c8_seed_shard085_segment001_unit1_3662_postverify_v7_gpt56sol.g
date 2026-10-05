# Exact wrapper for sealed degree-24 seed workload shard085.
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD085_SEGMENT001_UNIT1_3662_POSTVERIFY_V7_GPT56SOL.txt";
STOP_AFTER_UNIT:=fail;
INTERNAL_GUARD_MS:=1320000; START_UNIT:=1;
INITIAL_COUNTERS:=[0,0,0,0,0,0,0,0,0,0,0,0];
PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";
PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0;
PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";
CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD085_CHECKPOINT_GPT56SOL.txt";
CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD085_CHECKPOINT_TMP_GPT56SOL.txt";
EXPECTED_PROFILE_SHA256:="1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2";
EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard085_v7_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="2EE6DF94FF79D0C9057588939BED4B82210CB5D7A77C4E49769DC24DA0D261D5";
S085_RECORDS:=[
rec(k:=11558,first:=352,last:=384,unitFirst:=1,unitLast:=33,order:=12288,autOrder:=393216,parity:=7,classes:=384,raw:=4718592,method:="pc",representation:="pc_transport",pcOrder:=12288,profileMs:=1036),
rec(k:=11559,first:=1,last:=256,unitFirst:=34,unitLast:=289,order:=12288,autOrder:=196608,parity:=7,classes:=256,raw:=3145728,method:="pc",representation:="pc_transport",pcOrder:=12288,profileMs:=984),
rec(k:=11560,first:=1,last:=160,unitFirst:=290,unitLast:=449,order:=12288,autOrder:=196608,parity:=7,classes:=160,raw:=1966080,method:="pc",representation:="pc_transport",pcOrder:=12288,profileMs:=905),
rec(k:=11561,first:=1,last:=384,unitFirst:=450,unitLast:=833,order:=12288,autOrder:=196608,parity:=7,classes:=384,raw:=4718592,method:="pc",representation:="pc_transport",pcOrder:=12288,profileMs:=1224),
rec(k:=11562,first:=1,last:=328,unitFirst:=834,unitLast:=1161,order:=12288,autOrder:=393216,parity:=7,classes:=328,raw:=4030464,method:="pc",representation:="pc_transport",pcOrder:=12288,profileMs:=1218),
rec(k:=11563,first:=1,last:=384,unitFirst:=1162,unitLast:=1545,order:=12288,autOrder:=393216,parity:=7,classes:=384,raw:=4718592,method:="pc",representation:="pc_transport",pcOrder:=12288,profileMs:=1161),
rec(k:=11564,first:=1,last:=400,unitFirst:=1546,unitLast:=1945,order:=12288,autOrder:=786432,parity:=7,classes:=400,raw:=4915200,method:="pc",representation:="pc_transport",pcOrder:=12288,profileMs:=1646),
rec(k:=11565,first:=1,last:=380,unitFirst:=1946,unitLast:=2325,order:=12288,autOrder:=1179648,parity:=7,classes:=380,raw:=4669440,method:="pc",representation:="pc_transport",pcOrder:=12288,profileMs:=1152),
rec(k:=11566,first:=1,last:=256,unitFirst:=2326,unitLast:=2581,order:=12288,autOrder:=196608,parity:=7,classes:=256,raw:=3145728,method:="pc",representation:="pc_transport",pcOrder:=12288,profileMs:=1033),
rec(k:=11567,first:=1,last:=480,unitFirst:=2582,unitLast:=3061,order:=12288,autOrder:=393216,parity:=7,classes:=480,raw:=5898240,method:="pc",representation:="pc_transport",pcOrder:=12288,profileMs:=1136),
rec(k:=11568,first:=1,last:=172,unitFirst:=3062,unitLast:=3233,order:=12288,autOrder:=589824,parity:=7,classes:=172,raw:=2113536,method:="pc",representation:="pc_transport",pcOrder:=12288,profileMs:=732),
rec(k:=11569,first:=1,last:=128,unitFirst:=3234,unitLast:=3361,order:=12288,autOrder:=98304,parity:=7,classes:=128,raw:=1572864,method:="pc",representation:="pc_transport",pcOrder:=12288,profileMs:=1150),
rec(k:=11570,first:=1,last:=301,unitFirst:=3362,unitLast:=3662,order:=12288,autOrder:=196608,parity:=7,classes:=320,raw:=3932160,method:="pc",representation:="pc_transport",pcOrder:=12288,profileMs:=1083)
];
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard085_v7_gpt56sol.g");
