# Exact wrapper for sealed degree-24 seed workload shard520.
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD520_SEGMENT001_UNIT1_915_POSTVERIFY_V7_GPT56SOL.txt";
STOP_AFTER_UNIT:=fail;
INTERNAL_GUARD_MS:=1320000; START_UNIT:=1;
INITIAL_COUNTERS:=[0,0,0,0,0,0,0,0,0,0,0,0];
PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";
PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0;
PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";
CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD520_CHECKPOINT_GPT56SOL.txt";
CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD520_CHECKPOINT_TMP_GPT56SOL.txt";
EXPECTED_PROFILE_SHA256:="1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2";
EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard520_v7_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="F1EE3C60505D8F6E66ABA1F9ADE4F59C9E804CDD8F37AFD850450C418BE02B3E";
S520_RECORDS:=[
rec(k:=15343,first:=243,last:=512,unitFirst:=1,unitLast:=270,order:=49152,autOrder:=3145728,parity:=1,classes:=512,raw:=25165824,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=4199),
rec(k:=15344,first:=1,last:=282,unitFirst:=271,unitLast:=552,order:=49152,autOrder:=6291456,parity:=3,classes:=282,raw:=13860864,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=2085),
rec(k:=15345,first:=1,last:=314,unitFirst:=553,unitLast:=866,order:=49152,autOrder:=3145728,parity:=3,classes:=314,raw:=15433728,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1683),
rec(k:=15346,first:=1,last:=49,unitFirst:=867,unitLast:=915,order:=49152,autOrder:=3145728,parity:=3,classes:=308,raw:=15138816,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1573)
];
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard520_v7_gpt56sol.g");
