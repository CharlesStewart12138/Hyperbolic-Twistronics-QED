# Exact wrapper for sealed degree-24 seed workload shard139.
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD139_SEGMENT001_UNIT1_1831_POSTVERIFY_V7_GPT56SOL.txt";
STOP_AFTER_UNIT:=fail;
INTERNAL_GUARD_MS:=1320000; START_UNIT:=1;
INITIAL_COUNTERS:=[0,0,0,0,0,0,0,0,0,0,0,0];
PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";
PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0;
PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";
CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD139_CHECKPOINT_GPT56SOL.txt";
CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD139_CHECKPOINT_TMP_GPT56SOL.txt";
EXPECTED_PROFILE_SHA256:="1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2";
EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard139_v7_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="CBD80E499A25324E04BB15B9D280263A33DAF8EAD2E05596F1A917FD0B0DDA13";
S139_RECORDS:=[
rec(k:=12948,first:=51,last:=180,unitFirst:=1,unitLast:=130,order:=24576,autOrder:=1572864,parity:=1,classes:=180,raw:=4423680,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1376),
rec(k:=12949,first:=1,last:=137,unitFirst:=131,unitLast:=267,order:=24576,autOrder:=1572864,parity:=1,classes:=137,raw:=3366912,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=839),
rec(k:=12950,first:=1,last:=228,unitFirst:=268,unitLast:=495,order:=24576,autOrder:=1572864,parity:=1,classes:=228,raw:=5603328,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1562),
rec(k:=12951,first:=1,last:=714,unitFirst:=496,unitLast:=1209,order:=24576,autOrder:=1572864,parity:=7,classes:=714,raw:=17547264,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=2098),
rec(k:=12952,first:=1,last:=112,unitFirst:=1210,unitLast:=1321,order:=24576,autOrder:=393216,parity:=15,classes:=112,raw:=2752512,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=931),
rec(k:=12953,first:=1,last:=137,unitFirst:=1322,unitLast:=1458,order:=24576,autOrder:=1572864,parity:=1,classes:=137,raw:=3366912,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=848),
rec(k:=12954,first:=1,last:=128,unitFirst:=1459,unitLast:=1586,order:=24576,autOrder:=393216,parity:=3,classes:=128,raw:=3145728,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=904),
rec(k:=12955,first:=1,last:=178,unitFirst:=1587,unitLast:=1764,order:=24576,autOrder:=1572864,parity:=1,classes:=178,raw:=4374528,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1138),
rec(k:=12956,first:=1,last:=67,unitFirst:=1765,unitLast:=1831,order:=24576,autOrder:=393216,parity:=3,classes:=128,raw:=3145728,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1169)
];
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard139_v7_gpt56sol.g");
