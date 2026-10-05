# Exact wrapper for sealed degree-24 seed workload shard241.
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD241_SEGMENT001_UNIT1_1831_POSTVERIFY_V7_GPT56SOL.txt";
STOP_AFTER_UNIT:=fail;
INTERNAL_GUARD_MS:=1320000; START_UNIT:=1;
INITIAL_COUNTERS:=[0,0,0,0,0,0,0,0,0,0,0,0];
PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";
PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0;
PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";
CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD241_CHECKPOINT_GPT56SOL.txt";
CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD241_CHECKPOINT_TMP_GPT56SOL.txt";
EXPECTED_PROFILE_SHA256:="1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2";
EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard241_v7_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="164B2B867D8E7106096EAC13C21A8916A02BACBC095BDE22DCCBEC3AEC8EDB96";
S241_RECORDS:=[
rec(k:=13680,first:=168,last:=348,unitFirst:=1,unitLast:=181,order:=24576,autOrder:=393216,parity:=7,classes:=348,raw:=8552448,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1267),
rec(k:=13681,first:=1,last:=112,unitFirst:=182,unitLast:=293,order:=24576,autOrder:=196608,parity:=7,classes:=112,raw:=2752512,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1055),
rec(k:=13682,first:=1,last:=128,unitFirst:=294,unitLast:=421,order:=24576,autOrder:=393216,parity:=7,classes:=128,raw:=3145728,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1473),
rec(k:=13683,first:=1,last:=96,unitFirst:=422,unitLast:=517,order:=24576,autOrder:=196608,parity:=3,classes:=96,raw:=2359296,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1355),
rec(k:=13684,first:=1,last:=192,unitFirst:=518,unitLast:=709,order:=24576,autOrder:=393216,parity:=7,classes:=192,raw:=4718592,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1018),
rec(k:=13685,first:=1,last:=1122,unitFirst:=710,unitLast:=1831,order:=24576,autOrder:=25165824,parity:=3,classes:=2288,raw:=56229888,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=8027)
];
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard241_v7_gpt56sol.g");
