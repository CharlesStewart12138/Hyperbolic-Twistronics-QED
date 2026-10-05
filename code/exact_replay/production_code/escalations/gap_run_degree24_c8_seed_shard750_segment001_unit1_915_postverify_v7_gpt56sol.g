# Exact wrapper for sealed degree-24 seed workload shard750.
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD750_SEGMENT001_UNIT1_915_POSTVERIFY_V7_GPT56SOL.txt";
STOP_AFTER_UNIT:=fail;
INTERNAL_GUARD_MS:=1320000; START_UNIT:=1;
INITIAL_COUNTERS:=[0,0,0,0,0,0,0,0,0,0,0,0];
PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";
PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0;
PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";
CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD750_CHECKPOINT_GPT56SOL.txt";
CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD750_CHECKPOINT_TMP_GPT56SOL.txt";
EXPECTED_PROFILE_SHA256:="1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2";
EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard750_v7_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="AE20FEF59B81CEACE3452456EFCD08778D3FD639FF1571DBA22AF89070AC68EC";
S750_RECORDS:=[
rec(k:=15800,first:=168,last:=200,unitFirst:=1,unitLast:=33,order:=49152,autOrder:=786432,parity:=15,classes:=200,raw:=9830400,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1916),
rec(k:=15801,first:=1,last:=48,unitFirst:=34,unitLast:=81,order:=49152,autOrder:=393216,parity:=7,classes:=48,raw:=2359296,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=777),
rec(k:=15802,first:=1,last:=320,unitFirst:=82,unitLast:=401,order:=49152,autOrder:=393216,parity:=7,classes:=320,raw:=15728640,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1063),
rec(k:=15803,first:=1,last:=292,unitFirst:=402,unitLast:=693,order:=49152,autOrder:=1572864,parity:=15,classes:=292,raw:=14352384,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1400),
rec(k:=15804,first:=1,last:=72,unitFirst:=694,unitLast:=765,order:=49152,autOrder:=786432,parity:=15,classes:=72,raw:=3538944,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=953),
rec(k:=15805,first:=1,last:=144,unitFirst:=766,unitLast:=909,order:=49152,autOrder:=393216,parity:=7,classes:=144,raw:=7077888,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1207),
rec(k:=15806,first:=1,last:=6,unitFirst:=910,unitLast:=915,order:=49152,autOrder:=393216,parity:=7,classes:=256,raw:=12582912,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1646)
];
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard750_v7_gpt56sol.g");
