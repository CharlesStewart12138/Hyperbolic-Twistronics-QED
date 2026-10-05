# Exact wrapper for sealed degree-24 seed workload shard101.
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD101_SEGMENT001_UNIT1_3662_POSTVERIFY_V7_GPT56SOL.txt";
STOP_AFTER_UNIT:=fail;
INTERNAL_GUARD_MS:=1320000; START_UNIT:=1;
INITIAL_COUNTERS:=[0,0,0,0,0,0,0,0,0,0,0,0];
PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";
PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0;
PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";
CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD101_CHECKPOINT_GPT56SOL.txt";
CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD101_CHECKPOINT_TMP_GPT56SOL.txt";
EXPECTED_PROFILE_SHA256:="1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2";
EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard101_v7_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="6582992A97B5437C5B550177C5DC091C11973078FB9674AB96DD0B79BA290F05";
S101_RECORDS:=[
rec(k:=11890,first:=38,last:=62,unitFirst:=1,unitLast:=25,order:=12288,autOrder:=196608,parity:=7,classes:=62,raw:=761856,method:="pc",representation:="pc_transport",pcOrder:=12288,profileMs:=735),
rec(k:=11891,first:=1,last:=20,unitFirst:=26,unitLast:=45,order:=12288,autOrder:=49152,parity:=1,classes:=20,raw:=245760,method:="pc",representation:="pc_transport",pcOrder:=12288,profileMs:=514),
rec(k:=11892,first:=1,last:=172,unitFirst:=46,unitLast:=217,order:=12288,autOrder:=196608,parity:=1,classes:=172,raw:=2113536,method:="pc",representation:="pc_transport",pcOrder:=12288,profileMs:=599),
rec(k:=11893,first:=1,last:=168,unitFirst:=218,unitLast:=385,order:=12288,autOrder:=196608,parity:=1,classes:=168,raw:=2064384,method:="pc",representation:="pc_transport",pcOrder:=12288,profileMs:=797),
rec(k:=11894,first:=1,last:=270,unitFirst:=386,unitLast:=655,order:=12288,autOrder:=196608,parity:=3,classes:=270,raw:=3317760,method:="pc",representation:="pc_transport",pcOrder:=12288,profileMs:=718),
rec(k:=11895,first:=1,last:=396,unitFirst:=656,unitLast:=1051,order:=12288,autOrder:=25165824,parity:=7,classes:=396,raw:=4866048,method:="pc",representation:="pc_transport",pcOrder:=12288,profileMs:=3779),
rec(k:=11896,first:=1,last:=189,unitFirst:=1052,unitLast:=1240,order:=12288,autOrder:=196608,parity:=3,classes:=189,raw:=2322432,method:="pc",representation:="pc_transport",pcOrder:=12288,profileMs:=808),
rec(k:=11897,first:=1,last:=34,unitFirst:=1241,unitLast:=1274,order:=12288,autOrder:=196608,parity:=7,classes:=34,raw:=417792,method:="pc",representation:="pc_transport",pcOrder:=12288,profileMs:=547),
rec(k:=11898,first:=1,last:=44,unitFirst:=1275,unitLast:=1318,order:=12288,autOrder:=196608,parity:=15,classes:=44,raw:=540672,method:="pc",representation:="pc_transport",pcOrder:=12288,profileMs:=568),
rec(k:=11899,first:=1,last:=16,unitFirst:=1319,unitLast:=1334,order:=12288,autOrder:=2359296,parity:=15,classes:=16,raw:=196608,method:="pc",representation:="pc_transport",pcOrder:=12288,profileMs:=1069),
rec(k:=11900,first:=1,last:=60,unitFirst:=1335,unitLast:=1394,order:=12288,autOrder:=196608,parity:=15,classes:=60,raw:=737280,method:="pc",representation:="pc_transport",pcOrder:=12288,profileMs:=743),
rec(k:=11901,first:=1,last:=640,unitFirst:=1395,unitLast:=2034,order:=12288,autOrder:=196608,parity:=3,classes:=640,raw:=7864320,method:="pc",representation:="pc_transport",pcOrder:=12288,profileMs:=1029),
rec(k:=11902,first:=1,last:=412,unitFirst:=2035,unitLast:=2446,order:=12288,autOrder:=393216,parity:=3,classes:=412,raw:=5062656,method:="pc",representation:="pc_transport",pcOrder:=12288,profileMs:=1118),
rec(k:=11903,first:=1,last:=200,unitFirst:=2447,unitLast:=2646,order:=12288,autOrder:=98304,parity:=15,classes:=200,raw:=2457600,method:="pc",representation:="pc_transport",pcOrder:=12288,profileMs:=722),
rec(k:=11904,first:=1,last:=300,unitFirst:=2647,unitLast:=2946,order:=12288,autOrder:=196608,parity:=15,classes:=300,raw:=3686400,method:="pc",representation:="pc_transport",pcOrder:=12288,profileMs:=837),
rec(k:=11905,first:=1,last:=400,unitFirst:=2947,unitLast:=3346,order:=12288,autOrder:=98304,parity:=15,classes:=400,raw:=4915200,method:="pc",representation:="pc_transport",pcOrder:=12288,profileMs:=1033),
rec(k:=11906,first:=1,last:=183,unitFirst:=3347,unitLast:=3529,order:=12288,autOrder:=196608,parity:=3,classes:=183,raw:=2248704,method:="pc",representation:="pc_transport",pcOrder:=12288,profileMs:=746),
rec(k:=11907,first:=1,last:=133,unitFirst:=3530,unitLast:=3662,order:=12288,autOrder:=196608,parity:=3,classes:=201,raw:=2469888,method:="pc",representation:="pc_transport",pcOrder:=12288,profileMs:=686)
];
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard101_v7_gpt56sol.g");
