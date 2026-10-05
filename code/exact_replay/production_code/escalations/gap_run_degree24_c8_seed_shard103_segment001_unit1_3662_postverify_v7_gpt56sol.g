# Exact wrapper for sealed degree-24 seed workload shard103.
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD103_SEGMENT001_UNIT1_3662_POSTVERIFY_V7_GPT56SOL.txt";
STOP_AFTER_UNIT:=fail;
INTERNAL_GUARD_MS:=1320000; START_UNIT:=1;
INITIAL_COUNTERS:=[0,0,0,0,0,0,0,0,0,0,0,0];
PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";
PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0;
PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";
CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD103_CHECKPOINT_GPT56SOL.txt";
CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD103_CHECKPOINT_TMP_GPT56SOL.txt";
EXPECTED_PROFILE_SHA256:="1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2";
EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard103_v7_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="38EDC5C5C6FD09F843A06542ED460241F6386F077E5A6DDD88650758E1C59E2E";
S103_RECORDS:=[
rec(k:=11919,first:=271,last:=412,unitFirst:=1,unitLast:=142,order:=12288,autOrder:=393216,parity:=3,classes:=412,raw:=5062656,method:="pc",representation:="pc_transport",pcOrder:=12288,profileMs:=1059),
rec(k:=11920,first:=1,last:=414,unitFirst:=143,unitLast:=556,order:=12288,autOrder:=25165824,parity:=7,classes:=414,raw:=5087232,method:="pc",representation:="pc_transport",pcOrder:=12288,profileMs:=5156),
rec(k:=11921,first:=1,last:=48,unitFirst:=557,unitLast:=604,order:=12288,autOrder:=6291456,parity:=3,classes:=48,raw:=589824,method:="pc",representation:="pc_transport",pcOrder:=12288,profileMs:=10394),
rec(k:=11922,first:=1,last:=224,unitFirst:=605,unitLast:=828,order:=12288,autOrder:=49152,parity:=7,classes:=224,raw:=2752512,method:="pc",representation:="pc_transport",pcOrder:=12288,profileMs:=933),
rec(k:=11923,first:=1,last:=260,unitFirst:=829,unitLast:=1088,order:=12288,autOrder:=196608,parity:=7,classes:=260,raw:=3194880,method:="pc",representation:="pc_transport",pcOrder:=12288,profileMs:=910),
rec(k:=11924,first:=1,last:=72,unitFirst:=1089,unitLast:=1160,order:=12288,autOrder:=49152,parity:=7,classes:=72,raw:=884736,method:="pc",representation:="pc_transport",pcOrder:=12288,profileMs:=740),
rec(k:=11925,first:=1,last:=78,unitFirst:=1161,unitLast:=1238,order:=12288,autOrder:=196608,parity:=7,classes:=78,raw:=958464,method:="pc",representation:="pc_transport",pcOrder:=12288,profileMs:=735),
rec(k:=11926,first:=1,last:=22,unitFirst:=1239,unitLast:=1260,order:=12288,autOrder:=196608,parity:=7,classes:=22,raw:=270336,method:="pc",representation:="pc_transport",pcOrder:=12288,profileMs:=546),
rec(k:=11927,first:=1,last:=200,unitFirst:=1261,unitLast:=1460,order:=12288,autOrder:=98304,parity:=7,classes:=200,raw:=2457600,method:="pc",representation:="pc_transport",pcOrder:=12288,profileMs:=869),
rec(k:=11928,first:=1,last:=640,unitFirst:=1461,unitLast:=2100,order:=12288,autOrder:=196608,parity:=3,classes:=640,raw:=7864320,method:="pc",representation:="pc_transport",pcOrder:=12288,profileMs:=1277),
rec(k:=11929,first:=1,last:=640,unitFirst:=2101,unitLast:=2740,order:=12288,autOrder:=196608,parity:=3,classes:=640,raw:=7864320,method:="pc",representation:="pc_transport",pcOrder:=12288,profileMs:=1168),
rec(k:=11930,first:=1,last:=434,unitFirst:=2741,unitLast:=3174,order:=12288,autOrder:=393216,parity:=3,classes:=434,raw:=5332992,method:="pc",representation:="pc_transport",pcOrder:=12288,profileMs:=1206),
rec(k:=11931,first:=1,last:=220,unitFirst:=3175,unitLast:=3394,order:=12288,autOrder:=196608,parity:=7,classes:=220,raw:=2703360,method:="pc",representation:="pc_transport",pcOrder:=12288,profileMs:=655),
rec(k:=11932,first:=1,last:=268,unitFirst:=3395,unitLast:=3662,order:=12288,autOrder:=393216,parity:=3,classes:=434,raw:=5332992,method:="pc",representation:="pc_transport",pcOrder:=12288,profileMs:=1147)
];
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard103_v7_gpt56sol.g");
