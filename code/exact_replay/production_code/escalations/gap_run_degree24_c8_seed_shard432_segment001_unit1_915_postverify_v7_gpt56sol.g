# Exact wrapper for sealed degree-24 seed workload shard432.
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD432_SEGMENT001_UNIT1_915_POSTVERIFY_V7_GPT56SOL.txt";
STOP_AFTER_UNIT:=fail;
INTERNAL_GUARD_MS:=1320000; START_UNIT:=1;
INITIAL_COUNTERS:=[0,0,0,0,0,0,0,0,0,0,0,0];
PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";
PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0;
PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";
CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD432_CHECKPOINT_GPT56SOL.txt";
CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD432_CHECKPOINT_TMP_GPT56SOL.txt";
EXPECTED_PROFILE_SHA256:="1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2";
EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard432_v7_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="633B189532E7F28A34E6CA51ED49BD424780799F1F570DC1C2893D331C5848E9";
S432_RECORDS:=[
rec(k:=15132,first:=98,last:=320,unitFirst:=1,unitLast:=223,order:=49152,autOrder:=1572864,parity:=3,classes:=320,raw:=15728640,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1949),
rec(k:=15133,first:=1,last:=241,unitFirst:=224,unitLast:=464,order:=49152,autOrder:=6291456,parity:=3,classes:=241,raw:=11845632,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1329),
rec(k:=15134,first:=1,last:=260,unitFirst:=465,unitLast:=724,order:=49152,autOrder:=6291456,parity:=3,classes:=260,raw:=12779520,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=2756),
rec(k:=15135,first:=1,last:=80,unitFirst:=725,unitLast:=804,order:=49152,autOrder:=786432,parity:=1,classes:=80,raw:=3932160,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1403),
rec(k:=15136,first:=1,last:=111,unitFirst:=805,unitLast:=915,order:=49152,autOrder:=3145728,parity:=3,classes:=256,raw:=12582912,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1468)
];
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard432_v7_gpt56sol.g");
