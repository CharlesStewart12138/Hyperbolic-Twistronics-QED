# Exact wrapper for sealed degree-24 seed workload shard216.
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD216_SEGMENT001_UNIT1_1831_POSTVERIFY_V7_GPT56SOL.txt";
STOP_AFTER_UNIT:=fail;
INTERNAL_GUARD_MS:=1320000; START_UNIT:=1;
INITIAL_COUNTERS:=[0,0,0,0,0,0,0,0,0,0,0,0];
PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";
PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0;
PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";
CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD216_CHECKPOINT_GPT56SOL.txt";
CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD216_CHECKPOINT_TMP_GPT56SOL.txt";
EXPECTED_PROFILE_SHA256:="1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2";
EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard216_v7_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="EDED04D13BFC0334DF811852E58E3A5129B982A9490C42BAF48913E55DBE6D9C";
S216_RECORDS:=[
rec(k:=13542,first:=93,last:=96,unitFirst:=1,unitLast:=4,order:=24576,autOrder:=196608,parity:=3,classes:=96,raw:=2359296,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1118),
rec(k:=13543,first:=1,last:=720,unitFirst:=5,unitLast:=724,order:=24576,autOrder:=786432,parity:=3,classes:=720,raw:=17694720,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1786),
rec(k:=13544,first:=1,last:=520,unitFirst:=725,unitLast:=1244,order:=24576,autOrder:=786432,parity:=7,classes:=520,raw:=12779520,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1744),
rec(k:=13545,first:=1,last:=416,unitFirst:=1245,unitLast:=1660,order:=24576,autOrder:=393216,parity:=3,classes:=416,raw:=10223616,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1012),
rec(k:=13546,first:=1,last:=72,unitFirst:=1661,unitLast:=1732,order:=24576,autOrder:=393216,parity:=3,classes:=72,raw:=1769472,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1168),
rec(k:=13547,first:=1,last:=99,unitFirst:=1733,unitLast:=1831,order:=24576,autOrder:=1572864,parity:=7,classes:=226,raw:=5554176,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1539)
];
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard216_v7_gpt56sol.g");
