# Exact wrapper for sealed degree-24 seed workload shard299.
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD299_SEGMENT001_UNIT1_1831_POSTVERIFY_V7_GPT56SOL.txt";
STOP_AFTER_UNIT:=fail;
INTERNAL_GUARD_MS:=1320000; START_UNIT:=1;
INITIAL_COUNTERS:=[0,0,0,0,0,0,0,0,0,0,0,0];
PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";
PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0;
PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";
CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD299_CHECKPOINT_GPT56SOL.txt";
CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD299_CHECKPOINT_TMP_GPT56SOL.txt";
EXPECTED_PROFILE_SHA256:="1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2";
EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard299_v7_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="C77CE1B88DA89F5BB4FAE4CA5A12618DD96E8FC2A20C008C5565B2E75534C099";
S299_RECORDS:=[
rec(k:=13937,first:=587,last:=696,unitFirst:=1,unitLast:=110,order:=24576,autOrder:=6291456,parity:=7,classes:=696,raw:=17104896,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=2556),
rec(k:=13938,first:=1,last:=592,unitFirst:=111,unitLast:=702,order:=24576,autOrder:=3145728,parity:=7,classes:=592,raw:=14548992,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1674),
rec(k:=13939,first:=1,last:=884,unitFirst:=703,unitLast:=1586,order:=24576,autOrder:=6291456,parity:=7,classes:=884,raw:=21725184,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=3215),
rec(k:=13940,first:=1,last:=245,unitFirst:=1587,unitLast:=1831,order:=24576,autOrder:=196608,parity:=7,classes:=440,raw:=10813440,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=980)
];
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard299_v7_gpt56sol.g");
