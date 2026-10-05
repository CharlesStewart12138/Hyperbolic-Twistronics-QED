# Exact wrapper for sealed degree-24 seed workload shard813.
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD813_SEGMENT002_UNIT289_915_POSTVERIFY_V7_GPT56SOL.txt";
STOP_AFTER_UNIT:=fail;
INTERNAL_GUARD_MS:=1320000; START_UNIT:=289;
INITIAL_COUNTERS:=[288,14155776,288,8,314496,167616,39296,14592,0,0,0,0];
PREVIOUS_CHECKPOINT_SHA256:="d8fac1e3d9ae7cce5b06bfdcd3e967db7af54f32e9ef7cdd63fe1aad295213b5";
PREVIOUS_OUTPUT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD813_SEGMENT001_UNIT1_915_POSTVERIFY_V7_GPT56SOL.txt"; PREVIOUS_OUTPUT_PREFIX_BYTES:=215865;
PREVIOUS_OUTPUT_PREFIX_SHA256:="059caefba7834fe21af310457e3253dc0630c27a90dadbed33bb143c0c4c4b88";
CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD813_CHECKPOINT_GPT56SOL.txt";
CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD813_CHECKPOINT_TMP_GPT56SOL.txt";
EXPECTED_PROFILE_SHA256:="1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2";
EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard813_v7_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="A6DA324A48D4810C3DC6A434DA22388FA42C86400FCDC20A1CFD9F1437A0896D";
S813_RECORDS:=[
rec(k:=15894,first:=818,last:=1096,unitFirst:=1,unitLast:=279,order:=49152,autOrder:=786432,parity:=3,classes:=1096,raw:=53870592,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=2400),
rec(k:=15895,first:=1,last:=320,unitFirst:=280,unitLast:=599,order:=49152,autOrder:=1572864,parity:=3,classes:=320,raw:=15728640,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=2002),
rec(k:=15896,first:=1,last:=316,unitFirst:=600,unitLast:=915,order:=49152,autOrder:=1572864,parity:=3,classes:=320,raw:=15728640,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1668)
];
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard813_v7_gpt56sol.g");
