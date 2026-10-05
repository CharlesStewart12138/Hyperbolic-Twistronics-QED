# Exact wrapper for sealed degree-24 seed workload shard285.
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD285_SEGMENT001_UNIT1_1831_POSTVERIFY_V7_GPT56SOL.txt";
STOP_AFTER_UNIT:=fail;
INTERNAL_GUARD_MS:=1320000; START_UNIT:=1;
INITIAL_COUNTERS:=[0,0,0,0,0,0,0,0,0,0,0,0];
PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";
PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0;
PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";
CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD285_CHECKPOINT_GPT56SOL.txt";
CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD285_CHECKPOINT_TMP_GPT56SOL.txt";
EXPECTED_PROFILE_SHA256:="1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2";
EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard285_v7_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="8E224D791C91D1F66FB4ED3D3AAAFA8B5913EA24ABB051699E3D398816A864F2";
S285_RECORDS:=[
rec(k:=13882,first:=98,last:=1280,unitFirst:=1,unitLast:=1183,order:=24576,autOrder:=393216,parity:=7,classes:=1280,raw:=31457280,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=2350),
rec(k:=13883,first:=1,last:=435,unitFirst:=1184,unitLast:=1618,order:=24576,autOrder:=25165824,parity:=15,classes:=435,raw:=10690560,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=3228),
rec(k:=13884,first:=1,last:=96,unitFirst:=1619,unitLast:=1714,order:=24576,autOrder:=393216,parity:=3,classes:=96,raw:=2359296,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1008),
rec(k:=13885,first:=1,last:=117,unitFirst:=1715,unitLast:=1831,order:=24576,autOrder:=196608,parity:=3,classes:=292,raw:=7176192,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=853)
];
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard285_v7_gpt56sol.g");
