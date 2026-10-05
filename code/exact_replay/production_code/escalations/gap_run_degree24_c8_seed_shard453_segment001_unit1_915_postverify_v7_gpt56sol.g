# Exact wrapper for sealed degree-24 seed workload shard453.
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD453_SEGMENT001_UNIT1_915_POSTVERIFY_V7_GPT56SOL.txt";
STOP_AFTER_UNIT:=fail;
INTERNAL_GUARD_MS:=1320000; START_UNIT:=1;
INITIAL_COUNTERS:=[0,0,0,0,0,0,0,0,0,0,0,0];
PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";
PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0;
PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";
CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD453_CHECKPOINT_GPT56SOL.txt";
CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD453_CHECKPOINT_TMP_GPT56SOL.txt";
EXPECTED_PROFILE_SHA256:="1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2";
EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard453_v7_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="A59A2E3A4DB82A37B568DF4DBCBB068FE62705B33CFFC1A15D5C2D0D83462868";
S453_RECORDS:=[
rec(k:=15181,first:=97,last:=320,unitFirst:=1,unitLast:=224,order:=49152,autOrder:=1572864,parity:=3,classes:=320,raw:=15728640,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1745),
rec(k:=15182,first:=1,last:=320,unitFirst:=225,unitLast:=544,order:=49152,autOrder:=1572864,parity:=3,classes:=320,raw:=15728640,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1643),
rec(k:=15183,first:=1,last:=356,unitFirst:=545,unitLast:=900,order:=49152,autOrder:=3145728,parity:=3,classes:=356,raw:=17498112,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=2014),
rec(k:=15184,first:=1,last:=15,unitFirst:=901,unitLast:=915,order:=49152,autOrder:=1572864,parity:=3,classes:=320,raw:=15728640,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1534)
];
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard453_v7_gpt56sol.g");
