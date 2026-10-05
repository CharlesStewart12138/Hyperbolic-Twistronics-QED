# Exact wrapper for sealed degree-24 seed workload shard146.
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD146_SEGMENT001_UNIT1_1831_POSTVERIFY_V7_GPT56SOL.txt";
STOP_AFTER_UNIT:=fail;
INTERNAL_GUARD_MS:=1320000; START_UNIT:=1;
INITIAL_COUNTERS:=[0,0,0,0,0,0,0,0,0,0,0,0];
PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";
PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0;
PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";
CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD146_CHECKPOINT_GPT56SOL.txt";
CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD146_CHECKPOINT_TMP_GPT56SOL.txt";
EXPECTED_PROFILE_SHA256:="1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2";
EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard146_v7_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="546D4C6AFB25E3193F11DD544DBFE4C71E663CEDB2123AC926CDB48068A5AA60";
S146_RECORDS:=[
rec(k:=13002,first:=242,last:=366,unitFirst:=1,unitLast:=125,order:=24576,autOrder:=3145728,parity:=1,classes:=366,raw:=8994816,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1192),
rec(k:=13003,first:=1,last:=466,unitFirst:=126,unitLast:=591,order:=24576,autOrder:=3145728,parity:=7,classes:=466,raw:=11452416,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1439),
rec(k:=13004,first:=1,last:=178,unitFirst:=592,unitLast:=769,order:=24576,autOrder:=1572864,parity:=1,classes:=178,raw:=4374528,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1269),
rec(k:=13005,first:=1,last:=156,unitFirst:=770,unitLast:=925,order:=24576,autOrder:=3145728,parity:=1,classes:=156,raw:=3833856,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1639),
rec(k:=13006,first:=1,last:=136,unitFirst:=926,unitLast:=1061,order:=24576,autOrder:=1572864,parity:=1,classes:=136,raw:=3342336,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1658),
rec(k:=13007,first:=1,last:=156,unitFirst:=1062,unitLast:=1217,order:=24576,autOrder:=786432,parity:=3,classes:=156,raw:=3833856,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1980),
rec(k:=13008,first:=1,last:=334,unitFirst:=1218,unitLast:=1551,order:=24576,autOrder:=786432,parity:=1,classes:=334,raw:=8208384,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1161),
rec(k:=13010,first:=1,last:=280,unitFirst:=1552,unitLast:=1831,order:=24576,autOrder:=1572864,parity:=3,classes:=392,raw:=9633792,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1513)
];
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard146_v7_gpt56sol.g");
