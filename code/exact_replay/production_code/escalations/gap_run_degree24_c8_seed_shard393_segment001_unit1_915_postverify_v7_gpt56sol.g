# Exact wrapper for sealed degree-24 seed workload shard393.
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD393_SEGMENT001_UNIT1_915_POSTVERIFY_V7_GPT56SOL.txt";
STOP_AFTER_UNIT:=fail;
INTERNAL_GUARD_MS:=1320000; START_UNIT:=1;
INITIAL_COUNTERS:=[0,0,0,0,0,0,0,0,0,0,0,0];
PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";
PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0;
PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";
CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD393_CHECKPOINT_GPT56SOL.txt";
CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD393_CHECKPOINT_TMP_GPT56SOL.txt";
EXPECTED_PROFILE_SHA256:="1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2";
EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard393_v7_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="ABCEE1363C55F158B82BEA031DA7C3871DA02EE07D1E7CB18DF79B5A24BF83AA";
S393_RECORDS:=[
rec(k:=15018,first:=137,last:=206,unitFirst:=1,unitLast:=70,order:=49152,autOrder:=9437184,parity:=7,classes:=206,raw:=10125312,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1615),
rec(k:=15019,first:=1,last:=96,unitFirst:=71,unitLast:=166,order:=49152,autOrder:=1572864,parity:=7,classes:=96,raw:=4718592,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1631),
rec(k:=15020,first:=1,last:=242,unitFirst:=167,unitLast:=408,order:=49152,autOrder:=9437184,parity:=7,classes:=242,raw:=11894784,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1728),
rec(k:=15021,first:=1,last:=272,unitFirst:=409,unitLast:=680,order:=49152,autOrder:=3145728,parity:=3,classes:=272,raw:=13369344,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=2087),
rec(k:=15022,first:=1,last:=235,unitFirst:=681,unitLast:=915,order:=49152,autOrder:=3145728,parity:=3,classes:=272,raw:=13369344,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=2571)
];
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard393_v7_gpt56sol.g");
