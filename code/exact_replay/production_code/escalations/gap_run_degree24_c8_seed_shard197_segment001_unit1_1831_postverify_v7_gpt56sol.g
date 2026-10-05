# Exact wrapper for sealed degree-24 seed workload shard197.
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD197_SEGMENT001_UNIT1_1831_POSTVERIFY_V7_GPT56SOL.txt";
STOP_AFTER_UNIT:=fail;
INTERNAL_GUARD_MS:=1320000; START_UNIT:=1;
INITIAL_COUNTERS:=[0,0,0,0,0,0,0,0,0,0,0,0];
PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";
PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0;
PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";
CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD197_CHECKPOINT_GPT56SOL.txt";
CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD197_CHECKPOINT_TMP_GPT56SOL.txt";
EXPECTED_PROFILE_SHA256:="1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2";
EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard197_v7_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="CBF308E609676755D3068B95AE95774EA68A3575C690421DCF4252938FD63D62";
S197_RECORDS:=[
rec(k:=13430,first:=429,last:=512,unitFirst:=1,unitLast:=84,order:=24576,autOrder:=393216,parity:=15,classes:=512,raw:=12582912,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1939),
rec(k:=13431,first:=1,last:=960,unitFirst:=85,unitLast:=1044,order:=24576,autOrder:=1572864,parity:=15,classes:=960,raw:=23592960,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=3582),
rec(k:=13432,first:=1,last:=144,unitFirst:=1045,unitLast:=1188,order:=24576,autOrder:=393216,parity:=15,classes:=144,raw:=3538944,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=2447),
rec(k:=13433,first:=1,last:=128,unitFirst:=1189,unitLast:=1316,order:=24576,autOrder:=393216,parity:=7,classes:=128,raw:=3145728,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=975),
rec(k:=13434,first:=1,last:=120,unitFirst:=1317,unitLast:=1436,order:=24576,autOrder:=786432,parity:=7,classes:=120,raw:=2949120,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1199),
rec(k:=13435,first:=1,last:=395,unitFirst:=1437,unitLast:=1831,order:=24576,autOrder:=393216,parity:=7,classes:=512,raw:=12582912,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1861)
];
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard197_v7_gpt56sol.g");
