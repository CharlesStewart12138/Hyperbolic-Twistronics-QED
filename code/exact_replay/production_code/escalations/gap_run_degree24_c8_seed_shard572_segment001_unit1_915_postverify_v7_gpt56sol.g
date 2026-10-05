# Exact wrapper for sealed degree-24 seed workload shard572.
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD572_SEGMENT001_UNIT1_915_POSTVERIFY_V7_GPT56SOL.txt";
STOP_AFTER_UNIT:=fail;
INTERNAL_GUARD_MS:=1320000; START_UNIT:=1;
INITIAL_COUNTERS:=[0,0,0,0,0,0,0,0,0,0,0,0];
PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";
PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0;
PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";
CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD572_CHECKPOINT_GPT56SOL.txt";
CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD572_CHECKPOINT_TMP_GPT56SOL.txt";
EXPECTED_PROFILE_SHA256:="1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2";
EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard572_v7_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="7CBD22F59EA3100804CFE1B1497927E70B7F1FA79E45F9E8A135F179CB325DFD";
S572_RECORDS:=[
rec(k:=15476,first:=206,last:=236,unitFirst:=1,unitLast:=31,order:=49152,autOrder:=3145728,parity:=7,classes:=236,raw:=11599872,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=2177),
rec(k:=15477,first:=1,last:=588,unitFirst:=32,unitLast:=619,order:=49152,autOrder:=12582912,parity:=3,classes:=588,raw:=28901376,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=2003),
rec(k:=15478,first:=1,last:=290,unitFirst:=620,unitLast:=909,order:=49152,autOrder:=6291456,parity:=3,classes:=290,raw:=14254080,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=2514),
rec(k:=15479,first:=1,last:=6,unitFirst:=910,unitLast:=915,order:=49152,autOrder:=1572864,parity:=3,classes:=96,raw:=4718592,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=3006)
];
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard572_v7_gpt56sol.g");
