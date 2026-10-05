# Exact wrapper for sealed degree-24 seed workload shard221.
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD221_SEGMENT001_UNIT1_1831_POSTVERIFY_V7_GPT56SOL.txt";
STOP_AFTER_UNIT:=fail;
INTERNAL_GUARD_MS:=1320000; START_UNIT:=1;
INITIAL_COUNTERS:=[0,0,0,0,0,0,0,0,0,0,0,0];
PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";
PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0;
PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";
CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD221_CHECKPOINT_GPT56SOL.txt";
CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD221_CHECKPOINT_TMP_GPT56SOL.txt";
EXPECTED_PROFILE_SHA256:="1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2";
EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard221_v7_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="57361839B242812AEFBD3D5667701D52564297F020726E2FFE209C43918DE066";
S221_RECORDS:=[
rec(k:=13569,first:=86,last:=432,unitFirst:=1,unitLast:=347,order:=24576,autOrder:=393216,parity:=3,classes:=432,raw:=10616832,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1414),
rec(k:=13570,first:=1,last:=680,unitFirst:=348,unitLast:=1027,order:=24576,autOrder:=786432,parity:=7,classes:=680,raw:=16711680,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1992),
rec(k:=13571,first:=1,last:=116,unitFirst:=1028,unitLast:=1143,order:=24576,autOrder:=786432,parity:=3,classes:=116,raw:=2850816,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1535),
rec(k:=13572,first:=1,last:=480,unitFirst:=1144,unitLast:=1623,order:=24576,autOrder:=393216,parity:=7,classes:=480,raw:=11796480,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1760),
rec(k:=13573,first:=1,last:=208,unitFirst:=1624,unitLast:=1831,order:=24576,autOrder:=786432,parity:=3,classes:=600,raw:=14745600,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1732)
];
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard221_v7_gpt56sol.g");
