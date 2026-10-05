# Exact wrapper for sealed degree-24 seed workload shard275.
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD275_SEGMENT001_UNIT1_1831_POSTVERIFY_V7_GPT56SOL.txt";
STOP_AFTER_UNIT:=fail;
INTERNAL_GUARD_MS:=1320000; START_UNIT:=1;
INITIAL_COUNTERS:=[0,0,0,0,0,0,0,0,0,0,0,0];
PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";
PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0;
PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";
CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD275_CHECKPOINT_GPT56SOL.txt";
CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD275_CHECKPOINT_TMP_GPT56SOL.txt";
EXPECTED_PROFILE_SHA256:="1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2";
EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard275_v7_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="55BCFBEDE7A387C1D37BC81D1FB90CBCDE5D19BEE76CDF2D092FCDD6DBB3C6A7";
S275_RECORDS:=[
rec(k:=13815,first:=52,last:=476,unitFirst:=1,unitLast:=425,order:=24576,autOrder:=786432,parity:=1,classes:=476,raw:=11698176,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1013),
rec(k:=13816,first:=1,last:=160,unitFirst:=426,unitLast:=585,order:=24576,autOrder:=786432,parity:=1,classes:=160,raw:=3932160,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1058),
rec(k:=13817,first:=1,last:=640,unitFirst:=586,unitLast:=1225,order:=24576,autOrder:=393216,parity:=7,classes:=640,raw:=15728640,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1077),
rec(k:=13818,first:=1,last:=606,unitFirst:=1226,unitLast:=1831,order:=24576,autOrder:=393216,parity:=7,classes:=640,raw:=15728640,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1455)
];
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard275_v7_gpt56sol.g");
