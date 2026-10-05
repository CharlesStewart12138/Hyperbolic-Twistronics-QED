# Exact wrapper for sealed degree-24 seed workload shard333.
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD333_SEGMENT001_UNIT1_915_POSTVERIFY_V7_GPT56SOL.txt";
STOP_AFTER_UNIT:=fail;
INTERNAL_GUARD_MS:=1320000; START_UNIT:=1;
INITIAL_COUNTERS:=[0,0,0,0,0,0,0,0,0,0,0,0];
PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";
PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0;
PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";
CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD333_CHECKPOINT_GPT56SOL.txt";
CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD333_CHECKPOINT_TMP_GPT56SOL.txt";
EXPECTED_PROFILE_SHA256:="1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2";
EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard333_v7_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="0B9B0D5BB6C8868F92929AD1EF6580874240B8F85ACE866169A33B3065DBB91D";
S333_RECORDS:=[
rec(k:=14777,first:=29,last:=206,unitFirst:=1,unitLast:=178,order:=49152,autOrder:=9437184,parity:=3,classes:=206,raw:=10125312,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=2208),
rec(k:=14778,first:=1,last:=206,unitFirst:=179,unitLast:=384,order:=49152,autOrder:=9437184,parity:=3,classes:=206,raw:=10125312,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1401),
rec(k:=14779,first:=1,last:=206,unitFirst:=385,unitLast:=590,order:=49152,autOrder:=9437184,parity:=7,classes:=206,raw:=10125312,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1035),
rec(k:=14780,first:=1,last:=206,unitFirst:=591,unitLast:=796,order:=49152,autOrder:=9437184,parity:=7,classes:=206,raw:=10125312,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1508),
rec(k:=14781,first:=1,last:=119,unitFirst:=797,unitLast:=915,order:=49152,autOrder:=6291456,parity:=3,classes:=446,raw:=21921792,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=3160)
];
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard333_v7_gpt56sol.g");
