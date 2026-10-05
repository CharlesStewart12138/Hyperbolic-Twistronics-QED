# Exact wrapper for sealed degree-24 seed workload shard254.
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD254_SEGMENT001_UNIT1_1831_POSTVERIFY_V7_GPT56SOL.txt";
STOP_AFTER_UNIT:=fail;
INTERNAL_GUARD_MS:=1320000; START_UNIT:=1;
INITIAL_COUNTERS:=[0,0,0,0,0,0,0,0,0,0,0,0];
PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";
PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0;
PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";
CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD254_CHECKPOINT_GPT56SOL.txt";
CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD254_CHECKPOINT_TMP_GPT56SOL.txt";
EXPECTED_PROFILE_SHA256:="1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2";
EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard254_v7_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="6A673E12B5F71A7AD5A6C86486B5E1543FAC46E2D980EE4E6F8F4514D846EACA";
S254_RECORDS:=[
rec(k:=13745,first:=200,last:=428,unitFirst:=1,unitLast:=229,order:=24576,autOrder:=786432,parity:=1,classes:=428,raw:=10518528,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1314),
rec(k:=13746,first:=1,last:=356,unitFirst:=230,unitLast:=585,order:=24576,autOrder:=393216,parity:=1,classes:=356,raw:=8749056,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1195),
rec(k:=13747,first:=1,last:=476,unitFirst:=586,unitLast:=1061,order:=24576,autOrder:=786432,parity:=1,classes:=476,raw:=11698176,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1500),
rec(k:=13748,first:=1,last:=585,unitFirst:=1062,unitLast:=1646,order:=24576,autOrder:=1572864,parity:=1,classes:=585,raw:=14376960,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1475),
rec(k:=13749,first:=1,last:=185,unitFirst:=1647,unitLast:=1831,order:=24576,autOrder:=786432,parity:=1,classes:=476,raw:=11698176,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=936)
];
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard254_v7_gpt56sol.g");
