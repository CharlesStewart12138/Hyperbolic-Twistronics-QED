# Exact wrapper for sealed degree-24 seed workload shard256.
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD256_SEGMENT001_UNIT1_1831_POSTVERIFY_V7_GPT56SOL.txt";
STOP_AFTER_UNIT:=fail;
INTERNAL_GUARD_MS:=1320000; START_UNIT:=1;
INITIAL_COUNTERS:=[0,0,0,0,0,0,0,0,0,0,0,0];
PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";
PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0;
PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";
CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD256_CHECKPOINT_GPT56SOL.txt";
CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD256_CHECKPOINT_TMP_GPT56SOL.txt";
EXPECTED_PROFILE_SHA256:="1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2";
EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard256_v7_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="29BFCBDD139C5F59252A17743847EF77D8E39C9D7A91C4A6375B798530C74B96";
S256_RECORDS:=[
rec(k:=13757,first:=303,last:=336,unitFirst:=1,unitLast:=34,order:=24576,autOrder:=196608,parity:=7,classes:=336,raw:=8257536,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1434),
rec(k:=13758,first:=1,last:=336,unitFirst:=35,unitLast:=370,order:=24576,autOrder:=196608,parity:=7,classes:=336,raw:=8257536,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1058),
rec(k:=13759,first:=1,last:=336,unitFirst:=371,unitLast:=706,order:=24576,autOrder:=196608,parity:=7,classes:=336,raw:=8257536,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1495),
rec(k:=13760,first:=1,last:=880,unitFirst:=707,unitLast:=1586,order:=24576,autOrder:=393216,parity:=7,classes:=880,raw:=21626880,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1376),
rec(k:=13761,first:=1,last:=245,unitFirst:=1587,unitLast:=1831,order:=24576,autOrder:=393216,parity:=7,classes:=880,raw:=21626880,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=2030)
];
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard256_v7_gpt56sol.g");
