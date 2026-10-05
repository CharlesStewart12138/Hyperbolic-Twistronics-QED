# Exact wrapper for sealed degree-24 seed workload shard381.
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD381_SEGMENT001_UNIT1_915_POSTVERIFY_V7_GPT56SOL.txt";
STOP_AFTER_UNIT:=fail;
INTERNAL_GUARD_MS:=1320000; START_UNIT:=1;
INITIAL_COUNTERS:=[0,0,0,0,0,0,0,0,0,0,0,0];
PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";
PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0;
PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";
CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD381_CHECKPOINT_GPT56SOL.txt";
CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD381_CHECKPOINT_TMP_GPT56SOL.txt";
EXPECTED_PROFILE_SHA256:="1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2";
EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard381_v7_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="7A75EA27CE46A8056C5E92E8893ADA68F9F93EABF21B25A80B6A298950360A72";
S381_RECORDS:=[
rec(k:=14974,first:=101,last:=320,unitFirst:=1,unitLast:=220,order:=49152,autOrder:=1572864,parity:=3,classes:=320,raw:=15728640,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1533),
rec(k:=14975,first:=1,last:=199,unitFirst:=221,unitLast:=419,order:=49152,autOrder:=37748736,parity:=7,classes:=199,raw:=9781248,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1466),
rec(k:=14976,first:=1,last:=241,unitFirst:=420,unitLast:=660,order:=49152,autOrder:=6291456,parity:=3,classes:=241,raw:=11845632,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1459),
rec(k:=14977,first:=1,last:=199,unitFirst:=661,unitLast:=859,order:=49152,autOrder:=37748736,parity:=7,classes:=199,raw:=9781248,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1764),
rec(k:=14978,first:=1,last:=56,unitFirst:=860,unitLast:=915,order:=49152,autOrder:=6291456,parity:=3,classes:=241,raw:=11845632,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1800)
];
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard381_v7_gpt56sol.g");
