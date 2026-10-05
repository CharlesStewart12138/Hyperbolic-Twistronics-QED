# Exact wrapper for sealed degree-24 seed workload shard212.
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD212_SEGMENT001_UNIT1_1831_POSTVERIFY_V7_GPT56SOL.txt";
STOP_AFTER_UNIT:=fail;
INTERNAL_GUARD_MS:=1320000; START_UNIT:=1;
INITIAL_COUNTERS:=[0,0,0,0,0,0,0,0,0,0,0,0];
PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";
PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0;
PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";
CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD212_CHECKPOINT_GPT56SOL.txt";
CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD212_CHECKPOINT_TMP_GPT56SOL.txt";
EXPECTED_PROFILE_SHA256:="1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2";
EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard212_v7_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="D12AAEC52F701F61245C0140B00928B1F40A31B0E9D0D57867A3E42F230E37C3";
S212_RECORDS:=[
rec(k:=13517,first:=331,last:=480,unitFirst:=1,unitLast:=150,order:=24576,autOrder:=393216,parity:=3,classes:=480,raw:=11796480,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1369),
rec(k:=13518,first:=1,last:=680,unitFirst:=151,unitLast:=830,order:=24576,autOrder:=786432,parity:=7,classes:=680,raw:=16711680,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1382),
rec(k:=13519,first:=1,last:=72,unitFirst:=831,unitLast:=902,order:=24576,autOrder:=393216,parity:=3,classes:=72,raw:=1769472,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1277),
rec(k:=13520,first:=1,last:=180,unitFirst:=903,unitLast:=1082,order:=24576,autOrder:=1572864,parity:=7,classes:=180,raw:=4423680,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1255),
rec(k:=13521,first:=1,last:=480,unitFirst:=1083,unitLast:=1562,order:=24576,autOrder:=393216,parity:=3,classes:=480,raw:=11796480,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1699),
rec(k:=13522,first:=1,last:=40,unitFirst:=1563,unitLast:=1602,order:=24576,autOrder:=98304,parity:=3,classes:=40,raw:=983040,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=851),
rec(k:=13523,first:=1,last:=229,unitFirst:=1603,unitLast:=1831,order:=24576,autOrder:=786432,parity:=7,classes:=470,raw:=11550720,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1453)
];
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard212_v7_gpt56sol.g");
