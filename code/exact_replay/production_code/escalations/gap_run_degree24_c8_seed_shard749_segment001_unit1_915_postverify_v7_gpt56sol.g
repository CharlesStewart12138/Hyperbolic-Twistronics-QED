# Exact wrapper for sealed degree-24 seed workload shard749.
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD749_SEGMENT001_UNIT1_915_POSTVERIFY_V7_GPT56SOL.txt";
STOP_AFTER_UNIT:=fail;
INTERNAL_GUARD_MS:=1320000; START_UNIT:=1;
INITIAL_COUNTERS:=[0,0,0,0,0,0,0,0,0,0,0,0];
PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";
PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0;
PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";
CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD749_CHECKPOINT_GPT56SOL.txt";
CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD749_CHECKPOINT_TMP_GPT56SOL.txt";
EXPECTED_PROFILE_SHA256:="1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2";
EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard749_v7_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="43AC5A1A56A88020C51D80C34C8EACDFBB38E78805F1C083FDBC65E2A0B56776";
S749_RECORDS:=[
rec(k:=15797,first:=341,last:=644,unitFirst:=1,unitLast:=304,order:=49152,autOrder:=786432,parity:=7,classes:=644,raw:=31653888,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1868),
rec(k:=15798,first:=1,last:=128,unitFirst:=305,unitLast:=432,order:=49152,autOrder:=393216,parity:=7,classes:=128,raw:=6291456,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1103),
rec(k:=15799,first:=1,last:=316,unitFirst:=433,unitLast:=748,order:=49152,autOrder:=1572864,parity:=15,classes:=316,raw:=15532032,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1264),
rec(k:=15800,first:=1,last:=167,unitFirst:=749,unitLast:=915,order:=49152,autOrder:=786432,parity:=15,classes:=200,raw:=9830400,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1916)
];
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard749_v7_gpt56sol.g");
