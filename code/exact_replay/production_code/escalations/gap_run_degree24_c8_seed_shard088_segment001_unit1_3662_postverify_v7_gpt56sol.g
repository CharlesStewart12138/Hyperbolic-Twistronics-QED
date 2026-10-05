# Exact wrapper for sealed degree-24 seed workload shard088.
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD088_SEGMENT001_UNIT1_3662_POSTVERIFY_V7_GPT56SOL.txt";
STOP_AFTER_UNIT:=fail;
INTERNAL_GUARD_MS:=1320000; START_UNIT:=1;
INITIAL_COUNTERS:=[0,0,0,0,0,0,0,0,0,0,0,0];
PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";
PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0;
PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";
CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD088_CHECKPOINT_GPT56SOL.txt";
CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD088_CHECKPOINT_TMP_GPT56SOL.txt";
EXPECTED_PROFILE_SHA256:="1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2";
EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard088_v7_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="1278C7819779672CAA3A142C1579DBCDCE7325BADAF15D1788A333407584AE17";
S088_RECORDS:=[
rec(k:=11603,first:=108,last:=210,unitFirst:=1,unitLast:=103,order:=12288,autOrder:=393216,parity:=3,classes:=210,raw:=2580480,method:="pc",representation:="pc_transport",pcOrder:=12288,profileMs:=1511),
rec(k:=11604,first:=1,last:=210,unitFirst:=104,unitLast:=313,order:=12288,autOrder:=393216,parity:=3,classes:=210,raw:=2580480,method:="pc",representation:="pc_transport",pcOrder:=12288,profileMs:=1339),
rec(k:=11605,first:=1,last:=1140,unitFirst:=314,unitLast:=1453,order:=12288,autOrder:=1572864,parity:=3,classes:=1140,raw:=14008320,method:="pc",representation:="pc_transport",pcOrder:=12288,profileMs:=1875),
rec(k:=11606,first:=1,last:=1140,unitFirst:=1454,unitLast:=2593,order:=12288,autOrder:=1572864,parity:=3,classes:=1140,raw:=14008320,method:="pc",representation:="pc_transport",pcOrder:=12288,profileMs:=1798),
rec(k:=11607,first:=1,last:=80,unitFirst:=2594,unitLast:=2673,order:=12288,autOrder:=393216,parity:=3,classes:=80,raw:=983040,method:="pc",representation:="pc_transport",pcOrder:=12288,profileMs:=1319),
rec(k:=11608,first:=1,last:=80,unitFirst:=2674,unitLast:=2753,order:=12288,autOrder:=393216,parity:=3,classes:=80,raw:=983040,method:="pc",representation:="pc_transport",pcOrder:=12288,profileMs:=1464),
rec(k:=11609,first:=1,last:=274,unitFirst:=2754,unitLast:=3027,order:=12288,autOrder:=393216,parity:=3,classes:=274,raw:=3366912,method:="pc",representation:="pc_transport",pcOrder:=12288,profileMs:=1209),
rec(k:=11610,first:=1,last:=274,unitFirst:=3028,unitLast:=3301,order:=12288,autOrder:=393216,parity:=3,classes:=274,raw:=3366912,method:="pc",representation:="pc_transport",pcOrder:=12288,profileMs:=1064),
rec(k:=11611,first:=1,last:=361,unitFirst:=3302,unitLast:=3662,order:=12288,autOrder:=786432,parity:=3,classes:=600,raw:=7372800,method:="pc",representation:="pc_transport",pcOrder:=12288,profileMs:=1600)
];
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard088_v7_gpt56sol.g");
