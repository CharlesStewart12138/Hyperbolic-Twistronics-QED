# Exact wrapper for sealed degree-24 seed workload shard590.
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD590_SEGMENT001_UNIT1_915_POSTVERIFY_V7_GPT56SOL.txt";
STOP_AFTER_UNIT:=fail;
INTERNAL_GUARD_MS:=1320000; START_UNIT:=1;
INITIAL_COUNTERS:=[0,0,0,0,0,0,0,0,0,0,0,0];
PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";
PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0;
PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";
CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD590_CHECKPOINT_GPT56SOL.txt";
CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD590_CHECKPOINT_TMP_GPT56SOL.txt";
EXPECTED_PROFILE_SHA256:="1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2";
EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard590_v7_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="0CDBA529D9F9B7A14743381656DC943A66272273C82F150EF619C41A9DDFBA54";
S590_RECORDS:=[
rec(k:=15543,first:=78,last:=132,unitFirst:=1,unitLast:=55,order:=49152,autOrder:=1572864,parity:=7,classes:=132,raw:=6488064,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=2311),
rec(k:=15544,first:=1,last:=176,unitFirst:=56,unitLast:=231,order:=49152,autOrder:=1572864,parity:=7,classes:=176,raw:=8650752,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1211),
rec(k:=15545,first:=1,last:=192,unitFirst:=232,unitLast:=423,order:=49152,autOrder:=1572864,parity:=15,classes:=192,raw:=9437184,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1955),
rec(k:=15546,first:=1,last:=400,unitFirst:=424,unitLast:=823,order:=49152,autOrder:=3145728,parity:=15,classes:=400,raw:=19660800,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=976),
rec(k:=15547,first:=1,last:=92,unitFirst:=824,unitLast:=915,order:=49152,autOrder:=1572864,parity:=15,classes:=208,raw:=10223616,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1396)
];
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard590_v7_gpt56sol.g");
