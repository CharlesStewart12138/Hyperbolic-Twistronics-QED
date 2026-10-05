# Exact wrapper for sealed degree-24 seed workload shard636.
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD636_SEGMENT001_UNIT1_915_POSTVERIFY_V7_GPT56SOL.txt";
STOP_AFTER_UNIT:=fail;
INTERNAL_GUARD_MS:=1320000; START_UNIT:=1;
INITIAL_COUNTERS:=[0,0,0,0,0,0,0,0,0,0,0,0];
PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";
PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0;
PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";
CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD636_CHECKPOINT_GPT56SOL.txt";
CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD636_CHECKPOINT_TMP_GPT56SOL.txt";
EXPECTED_PROFILE_SHA256:="1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2";
EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard636_v7_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="D59AD4024A0D8E4E52AFA800D47C3B0428E9D3AFAA5CC89F6558CD2F624D063F";
S636_RECORDS:=[
rec(k:=15656,first:=181,last:=212,unitFirst:=1,unitLast:=32,order:=49152,autOrder:=1572864,parity:=7,classes:=212,raw:=10420224,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1551),
rec(k:=15657,first:=1,last:=200,unitFirst:=33,unitLast:=232,order:=49152,autOrder:=1572864,parity:=7,classes:=200,raw:=9830400,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1443),
rec(k:=15658,first:=1,last:=72,unitFirst:=233,unitLast:=304,order:=49152,autOrder:=1572864,parity:=7,classes:=72,raw:=3538944,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1626),
rec(k:=15659,first:=1,last:=304,unitFirst:=305,unitLast:=608,order:=49152,autOrder:=1572864,parity:=3,classes:=304,raw:=14942208,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=3171),
rec(k:=15660,first:=1,last:=188,unitFirst:=609,unitLast:=796,order:=49152,autOrder:=1572864,parity:=3,classes:=188,raw:=9240576,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=2257),
rec(k:=15661,first:=1,last:=119,unitFirst:=797,unitLast:=915,order:=49152,autOrder:=1572864,parity:=3,classes:=152,raw:=7471104,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=2317)
];
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard636_v7_gpt56sol.g");
