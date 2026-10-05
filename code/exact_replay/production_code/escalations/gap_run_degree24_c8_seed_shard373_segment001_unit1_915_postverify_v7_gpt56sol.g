# Exact wrapper for sealed degree-24 seed workload shard373.
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD373_SEGMENT001_UNIT1_915_POSTVERIFY_V7_GPT56SOL.txt";
STOP_AFTER_UNIT:=fail;
INTERNAL_GUARD_MS:=1320000; START_UNIT:=1;
INITIAL_COUNTERS:=[0,0,0,0,0,0,0,0,0,0,0,0];
PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";
PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0;
PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";
CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD373_CHECKPOINT_GPT56SOL.txt";
CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD373_CHECKPOINT_TMP_GPT56SOL.txt";
EXPECTED_PROFILE_SHA256:="1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2";
EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard373_v7_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="B3B500BE81DF48B11837AD3633BCCFE18CA0F80137A558AC419C8CA9997E0895";
S373_RECORDS:=[
rec(k:=14943,first:=289,last:=348,unitFirst:=1,unitLast:=60,order:=49152,autOrder:=3145728,parity:=3,classes:=348,raw:=17104896,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1967),
rec(k:=14944,first:=1,last:=192,unitFirst:=61,unitLast:=252,order:=49152,autOrder:=1572864,parity:=1,classes:=192,raw:=9437184,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1270),
rec(k:=14945,first:=1,last:=108,unitFirst:=253,unitLast:=360,order:=49152,autOrder:=786432,parity:=1,classes:=108,raw:=5308416,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1682),
rec(k:=14946,first:=1,last:=80,unitFirst:=361,unitLast:=440,order:=49152,autOrder:=786432,parity:=1,classes:=80,raw:=3932160,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1501),
rec(k:=14947,first:=1,last:=128,unitFirst:=441,unitLast:=568,order:=49152,autOrder:=786432,parity:=1,classes:=128,raw:=6291456,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=988),
rec(k:=14948,first:=1,last:=347,unitFirst:=569,unitLast:=915,order:=49152,autOrder:=3145728,parity:=3,classes:=448,raw:=22020096,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=2103)
];
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard373_v7_gpt56sol.g");
