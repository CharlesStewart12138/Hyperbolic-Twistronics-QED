# Exact wrapper for sealed degree-24 seed workload shard193.
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD193_SEGMENT001_UNIT1_1831_POSTVERIFY_V7_GPT56SOL.txt";
STOP_AFTER_UNIT:=fail;
INTERNAL_GUARD_MS:=1320000; START_UNIT:=1;
INITIAL_COUNTERS:=[0,0,0,0,0,0,0,0,0,0,0,0];
PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";
PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0;
PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";
CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD193_CHECKPOINT_GPT56SOL.txt";
CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD193_CHECKPOINT_TMP_GPT56SOL.txt";
EXPECTED_PROFILE_SHA256:="1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2";
EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard193_v7_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="8AB1F80C349DCA78007D92F8189A99AA1464E1521B2097B94C5440EAC59310B4";
S193_RECORDS:=[
rec(k:=13412,first:=585,last:=840,unitFirst:=1,unitLast:=256,order:=24576,autOrder:=786432,parity:=15,classes:=840,raw:=20643840,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=2028),
rec(k:=13413,first:=1,last:=448,unitFirst:=257,unitLast:=704,order:=24576,autOrder:=196608,parity:=15,classes:=448,raw:=11010048,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=949),
rec(k:=13414,first:=1,last:=448,unitFirst:=705,unitLast:=1152,order:=24576,autOrder:=393216,parity:=15,classes:=448,raw:=11010048,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1022),
rec(k:=13415,first:=1,last:=128,unitFirst:=1153,unitLast:=1280,order:=24576,autOrder:=786432,parity:=15,classes:=128,raw:=3145728,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1474),
rec(k:=13416,first:=1,last:=236,unitFirst:=1281,unitLast:=1516,order:=24576,autOrder:=3145728,parity:=15,classes:=236,raw:=5799936,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1852),
rec(k:=13417,first:=1,last:=315,unitFirst:=1517,unitLast:=1831,order:=24576,autOrder:=196608,parity:=15,classes:=448,raw:=11010048,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=869)
];
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard193_v7_gpt56sol.g");
