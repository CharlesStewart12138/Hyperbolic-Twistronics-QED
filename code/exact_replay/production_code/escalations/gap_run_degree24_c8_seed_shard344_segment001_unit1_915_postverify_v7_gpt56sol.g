# Exact wrapper for sealed degree-24 seed workload shard344.
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD344_SEGMENT001_UNIT1_915_POSTVERIFY_V7_GPT56SOL.txt";
STOP_AFTER_UNIT:=fail;
INTERNAL_GUARD_MS:=1320000; START_UNIT:=1;
INITIAL_COUNTERS:=[0,0,0,0,0,0,0,0,0,0,0,0];
PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";
PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0;
PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";
CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD344_CHECKPOINT_GPT56SOL.txt";
CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD344_CHECKPOINT_TMP_GPT56SOL.txt";
EXPECTED_PROFILE_SHA256:="1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2";
EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard344_v7_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="C1E2B2B4DEAAF7833EDA4ED0473119AB5334A736B21383E3E5F800B5381D7084";
S344_RECORDS:=[
rec(k:=14827,first:=86,last:=256,unitFirst:=1,unitLast:=171,order:=49152,autOrder:=3145728,parity:=3,classes:=256,raw:=12582912,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1448),
rec(k:=14828,first:=1,last:=128,unitFirst:=172,unitLast:=299,order:=49152,autOrder:=1572864,parity:=1,classes:=128,raw:=6291456,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1111),
rec(k:=14829,first:=1,last:=186,unitFirst:=300,unitLast:=485,order:=49152,autOrder:=37748736,parity:=7,classes:=186,raw:=9142272,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=5123),
rec(k:=14830,first:=1,last:=192,unitFirst:=486,unitLast:=677,order:=49152,autOrder:=12582912,parity:=3,classes:=192,raw:=9437184,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=2416),
rec(k:=14831,first:=1,last:=48,unitFirst:=678,unitLast:=725,order:=49152,autOrder:=1572864,parity:=1,classes:=48,raw:=2359296,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1166),
rec(k:=14832,first:=1,last:=76,unitFirst:=726,unitLast:=801,order:=49152,autOrder:=1572864,parity:=1,classes:=76,raw:=3735552,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1291),
rec(k:=14833,first:=1,last:=114,unitFirst:=802,unitLast:=915,order:=49152,autOrder:=1572864,parity:=7,classes:=176,raw:=8650752,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=2081)
];
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard344_v7_gpt56sol.g");
