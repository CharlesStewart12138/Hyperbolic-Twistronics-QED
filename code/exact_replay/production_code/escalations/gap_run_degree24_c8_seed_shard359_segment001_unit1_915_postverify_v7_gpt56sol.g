# Exact wrapper for sealed degree-24 seed workload shard359.
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD359_SEGMENT001_UNIT1_915_POSTVERIFY_V7_GPT56SOL.txt";
STOP_AFTER_UNIT:=fail;
INTERNAL_GUARD_MS:=1320000; START_UNIT:=1;
INITIAL_COUNTERS:=[0,0,0,0,0,0,0,0,0,0,0,0];
PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";
PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0;
PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";
CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD359_CHECKPOINT_GPT56SOL.txt";
CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD359_CHECKPOINT_TMP_GPT56SOL.txt";
EXPECTED_PROFILE_SHA256:="1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2";
EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard359_v7_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="9BB4A1EC60821FCCACEB5FD16D6E7D11A7E6FBB8F76F711B227EE96CBBDA4E79";
S359_RECORDS:=[
rec(k:=14896,first:=85,last:=224,unitFirst:=1,unitLast:=140,order:=49152,autOrder:=1572864,parity:=7,classes:=224,raw:=11010048,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=2286),
rec(k:=14897,first:=1,last:=208,unitFirst:=141,unitLast:=348,order:=49152,autOrder:=1572864,parity:=3,classes:=208,raw:=10223616,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=2666),
rec(k:=14898,first:=1,last:=184,unitFirst:=349,unitLast:=532,order:=49152,autOrder:=1572864,parity:=3,classes:=184,raw:=9043968,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=2079),
rec(k:=14899,first:=1,last:=160,unitFirst:=533,unitLast:=692,order:=49152,autOrder:=1572864,parity:=3,classes:=160,raw:=7864320,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1989),
rec(k:=14900,first:=1,last:=164,unitFirst:=693,unitLast:=856,order:=49152,autOrder:=1572864,parity:=3,classes:=164,raw:=8060928,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1343),
rec(k:=14901,first:=1,last:=59,unitFirst:=857,unitLast:=915,order:=49152,autOrder:=1572864,parity:=7,classes:=152,raw:=7471104,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1675)
];
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard359_v7_gpt56sol.g");
