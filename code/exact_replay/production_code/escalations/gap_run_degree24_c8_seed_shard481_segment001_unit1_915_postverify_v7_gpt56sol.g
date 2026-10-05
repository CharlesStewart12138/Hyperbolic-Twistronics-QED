# Exact wrapper for sealed degree-24 seed workload shard481.
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD481_SEGMENT001_UNIT1_915_POSTVERIFY_V7_GPT56SOL.txt";
STOP_AFTER_UNIT:=fail;
INTERNAL_GUARD_MS:=1320000; START_UNIT:=1;
INITIAL_COUNTERS:=[0,0,0,0,0,0,0,0,0,0,0,0];
PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";
PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0;
PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";
CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD481_CHECKPOINT_GPT56SOL.txt";
CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD481_CHECKPOINT_TMP_GPT56SOL.txt";
EXPECTED_PROFILE_SHA256:="1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2";
EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard481_v7_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="E32732801CCF2C43A441781EFB55BF772F261FCDED89DAF566AF978000FFAEAB";
S481_RECORDS:=[
rec(k:=15234,first:=68,last:=274,unitFirst:=1,unitLast:=207,order:=49152,autOrder:=3145728,parity:=3,classes:=274,raw:=13467648,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1378),
rec(k:=15235,first:=1,last:=144,unitFirst:=208,unitLast:=351,order:=49152,autOrder:=3145728,parity:=3,classes:=144,raw:=7077888,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1498),
rec(k:=15236,first:=1,last:=564,unitFirst:=352,unitLast:=915,order:=49152,autOrder:=3145728,parity:=1,classes:=768,raw:=37748736,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1397)
];
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard481_v7_gpt56sol.g");
