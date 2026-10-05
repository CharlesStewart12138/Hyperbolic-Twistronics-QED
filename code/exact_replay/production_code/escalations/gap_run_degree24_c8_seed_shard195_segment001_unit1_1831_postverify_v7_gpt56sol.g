# Exact wrapper for sealed degree-24 seed workload shard195.
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD195_SEGMENT001_UNIT1_1831_POSTVERIFY_V7_GPT56SOL.txt";
STOP_AFTER_UNIT:=fail;
INTERNAL_GUARD_MS:=1320000; START_UNIT:=1;
INITIAL_COUNTERS:=[0,0,0,0,0,0,0,0,0,0,0,0];
PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";
PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0;
PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";
CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD195_CHECKPOINT_GPT56SOL.txt";
CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD195_CHECKPOINT_TMP_GPT56SOL.txt";
EXPECTED_PROFILE_SHA256:="1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2";
EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard195_v7_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="DE5B114F822A50215EE104A5C3C05DBC61BD2D3DA6237B18A9EA53B0D8AA64D0";
S195_RECORDS:=[
rec(k:=13422,first:=65,last:=344,unitFirst:=1,unitLast:=280,order:=24576,autOrder:=1179648,parity:=15,classes:=344,raw:=8454144,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1934),
rec(k:=13423,first:=1,last:=384,unitFirst:=281,unitLast:=664,order:=24576,autOrder:=393216,parity:=15,classes:=384,raw:=9437184,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=2464),
rec(k:=13424,first:=1,last:=376,unitFirst:=665,unitLast:=1040,order:=24576,autOrder:=786432,parity:=15,classes:=376,raw:=9240576,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=2595),
rec(k:=13425,first:=1,last:=791,unitFirst:=1041,unitLast:=1831,order:=24576,autOrder:=786432,parity:=15,classes:=960,raw:=23592960,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=2356)
];
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard195_v7_gpt56sol.g");
