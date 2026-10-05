# Exact wrapper for sealed degree-24 seed workload shard295.
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD295_SEGMENT001_UNIT1_1831_POSTVERIFY_V7_GPT56SOL.txt";
STOP_AFTER_UNIT:=fail;
INTERNAL_GUARD_MS:=1320000; START_UNIT:=1;
INITIAL_COUNTERS:=[0,0,0,0,0,0,0,0,0,0,0,0];
PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";
PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0;
PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";
CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD295_CHECKPOINT_GPT56SOL.txt";
CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD295_CHECKPOINT_TMP_GPT56SOL.txt";
EXPECTED_PROFILE_SHA256:="1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2";
EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard295_v7_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="391E164060ED833AA7DBECFE202217FB9C85AE33310F350AA7034C535BAC15E6";
S295_RECORDS:=[
rec(k:=13927,first:=7,last:=440,unitFirst:=1,unitLast:=434,order:=24576,autOrder:=196608,parity:=7,classes:=440,raw:=10813440,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1100),
rec(k:=13928,first:=1,last:=440,unitFirst:=435,unitLast:=874,order:=24576,autOrder:=196608,parity:=7,classes:=440,raw:=10813440,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1146),
rec(k:=13929,first:=1,last:=392,unitFirst:=875,unitLast:=1266,order:=24576,autOrder:=196608,parity:=7,classes:=392,raw:=9633792,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=960),
rec(k:=13930,first:=1,last:=392,unitFirst:=1267,unitLast:=1658,order:=24576,autOrder:=196608,parity:=7,classes:=392,raw:=9633792,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1008),
rec(k:=13931,first:=1,last:=173,unitFirst:=1659,unitLast:=1831,order:=24576,autOrder:=196608,parity:=7,classes:=440,raw:=10813440,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1030)
];
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard295_v7_gpt56sol.g");
