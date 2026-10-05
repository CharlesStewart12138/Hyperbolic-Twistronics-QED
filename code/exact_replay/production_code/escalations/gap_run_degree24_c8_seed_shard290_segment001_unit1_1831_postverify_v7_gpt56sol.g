# Exact wrapper for sealed degree-24 seed workload shard290.
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD290_SEGMENT001_UNIT1_1831_POSTVERIFY_V7_GPT56SOL.txt";
STOP_AFTER_UNIT:=fail;
INTERNAL_GUARD_MS:=1320000; START_UNIT:=1;
INITIAL_COUNTERS:=[0,0,0,0,0,0,0,0,0,0,0,0];
PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";
PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0;
PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";
CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD290_CHECKPOINT_GPT56SOL.txt";
CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD290_CHECKPOINT_TMP_GPT56SOL.txt";
EXPECTED_PROFILE_SHA256:="1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2";
EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard290_v7_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="C8C562C3A097D3886D7EC668C5AA11B78F91660EE6C7C04318C3B1015FE6073C";
S290_RECORDS:=[
rec(k:=13902,first:=630,last:=1368,unitFirst:=1,unitLast:=739,order:=24576,autOrder:=50331648,parity:=7,classes:=1368,raw:=33619968,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=16457),
rec(k:=13903,first:=1,last:=540,unitFirst:=740,unitLast:=1279,order:=24576,autOrder:=393216,parity:=7,classes:=540,raw:=13271040,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1434),
rec(k:=13904,first:=1,last:=540,unitFirst:=1280,unitLast:=1819,order:=24576,autOrder:=393216,parity:=7,classes:=540,raw:=13271040,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1486),
rec(k:=13905,first:=1,last:=12,unitFirst:=1820,unitLast:=1831,order:=24576,autOrder:=196608,parity:=3,classes:=268,raw:=6586368,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=882)
];
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard290_v7_gpt56sol.g");
