# Exact wrapper for sealed degree-24 seed workload shard793.
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD793_SEGMENT001_UNIT1_915_POSTVERIFY_V7_GPT56SOL.txt";
STOP_AFTER_UNIT:=fail;
INTERNAL_GUARD_MS:=1320000; START_UNIT:=1;
INITIAL_COUNTERS:=[0,0,0,0,0,0,0,0,0,0,0,0];
PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";
PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0;
PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";
CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD793_CHECKPOINT_GPT56SOL.txt";
CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD793_CHECKPOINT_TMP_GPT56SOL.txt";
EXPECTED_PROFILE_SHA256:="1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2";
EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard793_v7_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="7DB9A424DC41FF7C127C81FC2C3FB56E565F7D8988A2DA9D908788FEAA69E726";
S793_RECORDS:=[
rec(k:=15864,first:=1254,last:=1376,unitFirst:=1,unitLast:=123,order:=49152,autOrder:=3145728,parity:=7,classes:=1376,raw:=67633152,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=3244),
rec(k:=15865,first:=1,last:=256,unitFirst:=124,unitLast:=379,order:=49152,autOrder:=786432,parity:=7,classes:=256,raw:=12582912,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1664),
rec(k:=15866,first:=1,last:=320,unitFirst:=380,unitLast:=699,order:=49152,autOrder:=1572864,parity:=3,classes:=320,raw:=15728640,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=2467),
rec(k:=15867,first:=1,last:=216,unitFirst:=700,unitLast:=915,order:=49152,autOrder:=786432,parity:=3,classes:=672,raw:=33030144,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1666)
];
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard793_v7_gpt56sol.g");
