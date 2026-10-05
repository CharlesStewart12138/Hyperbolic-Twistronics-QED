# Exact wrapper for sealed degree-24 seed workload shard242.
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD242_SEGMENT001_UNIT1_1831_POSTVERIFY_V7_GPT56SOL.txt";
STOP_AFTER_UNIT:=fail;
INTERNAL_GUARD_MS:=1320000; START_UNIT:=1;
INITIAL_COUNTERS:=[0,0,0,0,0,0,0,0,0,0,0,0];
PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";
PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0;
PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";
CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD242_CHECKPOINT_GPT56SOL.txt";
CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD242_CHECKPOINT_TMP_GPT56SOL.txt";
EXPECTED_PROFILE_SHA256:="1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2";
EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard242_v7_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="CCEBDAD06D896F0E388BBACEB27AD6A3C9107DD4585CB765DE6FFE9D0AED09C7";
S242_RECORDS:=[
rec(k:=13685,first:=1123,last:=2288,unitFirst:=1,unitLast:=1166,order:=24576,autOrder:=25165824,parity:=3,classes:=2288,raw:=56229888,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=8027),
rec(k:=13686,first:=1,last:=128,unitFirst:=1167,unitLast:=1294,order:=24576,autOrder:=393216,parity:=7,classes:=128,raw:=3145728,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1650),
rec(k:=13687,first:=1,last:=112,unitFirst:=1295,unitLast:=1406,order:=24576,autOrder:=196608,parity:=7,classes:=112,raw:=2752512,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1194),
rec(k:=13688,first:=1,last:=128,unitFirst:=1407,unitLast:=1534,order:=24576,autOrder:=393216,parity:=7,classes:=128,raw:=3145728,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1402),
rec(k:=13689,first:=1,last:=256,unitFirst:=1535,unitLast:=1790,order:=24576,autOrder:=75497472,parity:=3,classes:=256,raw:=6291456,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=4623),
rec(k:=13690,first:=1,last:=41,unitFirst:=1791,unitLast:=1831,order:=24576,autOrder:=196608,parity:=7,classes:=112,raw:=2752512,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1118)
];
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard242_v7_gpt56sol.g");
