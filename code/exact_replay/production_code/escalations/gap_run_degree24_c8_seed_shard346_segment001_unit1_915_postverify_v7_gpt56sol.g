# Exact wrapper for sealed degree-24 seed workload shard346.
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD346_SEGMENT001_UNIT1_915_POSTVERIFY_V7_GPT56SOL.txt";
STOP_AFTER_UNIT:=fail;
INTERNAL_GUARD_MS:=1320000; START_UNIT:=1;
INITIAL_COUNTERS:=[0,0,0,0,0,0,0,0,0,0,0,0];
PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";
PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0;
PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";
CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD346_CHECKPOINT_GPT56SOL.txt";
CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD346_CHECKPOINT_TMP_GPT56SOL.txt";
EXPECTED_PROFILE_SHA256:="1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2";
EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard346_v7_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="C7E170D50CCF1E649C85D68CAA7E19611574DB0BD3338A038CA86D9C42B3E5AC";
S346_RECORDS:=[
rec(k:=14839,first:=86,last:=476,unitFirst:=1,unitLast:=391,order:=49152,autOrder:=3145728,parity:=31,classes:=476,raw:=23396352,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=2492),
rec(k:=14840,first:=1,last:=176,unitFirst:=392,unitLast:=567,order:=49152,autOrder:=1572864,parity:=7,classes:=176,raw:=8650752,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1241),
rec(k:=14841,first:=1,last:=208,unitFirst:=568,unitLast:=775,order:=49152,autOrder:=1572864,parity:=31,classes:=208,raw:=10223616,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1768),
rec(k:=14842,first:=1,last:=140,unitFirst:=776,unitLast:=915,order:=49152,autOrder:=1572864,parity:=7,classes:=200,raw:=9830400,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1647)
];
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard346_v7_gpt56sol.g");
