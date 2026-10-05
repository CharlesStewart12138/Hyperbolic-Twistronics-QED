# Exact wrapper for sealed degree-24 seed workload shard345.
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD345_SEGMENT001_UNIT1_915_POSTVERIFY_V7_GPT56SOL.txt";
STOP_AFTER_UNIT:=fail;
INTERNAL_GUARD_MS:=1320000; START_UNIT:=1;
INITIAL_COUNTERS:=[0,0,0,0,0,0,0,0,0,0,0,0];
PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";
PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0;
PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";
CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD345_CHECKPOINT_GPT56SOL.txt";
CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD345_CHECKPOINT_TMP_GPT56SOL.txt";
EXPECTED_PROFILE_SHA256:="1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2";
EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard345_v7_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="405C7D0F7D543445E9A0914D6B2C8AC90C42BBDCD7BC3F9C0BE4A7BEB0723230";
S345_RECORDS:=[
rec(k:=14833,first:=115,last:=176,unitFirst:=1,unitLast:=62,order:=49152,autOrder:=1572864,parity:=7,classes:=176,raw:=8650752,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=2081),
rec(k:=14834,first:=1,last:=152,unitFirst:=63,unitLast:=214,order:=49152,autOrder:=1572864,parity:=7,classes:=152,raw:=7471104,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1495),
rec(k:=14835,first:=1,last:=160,unitFirst:=215,unitLast:=374,order:=49152,autOrder:=1572864,parity:=7,classes:=160,raw:=7864320,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1793),
rec(k:=14836,first:=1,last:=168,unitFirst:=375,unitLast:=542,order:=49152,autOrder:=1572864,parity:=7,classes:=168,raw:=8257536,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1527),
rec(k:=14837,first:=1,last:=160,unitFirst:=543,unitLast:=702,order:=49152,autOrder:=393216,parity:=7,classes:=160,raw:=7864320,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1139),
rec(k:=14838,first:=1,last:=128,unitFirst:=703,unitLast:=830,order:=49152,autOrder:=393216,parity:=7,classes:=128,raw:=6291456,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=877),
rec(k:=14839,first:=1,last:=85,unitFirst:=831,unitLast:=915,order:=49152,autOrder:=3145728,parity:=31,classes:=476,raw:=23396352,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=2492)
];
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard345_v7_gpt56sol.g");
