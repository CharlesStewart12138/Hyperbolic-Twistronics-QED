# Exact wrapper for sealed degree-24 seed workload shard239.
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD239_SEGMENT001_UNIT1_1831_POSTVERIFY_V7_GPT56SOL.txt";
STOP_AFTER_UNIT:=fail;
INTERNAL_GUARD_MS:=1320000; START_UNIT:=1;
INITIAL_COUNTERS:=[0,0,0,0,0,0,0,0,0,0,0,0];
PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";
PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0;
PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";
CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD239_CHECKPOINT_GPT56SOL.txt";
CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD239_CHECKPOINT_TMP_GPT56SOL.txt";
EXPECTED_PROFILE_SHA256:="1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2";
EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard239_v7_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="3B00A0CFD0814F1AB8AF1BE52A5D697D1A4825FA594234024D903ABC816F4C68";
S239_RECORDS:=[
rec(k:=13671,first:=305,last:=560,unitFirst:=1,unitLast:=256,order:=24576,autOrder:=3145728,parity:=3,classes:=560,raw:=13762560,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1566),
rec(k:=13672,first:=1,last:=774,unitFirst:=257,unitLast:=1030,order:=24576,autOrder:=9437184,parity:=3,classes:=774,raw:=19021824,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=2233),
rec(k:=13673,first:=1,last:=192,unitFirst:=1031,unitLast:=1222,order:=24576,autOrder:=393216,parity:=7,classes:=192,raw:=4718592,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1354),
rec(k:=13674,first:=1,last:=348,unitFirst:=1223,unitLast:=1570,order:=24576,autOrder:=393216,parity:=7,classes:=348,raw:=8552448,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1347),
rec(k:=13675,first:=1,last:=242,unitFirst:=1571,unitLast:=1812,order:=24576,autOrder:=393216,parity:=3,classes:=242,raw:=5947392,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1368),
rec(k:=13676,first:=1,last:=19,unitFirst:=1813,unitLast:=1831,order:=24576,autOrder:=393216,parity:=7,classes:=192,raw:=4718592,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1484)
];
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard239_v7_gpt56sol.g");
