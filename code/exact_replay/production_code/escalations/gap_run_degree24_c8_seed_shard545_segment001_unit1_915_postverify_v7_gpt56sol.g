# Exact wrapper for sealed degree-24 seed workload shard545.
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD545_SEGMENT001_UNIT1_915_POSTVERIFY_V7_GPT56SOL.txt";
STOP_AFTER_UNIT:=fail;
INTERNAL_GUARD_MS:=1320000; START_UNIT:=1;
INITIAL_COUNTERS:=[0,0,0,0,0,0,0,0,0,0,0,0];
PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";
PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0;
PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";
CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD545_CHECKPOINT_GPT56SOL.txt";
CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD545_CHECKPOINT_TMP_GPT56SOL.txt";
EXPECTED_PROFILE_SHA256:="1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2";
EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard545_v7_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="991258D41D990B5AA432065C75BFA383A81FD224CBD96507255783FC60CB62D8";
S545_RECORDS:=[
rec(k:=15396,first:=163,last:=288,unitFirst:=1,unitLast:=126,order:=49152,autOrder:=1572864,parity:=3,classes:=288,raw:=14155776,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1637),
rec(k:=15397,first:=1,last:=288,unitFirst:=127,unitLast:=414,order:=49152,autOrder:=1572864,parity:=3,classes:=288,raw:=14155776,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1374),
rec(k:=15398,first:=1,last:=321,unitFirst:=415,unitLast:=735,order:=49152,autOrder:=6291456,parity:=3,classes:=321,raw:=15777792,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1352),
rec(k:=15399,first:=1,last:=124,unitFirst:=736,unitLast:=859,order:=49152,autOrder:=786432,parity:=1,classes:=124,raw:=6094848,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1319),
rec(k:=15400,first:=1,last:=56,unitFirst:=860,unitLast:=915,order:=49152,autOrder:=3145728,parity:=3,classes:=356,raw:=17498112,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1826)
];
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard545_v7_gpt56sol.g");
