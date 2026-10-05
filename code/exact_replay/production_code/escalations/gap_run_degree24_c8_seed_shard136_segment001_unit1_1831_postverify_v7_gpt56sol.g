# Exact wrapper for sealed degree-24 seed workload shard136.
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD136_SEGMENT001_UNIT1_1831_POSTVERIFY_V7_GPT56SOL.txt";
STOP_AFTER_UNIT:=fail;
INTERNAL_GUARD_MS:=1320000; START_UNIT:=1;
INITIAL_COUNTERS:=[0,0,0,0,0,0,0,0,0,0,0,0];
PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";
PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0;
PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";
CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD136_CHECKPOINT_GPT56SOL.txt";
CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD136_CHECKPOINT_TMP_GPT56SOL.txt";
EXPECTED_PROFILE_SHA256:="1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2";
EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard136_v7_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="7A8A050B4575B123B97591D56052E4C737923911296BFE84F59CBB2475528CD4";
S136_RECORDS:=[
rec(k:=12930,first:=71,last:=576,unitFirst:=1,unitLast:=506,order:=24576,autOrder:=1572864,parity:=1,classes:=576,raw:=14155776,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=2019),
rec(k:=12931,first:=1,last:=560,unitFirst:=507,unitLast:=1066,order:=24576,autOrder:=6291456,parity:=3,classes:=560,raw:=13762560,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1975),
rec(k:=12932,first:=1,last:=156,unitFirst:=1067,unitLast:=1222,order:=24576,autOrder:=3145728,parity:=1,classes:=156,raw:=3833856,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1692),
rec(k:=12933,first:=1,last:=446,unitFirst:=1223,unitLast:=1668,order:=24576,autOrder:=3145728,parity:=1,classes:=446,raw:=10960896,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1962),
rec(k:=12934,first:=1,last:=163,unitFirst:=1669,unitLast:=1831,order:=24576,autOrder:=75497472,parity:=3,classes:=256,raw:=6291456,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=3593)
];
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard136_v7_gpt56sol.g");
