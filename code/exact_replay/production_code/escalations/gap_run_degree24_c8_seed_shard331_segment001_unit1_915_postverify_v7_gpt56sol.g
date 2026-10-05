# Exact wrapper for sealed degree-24 seed workload shard331.
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD331_SEGMENT001_UNIT1_915_POSTVERIFY_V7_GPT56SOL.txt";
STOP_AFTER_UNIT:=fail;
INTERNAL_GUARD_MS:=1320000; START_UNIT:=1;
INITIAL_COUNTERS:=[0,0,0,0,0,0,0,0,0,0,0,0];
PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";
PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0;
PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";
CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD331_CHECKPOINT_GPT56SOL.txt";
CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD331_CHECKPOINT_TMP_GPT56SOL.txt";
EXPECTED_PROFILE_SHA256:="1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2";
EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard331_v7_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="83DF39295BE50405C970EEEDCE935C39A00F7B639707FD6C12AF7A9A5F44348B";
S331_RECORDS:=[
rec(k:=14767,first:=15,last:=132,unitFirst:=1,unitLast:=118,order:=49152,autOrder:=1572864,parity:=7,classes:=132,raw:=6488064,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=2411),
rec(k:=14768,first:=1,last:=132,unitFirst:=119,unitLast:=250,order:=49152,autOrder:=1572864,parity:=3,classes:=132,raw:=6488064,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=2102),
rec(k:=14769,first:=1,last:=152,unitFirst:=251,unitLast:=402,order:=49152,autOrder:=1572864,parity:=7,classes:=152,raw:=7471104,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1556),
rec(k:=14770,first:=1,last:=152,unitFirst:=403,unitLast:=554,order:=49152,autOrder:=1572864,parity:=3,classes:=152,raw:=7471104,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1752),
rec(k:=14771,first:=1,last:=152,unitFirst:=555,unitLast:=706,order:=49152,autOrder:=1572864,parity:=7,classes:=152,raw:=7471104,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1218),
rec(k:=14772,first:=1,last:=152,unitFirst:=707,unitLast:=858,order:=49152,autOrder:=1572864,parity:=3,classes:=152,raw:=7471104,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1521),
rec(k:=14773,first:=1,last:=57,unitFirst:=859,unitLast:=915,order:=49152,autOrder:=3145728,parity:=7,classes:=236,raw:=11599872,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1702)
];
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard331_v7_gpt56sol.g");
