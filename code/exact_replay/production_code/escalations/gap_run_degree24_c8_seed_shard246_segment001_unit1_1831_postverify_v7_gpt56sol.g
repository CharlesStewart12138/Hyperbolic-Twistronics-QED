# Exact wrapper for sealed degree-24 seed workload shard246.
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD246_SEGMENT001_UNIT1_1831_POSTVERIFY_V7_GPT56SOL.txt";
STOP_AFTER_UNIT:=fail;
INTERNAL_GUARD_MS:=1320000; START_UNIT:=1;
INITIAL_COUNTERS:=[0,0,0,0,0,0,0,0,0,0,0,0];
PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";
PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0;
PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";
CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD246_CHECKPOINT_GPT56SOL.txt";
CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD246_CHECKPOINT_TMP_GPT56SOL.txt";
EXPECTED_PROFILE_SHA256:="1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2";
EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard246_v7_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="82CBEA11C3D2BE1C186E8E9493994B184FA9AFD1D49E918410BF857F58F7EBE6";
S246_RECORDS:=[
rec(k:=13711,first:=115,last:=128,unitFirst:=1,unitLast:=14,order:=24576,autOrder:=196608,parity:=15,classes:=128,raw:=3145728,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1300),
rec(k:=13712,first:=1,last:=156,unitFirst:=15,unitLast:=170,order:=24576,autOrder:=786432,parity:=15,classes:=156,raw:=3833856,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1183),
rec(k:=13713,first:=1,last:=128,unitFirst:=171,unitLast:=298,order:=24576,autOrder:=196608,parity:=15,classes:=128,raw:=3145728,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1156),
rec(k:=13714,first:=1,last:=112,unitFirst:=299,unitLast:=410,order:=24576,autOrder:=393216,parity:=15,classes:=112,raw:=2752512,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=870),
rec(k:=13715,first:=1,last:=560,unitFirst:=411,unitLast:=970,order:=24576,autOrder:=393216,parity:=15,classes:=560,raw:=13762560,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1158),
rec(k:=13716,first:=1,last:=328,unitFirst:=971,unitLast:=1298,order:=24576,autOrder:=786432,parity:=15,classes:=328,raw:=8060928,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1675),
rec(k:=13717,first:=1,last:=533,unitFirst:=1299,unitLast:=1831,order:=24576,autOrder:=393216,parity:=15,classes:=560,raw:=13762560,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1907)
];
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard246_v7_gpt56sol.g");
