# Exact wrapper for sealed degree-24 seed workload shard632.
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD632_SEGMENT001_UNIT1_915_POSTVERIFY_V7_GPT56SOL.txt";
STOP_AFTER_UNIT:=fail;
INTERNAL_GUARD_MS:=1320000; START_UNIT:=1;
INITIAL_COUNTERS:=[0,0,0,0,0,0,0,0,0,0,0,0];
PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";
PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0;
PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";
CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD632_CHECKPOINT_GPT56SOL.txt";
CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD632_CHECKPOINT_TMP_GPT56SOL.txt";
EXPECTED_PROFILE_SHA256:="1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2";
EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard632_v7_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="987422DA2232C4F306FB1708A3D5DD0BDC7882BD688FBA22D8218DE538641E27";
S632_RECORDS:=[
rec(k:=15639,first:=121,last:=368,unitFirst:=1,unitLast:=248,order:=49152,autOrder:=1572864,parity:=3,classes:=368,raw:=18087936,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=2962),
rec(k:=15640,first:=1,last:=216,unitFirst:=249,unitLast:=464,order:=49152,autOrder:=1572864,parity:=3,classes:=216,raw:=10616832,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1026),
rec(k:=15641,first:=1,last:=152,unitFirst:=465,unitLast:=616,order:=49152,autOrder:=1572864,parity:=3,classes:=152,raw:=7471104,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1848),
rec(k:=15642,first:=1,last:=184,unitFirst:=617,unitLast:=800,order:=49152,autOrder:=1572864,parity:=3,classes:=184,raw:=9043968,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=2041),
rec(k:=15643,first:=1,last:=115,unitFirst:=801,unitLast:=915,order:=49152,autOrder:=1572864,parity:=7,classes:=304,raw:=14942208,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=3365)
];
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard632_v7_gpt56sol.g");
