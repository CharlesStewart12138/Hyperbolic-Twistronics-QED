# Exact wrapper for sealed degree-24 seed workload shard105.
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD105_SEGMENT001_UNIT1_3662_POSTVERIFY_V7_GPT56SOL.txt";
STOP_AFTER_UNIT:=fail;
INTERNAL_GUARD_MS:=1320000; START_UNIT:=1;
INITIAL_COUNTERS:=[0,0,0,0,0,0,0,0,0,0,0,0];
PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";
PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0;
PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";
CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD105_CHECKPOINT_GPT56SOL.txt";
CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD105_CHECKPOINT_TMP_GPT56SOL.txt";
EXPECTED_PROFILE_SHA256:="1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2";
EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard105_v7_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="A2F7E5CEB6513D0C484412661A746E1D0B61F4EC7AB7D65A22309D6C8D331ACF";
S105_RECORDS:=[
rec(k:=11949,first:=26,last:=220,unitFirst:=1,unitLast:=195,order:=12288,autOrder:=98304,parity:=3,classes:=220,raw:=2703360,method:="pc",representation:="pc_transport",pcOrder:=12288,profileMs:=815),
rec(k:=11950,first:=1,last:=322,unitFirst:=196,unitLast:=517,order:=12288,autOrder:=1572864,parity:=7,classes:=322,raw:=3956736,method:="pc",representation:="pc_transport",pcOrder:=12288,profileMs:=1946),
rec(k:=11951,first:=1,last:=256,unitFirst:=518,unitLast:=773,order:=12288,autOrder:=393216,parity:=3,classes:=256,raw:=3145728,method:="pc",representation:="pc_transport",pcOrder:=12288,profileMs:=1515),
rec(k:=11952,first:=1,last:=368,unitFirst:=774,unitLast:=1141,order:=12288,autOrder:=786432,parity:=3,classes:=368,raw:=4521984,method:="pc",representation:="pc_transport",pcOrder:=12288,profileMs:=1441),
rec(k:=11953,first:=1,last:=256,unitFirst:=1142,unitLast:=1397,order:=12288,autOrder:=393216,parity:=3,classes:=256,raw:=3145728,method:="pc",representation:="pc_transport",pcOrder:=12288,profileMs:=1554),
rec(k:=11954,first:=1,last:=220,unitFirst:=1398,unitLast:=1617,order:=12288,autOrder:=98304,parity:=3,classes:=220,raw:=2703360,method:="pc",representation:="pc_transport",pcOrder:=12288,profileMs:=916),
rec(k:=11955,first:=1,last:=184,unitFirst:=1618,unitLast:=1801,order:=12288,autOrder:=196608,parity:=3,classes:=184,raw:=2260992,method:="pc",representation:="pc_transport",pcOrder:=12288,profileMs:=908),
rec(k:=11956,first:=1,last:=220,unitFirst:=1802,unitLast:=2021,order:=12288,autOrder:=98304,parity:=3,classes:=220,raw:=2703360,method:="pc",representation:="pc_transport",pcOrder:=12288,profileMs:=794),
rec(k:=11957,first:=1,last:=184,unitFirst:=2022,unitLast:=2205,order:=12288,autOrder:=196608,parity:=3,classes:=184,raw:=2260992,method:="pc",representation:="pc_transport",pcOrder:=12288,profileMs:=771),
rec(k:=11958,first:=1,last:=546,unitFirst:=2206,unitLast:=2751,order:=12288,autOrder:=3145728,parity:=7,classes:=546,raw:=6709248,method:="pc",representation:="pc_transport",pcOrder:=12288,profileMs:=1622),
rec(k:=11959,first:=1,last:=512,unitFirst:=2752,unitLast:=3263,order:=12288,autOrder:=393216,parity:=3,classes:=512,raw:=6291456,method:="pc",representation:="pc_transport",pcOrder:=12288,profileMs:=1745),
rec(k:=11960,first:=1,last:=399,unitFirst:=3264,unitLast:=3662,order:=12288,autOrder:=1572864,parity:=3,classes:=624,raw:=7667712,method:="pc",representation:="pc_transport",pcOrder:=12288,profileMs:=2285)
];
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard105_v7_gpt56sol.g");
