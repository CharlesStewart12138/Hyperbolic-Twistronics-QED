# Exact wrapper for sealed degree-24 seed workload shard294.
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD294_SEGMENT001_UNIT1_1831_POSTVERIFY_V7_GPT56SOL.txt";
STOP_AFTER_UNIT:=fail;
INTERNAL_GUARD_MS:=1320000; START_UNIT:=1;
INITIAL_COUNTERS:=[0,0,0,0,0,0,0,0,0,0,0,0];
PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";
PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0;
PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";
CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD294_CHECKPOINT_GPT56SOL.txt";
CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD294_CHECKPOINT_TMP_GPT56SOL.txt";
EXPECTED_PROFILE_SHA256:="1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2";
EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard294_v7_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="CA9F60B447A796D0E78A4A6C1FE33AA30B5D1C82AF96C0E1E0DBAD068A485441";
S294_RECORDS:=[
rec(k:=13921,first:=390,last:=392,unitFirst:=1,unitLast:=3,order:=24576,autOrder:=196608,parity:=7,classes:=392,raw:=9633792,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1086),
rec(k:=13922,first:=1,last:=440,unitFirst:=4,unitLast:=443,order:=24576,autOrder:=196608,parity:=7,classes:=440,raw:=10813440,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1284),
rec(k:=13923,first:=1,last:=268,unitFirst:=444,unitLast:=711,order:=24576,autOrder:=196608,parity:=3,classes:=268,raw:=6586368,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1062),
rec(k:=13924,first:=1,last:=440,unitFirst:=712,unitLast:=1151,order:=24576,autOrder:=196608,parity:=7,classes:=440,raw:=10813440,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1004),
rec(k:=13925,first:=1,last:=282,unitFirst:=1152,unitLast:=1433,order:=24576,autOrder:=393216,parity:=7,classes:=282,raw:=6930432,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1152),
rec(k:=13926,first:=1,last:=392,unitFirst:=1434,unitLast:=1825,order:=24576,autOrder:=196608,parity:=7,classes:=392,raw:=9633792,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1557),
rec(k:=13927,first:=1,last:=6,unitFirst:=1826,unitLast:=1831,order:=24576,autOrder:=196608,parity:=7,classes:=440,raw:=10813440,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1100)
];
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard294_v7_gpt56sol.g");
