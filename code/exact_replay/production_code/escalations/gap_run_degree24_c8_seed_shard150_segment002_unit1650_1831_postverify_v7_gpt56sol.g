# Exact wrapper for sealed degree-24 seed workload shard150.
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD150_SEGMENT002_UNIT1650_1831_POSTVERIFY_V7_GPT56SOL.txt";
STOP_AFTER_UNIT:=fail;
INTERNAL_GUARD_MS:=1320000; START_UNIT:=1650;
INITIAL_COUNTERS:=[1649,40525824,1649,87,1507776,633856,205376,40256,0,0,0,0];
PREVIOUS_CHECKPOINT_SHA256:="cf87b77ccac675c1e827807d3a62d3a88cec784e582600c3134f8a46ddb2293e";
PREVIOUS_OUTPUT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD150_SEGMENT001_UNIT1_1831_POSTVERIFY_V7_GPT56SOL.txt"; PREVIOUS_OUTPUT_PREFIX_BYTES:=1243780;
PREVIOUS_OUTPUT_PREFIX_SHA256:="0a736924f8468fb8a22a1e0866224476e863bf544dab71032d4041151ed4d298";
CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD150_CHECKPOINT_GPT56SOL.txt";
CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD150_CHECKPOINT_TMP_GPT56SOL.txt";
EXPECTED_PROFILE_SHA256:="1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2";
EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard150_v7_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="57A3090518E9C930BDD31AC037EA5FE6C5152269C886177B2BA072003B349060";
S150_RECORDS:=[
rec(k:=13034,first:=479,last:=560,unitFirst:=1,unitLast:=82,order:=24576,autOrder:=6291456,parity:=3,classes:=560,raw:=13762560,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1877),
rec(k:=13035,first:=1,last:=92,unitFirst:=83,unitLast:=174,order:=24576,autOrder:=393216,parity:=3,classes:=92,raw:=2260992,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1685),
rec(k:=13036,first:=1,last:=178,unitFirst:=175,unitLast:=352,order:=24576,autOrder:=1572864,parity:=1,classes:=178,raw:=4374528,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1106),
rec(k:=13037,first:=1,last:=100,unitFirst:=353,unitLast:=452,order:=24576,autOrder:=393216,parity:=3,classes:=100,raw:=2457600,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=843),
rec(k:=13038,first:=1,last:=239,unitFirst:=453,unitLast:=691,order:=24576,autOrder:=3145728,parity:=3,classes:=239,raw:=5873664,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1554),
rec(k:=13039,first:=1,last:=144,unitFirst:=692,unitLast:=835,order:=24576,autOrder:=786432,parity:=1,classes:=144,raw:=3538944,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1658),
rec(k:=13040,first:=1,last:=137,unitFirst:=836,unitLast:=972,order:=24576,autOrder:=1572864,parity:=1,classes:=137,raw:=3366912,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=760),
rec(k:=13041,first:=1,last:=40,unitFirst:=973,unitLast:=1012,order:=24576,autOrder:=98304,parity:=3,classes:=40,raw:=983040,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=938),
rec(k:=13042,first:=1,last:=506,unitFirst:=1013,unitLast:=1518,order:=24576,autOrder:=12582912,parity:=1,classes:=506,raw:=12435456,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=2173),
rec(k:=13043,first:=1,last:=32,unitFirst:=1519,unitLast:=1550,order:=24576,autOrder:=393216,parity:=3,classes:=32,raw:=786432,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1130),
rec(k:=13044,first:=1,last:=120,unitFirst:=1551,unitLast:=1670,order:=24576,autOrder:=786432,parity:=7,classes:=120,raw:=2949120,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1497),
rec(k:=13045,first:=1,last:=128,unitFirst:=1671,unitLast:=1798,order:=24576,autOrder:=393216,parity:=3,classes:=128,raw:=3145728,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=833),
rec(k:=13046,first:=1,last:=33,unitFirst:=1799,unitLast:=1831,order:=24576,autOrder:=1572864,parity:=7,classes:=262,raw:=6438912,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1165)
];
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard150_v7_gpt56sol.g");
