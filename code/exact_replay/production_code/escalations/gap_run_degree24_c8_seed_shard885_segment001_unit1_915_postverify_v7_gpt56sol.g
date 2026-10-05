# Exact wrapper for sealed degree-24 seed workload shard885.
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD885_SEGMENT001_UNIT1_915_POSTVERIFY_V7_GPT56SOL.txt";
STOP_AFTER_UNIT:=fail;
INTERNAL_GUARD_MS:=1320000; START_UNIT:=1;
INITIAL_COUNTERS:=[0,0,0,0,0,0,0,0,0,0,0,0];
PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";
PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0;
PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";
CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD885_CHECKPOINT_GPT56SOL.txt";
CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD885_CHECKPOINT_TMP_GPT56SOL.txt";
EXPECTED_PROFILE_SHA256:="1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2";
EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard885_v7_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="9C3A20253CFF05BEC0479C21F33A048A59CAC56C18E5610300946C3F15946831";
S885_RECORDS:=[
rec(k:=15951,first:=356,last:=422,unitFirst:=1,unitLast:=67,order:=49152,autOrder:=6291456,parity:=3,classes:=422,raw:=20742144,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1855),
rec(k:=15952,first:=1,last:=96,unitFirst:=68,unitLast:=163,order:=49152,autOrder:=393216,parity:=3,classes:=96,raw:=4718592,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1244),
rec(k:=15953,first:=1,last:=446,unitFirst:=164,unitLast:=609,order:=49152,autOrder:=6291456,parity:=3,classes:=446,raw:=21921792,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=2586),
rec(k:=15954,first:=1,last:=96,unitFirst:=610,unitLast:=705,order:=49152,autOrder:=393216,parity:=3,classes:=96,raw:=4718592,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=957),
rec(k:=15955,first:=1,last:=96,unitFirst:=706,unitLast:=801,order:=49152,autOrder:=393216,parity:=3,classes:=96,raw:=4718592,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=724),
rec(k:=15956,first:=1,last:=114,unitFirst:=802,unitLast:=915,order:=49152,autOrder:=3145728,parity:=3,classes:=274,raw:=13467648,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1449)
];
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard885_v7_gpt56sol.g");
