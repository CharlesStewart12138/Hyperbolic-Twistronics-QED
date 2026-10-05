# Exact wrapper for sealed degree-24 seed workload shard757.
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD757_SEGMENT001_UNIT1_915_POSTVERIFY_V7_GPT56SOL.txt";
STOP_AFTER_UNIT:=fail;
INTERNAL_GUARD_MS:=1320000; START_UNIT:=1;
INITIAL_COUNTERS:=[0,0,0,0,0,0,0,0,0,0,0,0];
PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";
PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0;
PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";
CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD757_CHECKPOINT_GPT56SOL.txt";
CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD757_CHECKPOINT_TMP_GPT56SOL.txt";
EXPECTED_PROFILE_SHA256:="1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2";
EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard757_v7_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="27E555B4AA07F4B682D7F8298616A854BA9C4F583ADDF6EE127C8C2452D9E4EB";
S757_RECORDS:=[
rec(k:=15815,first:=89,last:=256,unitFirst:=1,unitLast:=168,order:=49152,autOrder:=393216,parity:=7,classes:=256,raw:=12582912,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1431),
rec(k:=15816,first:=1,last:=176,unitFirst:=169,unitLast:=344,order:=49152,autOrder:=786432,parity:=7,classes:=176,raw:=8650752,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1115),
rec(k:=15817,first:=1,last:=120,unitFirst:=345,unitLast:=464,order:=49152,autOrder:=786432,parity:=7,classes:=120,raw:=5898240,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1962),
rec(k:=15818,first:=1,last:=320,unitFirst:=465,unitLast:=784,order:=49152,autOrder:=393216,parity:=7,classes:=320,raw:=15728640,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=915),
rec(k:=15819,first:=1,last:=131,unitFirst:=785,unitLast:=915,order:=49152,autOrder:=393216,parity:=7,classes:=320,raw:=15728640,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1293)
];
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard757_v7_gpt56sol.g");
