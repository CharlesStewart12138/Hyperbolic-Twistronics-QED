# Exact wrapper for sealed degree-24 seed workload shard219.
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD219_SEGMENT001_UNIT1_1831_POSTVERIFY_V7_GPT56SOL.txt";
STOP_AFTER_UNIT:=fail;
INTERNAL_GUARD_MS:=1320000; START_UNIT:=1;
INITIAL_COUNTERS:=[0,0,0,0,0,0,0,0,0,0,0,0];
PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";
PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0;
PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";
CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD219_CHECKPOINT_GPT56SOL.txt";
CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD219_CHECKPOINT_TMP_GPT56SOL.txt";
EXPECTED_PROFILE_SHA256:="1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2";
EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard219_v7_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="4FE390E5600172848F40AD6EF02A4038A227671D0C76E1631973B18C0C6D7FF3";
S219_RECORDS:=[
rec(k:=13558,first:=70,last:=520,unitFirst:=1,unitLast:=451,order:=24576,autOrder:=786432,parity:=7,classes:=520,raw:=12779520,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1323),
rec(k:=13559,first:=1,last:=640,unitFirst:=452,unitLast:=1091,order:=24576,autOrder:=786432,parity:=7,classes:=640,raw:=15728640,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1233),
rec(k:=13560,first:=1,last:=154,unitFirst:=1092,unitLast:=1245,order:=24576,autOrder:=786432,parity:=3,classes:=154,raw:=3784704,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=845),
rec(k:=13561,first:=1,last:=88,unitFirst:=1246,unitLast:=1333,order:=24576,autOrder:=393216,parity:=3,classes:=88,raw:=2162688,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=973),
rec(k:=13562,first:=1,last:=120,unitFirst:=1334,unitLast:=1453,order:=24576,autOrder:=786432,parity:=7,classes:=120,raw:=2949120,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1296),
rec(k:=13563,first:=1,last:=378,unitFirst:=1454,unitLast:=1831,order:=24576,autOrder:=393216,parity:=3,classes:=420,raw:=10321920,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1365)
];
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard219_v7_gpt56sol.g");
