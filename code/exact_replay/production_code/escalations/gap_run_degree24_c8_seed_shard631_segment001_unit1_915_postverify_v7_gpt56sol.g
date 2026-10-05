# Exact wrapper for sealed degree-24 seed workload shard631.
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD631_SEGMENT001_UNIT1_915_POSTVERIFY_V7_GPT56SOL.txt";
STOP_AFTER_UNIT:=fail;
INTERNAL_GUARD_MS:=1320000; START_UNIT:=1;
INITIAL_COUNTERS:=[0,0,0,0,0,0,0,0,0,0,0,0];
PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";
PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0;
PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";
CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD631_CHECKPOINT_GPT56SOL.txt";
CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD631_CHECKPOINT_TMP_GPT56SOL.txt";
EXPECTED_PROFILE_SHA256:="1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2";
EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard631_v7_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="C666659E9E9A7797C5FB9FD9FDDF3FC5C03F46F14A230D73D06B76833554FC08";
S631_RECORDS:=[
rec(k:=15635,first:=942,last:=944,unitFirst:=1,unitLast:=3,order:=49152,autOrder:=3145728,parity:=7,classes:=944,raw:=46399488,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=2621),
rec(k:=15636,first:=1,last:=464,unitFirst:=4,unitLast:=467,order:=49152,autOrder:=3145728,parity:=7,classes:=464,raw:=22806528,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1904),
rec(k:=15637,first:=1,last:=132,unitFirst:=468,unitLast:=599,order:=49152,autOrder:=1572864,parity:=7,classes:=132,raw:=6488064,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1080),
rec(k:=15638,first:=1,last:=196,unitFirst:=600,unitLast:=795,order:=49152,autOrder:=1572864,parity:=7,classes:=196,raw:=9633792,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=2127),
rec(k:=15639,first:=1,last:=120,unitFirst:=796,unitLast:=915,order:=49152,autOrder:=1572864,parity:=3,classes:=368,raw:=18087936,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=2962)
];
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard631_v7_gpt56sol.g");
