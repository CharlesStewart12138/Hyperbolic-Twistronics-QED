# Exact wrapper for sealed degree-24 seed workload shard106.
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD106_SEGMENT001_UNIT1_3662_POSTVERIFY_V7_GPT56SOL.txt";
STOP_AFTER_UNIT:=fail;
INTERNAL_GUARD_MS:=1320000; START_UNIT:=1;
INITIAL_COUNTERS:=[0,0,0,0,0,0,0,0,0,0,0,0];
PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";
PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0;
PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";
CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD106_CHECKPOINT_GPT56SOL.txt";
CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD106_CHECKPOINT_TMP_GPT56SOL.txt";
EXPECTED_PROFILE_SHA256:="1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2";
EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard106_v7_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="782AE74ADEC6D6761A28BB37EA8A1FFA2FE22C1F7509D4714B6D29D6AF844461";
S106_RECORDS:=[
rec(k:=11960,first:=400,last:=624,unitFirst:=1,unitLast:=225,order:=12288,autOrder:=1572864,parity:=3,classes:=624,raw:=7667712,method:="pc",representation:="pc_transport",pcOrder:=12288,profileMs:=2285),
rec(k:=11961,first:=1,last:=512,unitFirst:=226,unitLast:=737,order:=12288,autOrder:=393216,parity:=3,classes:=512,raw:=6291456,method:="pc",representation:="pc_transport",pcOrder:=12288,profileMs:=2283),
rec(k:=11962,first:=1,last:=434,unitFirst:=738,unitLast:=1171,order:=12288,autOrder:=393216,parity:=3,classes:=434,raw:=5332992,method:="pc",representation:="pc_transport",pcOrder:=12288,profileMs:=1258),
rec(k:=11963,first:=1,last:=275,unitFirst:=1172,unitLast:=1446,order:=12288,autOrder:=786432,parity:=3,classes:=275,raw:=3379200,method:="pc",representation:="pc_transport",pcOrder:=12288,profileMs:=1060),
rec(k:=11964,first:=1,last:=640,unitFirst:=1447,unitLast:=2086,order:=12288,autOrder:=196608,parity:=3,classes:=640,raw:=7864320,method:="pc",representation:="pc_transport",pcOrder:=12288,profileMs:=1487),
rec(k:=11965,first:=1,last:=640,unitFirst:=2087,unitLast:=2726,order:=12288,autOrder:=196608,parity:=3,classes:=640,raw:=7864320,method:="pc",representation:="pc_transport",pcOrder:=12288,profileMs:=1369),
rec(k:=11966,first:=1,last:=434,unitFirst:=2727,unitLast:=3160,order:=12288,autOrder:=393216,parity:=3,classes:=434,raw:=5332992,method:="pc",representation:="pc_transport",pcOrder:=12288,profileMs:=1195),
rec(k:=11967,first:=1,last:=434,unitFirst:=3161,unitLast:=3594,order:=12288,autOrder:=393216,parity:=3,classes:=434,raw:=5332992,method:="pc",representation:="pc_transport",pcOrder:=12288,profileMs:=1138),
rec(k:=11968,first:=1,last:=68,unitFirst:=3595,unitLast:=3662,order:=12288,autOrder:=12582912,parity:=3,classes:=396,raw:=4866048,method:="pc",representation:="pc_transport",pcOrder:=12288,profileMs:=5790)
];
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard106_v7_gpt56sol.g");
