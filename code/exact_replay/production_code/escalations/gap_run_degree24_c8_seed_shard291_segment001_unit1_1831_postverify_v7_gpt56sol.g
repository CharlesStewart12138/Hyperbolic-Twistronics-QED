# Exact wrapper for sealed degree-24 seed workload shard291.
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD291_SEGMENT001_UNIT1_1831_POSTVERIFY_V7_GPT56SOL.txt";
STOP_AFTER_UNIT:=fail;
INTERNAL_GUARD_MS:=1320000; START_UNIT:=1;
INITIAL_COUNTERS:=[0,0,0,0,0,0,0,0,0,0,0,0];
PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";
PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0;
PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";
CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD291_CHECKPOINT_GPT56SOL.txt";
CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD291_CHECKPOINT_TMP_GPT56SOL.txt";
EXPECTED_PROFILE_SHA256:="1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2";
EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard291_v7_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="60ED930D3B35697915C6C724238103FB0A0F390FD4F65AB4D9831DA285A007EB";
S291_RECORDS:=[
rec(k:=13905,first:=13,last:=268,unitFirst:=1,unitLast:=256,order:=24576,autOrder:=196608,parity:=3,classes:=268,raw:=6586368,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=882),
rec(k:=13906,first:=1,last:=414,unitFirst:=257,unitLast:=670,order:=24576,autOrder:=393216,parity:=7,classes:=414,raw:=10174464,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1050),
rec(k:=13907,first:=1,last:=392,unitFirst:=671,unitLast:=1062,order:=24576,autOrder:=196608,parity:=7,classes:=392,raw:=9633792,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=986),
rec(k:=13908,first:=1,last:=98,unitFirst:=1063,unitLast:=1160,order:=24576,autOrder:=1572864,parity:=7,classes:=98,raw:=2408448,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1095),
rec(k:=13909,first:=1,last:=378,unitFirst:=1161,unitLast:=1538,order:=24576,autOrder:=393216,parity:=7,classes:=378,raw:=9289728,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1258),
rec(k:=13910,first:=1,last:=293,unitFirst:=1539,unitLast:=1831,order:=24576,autOrder:=3145728,parity:=7,classes:=1080,raw:=26542080,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=4031)
];
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard291_v7_gpt56sol.g");
