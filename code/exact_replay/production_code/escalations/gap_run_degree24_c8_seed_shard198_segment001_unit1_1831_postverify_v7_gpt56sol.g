# Exact wrapper for sealed degree-24 seed workload shard198.
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD198_SEGMENT001_UNIT1_1831_POSTVERIFY_V7_GPT56SOL.txt";
STOP_AFTER_UNIT:=fail;
INTERNAL_GUARD_MS:=1320000; START_UNIT:=1;
INITIAL_COUNTERS:=[0,0,0,0,0,0,0,0,0,0,0,0];
PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";
PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0;
PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";
CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD198_CHECKPOINT_GPT56SOL.txt";
CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD198_CHECKPOINT_TMP_GPT56SOL.txt";
EXPECTED_PROFILE_SHA256:="1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2";
EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard198_v7_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="1E0EFA8BBB49A2DCA0DEBB768A3DC86221F733C571FC8AE91CDBFF4FFB9D5D44";
S198_RECORDS:=[
rec(k:=13435,first:=396,last:=512,unitFirst:=1,unitLast:=117,order:=24576,autOrder:=393216,parity:=7,classes:=512,raw:=12582912,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1861),
rec(k:=13436,first:=1,last:=468,unitFirst:=118,unitLast:=585,order:=24576,autOrder:=786432,parity:=7,classes:=468,raw:=11501568,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1121),
rec(k:=13437,first:=1,last:=778,unitFirst:=586,unitLast:=1363,order:=24576,autOrder:=1572864,parity:=15,classes:=778,raw:=19120128,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1763),
rec(k:=13438,first:=1,last:=128,unitFirst:=1364,unitLast:=1491,order:=24576,autOrder:=393216,parity:=7,classes:=128,raw:=3145728,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1792),
rec(k:=13439,first:=1,last:=128,unitFirst:=1492,unitLast:=1619,order:=24576,autOrder:=393216,parity:=7,classes:=128,raw:=3145728,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1309),
rec(k:=13440,first:=1,last:=128,unitFirst:=1620,unitLast:=1747,order:=24576,autOrder:=393216,parity:=7,classes:=128,raw:=3145728,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1802),
rec(k:=13441,first:=1,last:=84,unitFirst:=1748,unitLast:=1831,order:=24576,autOrder:=393216,parity:=7,classes:=128,raw:=3145728,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1123)
];
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard198_v7_gpt56sol.g");
