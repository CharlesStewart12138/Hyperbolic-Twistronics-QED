# Exact wrapper for sealed degree-24 seed workload shard441.
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD441_SEGMENT001_UNIT1_915_POSTVERIFY_V7_GPT56SOL.txt";
STOP_AFTER_UNIT:=fail;
INTERNAL_GUARD_MS:=1320000; START_UNIT:=1;
INITIAL_COUNTERS:=[0,0,0,0,0,0,0,0,0,0,0,0];
PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";
PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0;
PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";
CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD441_CHECKPOINT_GPT56SOL.txt";
CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD441_CHECKPOINT_TMP_GPT56SOL.txt";
EXPECTED_PROFILE_SHA256:="1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2";
EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard441_v7_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="9A96C14FC685ABC940DDF5FF37031D54DF476FFCAAC3FC630419A11DCDF8B92C";
S441_RECORDS:=[
rec(k:=15150,first:=1477,last:=2120,unitFirst:=1,unitLast:=644,order:=49152,autOrder:=6291456,parity:=7,classes:=2120,raw:=104202240,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=3971),
rec(k:=15151,first:=1,last:=128,unitFirst:=645,unitLast:=772,order:=49152,autOrder:=786432,parity:=1,classes:=128,raw:=6291456,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=935),
rec(k:=15152,first:=1,last:=124,unitFirst:=773,unitLast:=896,order:=49152,autOrder:=786432,parity:=3,classes:=124,raw:=6094848,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1127),
rec(k:=15153,first:=1,last:=19,unitFirst:=897,unitLast:=915,order:=49152,autOrder:=786432,parity:=3,classes:=104,raw:=5111808,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1057)
];
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard441_v7_gpt56sol.g");
