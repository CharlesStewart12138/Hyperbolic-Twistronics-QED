# Exact wrapper for sealed degree-24 seed workload shard178.
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD178_SEGMENT001_UNIT1_1831_POSTVERIFY_V7_GPT56SOL.txt";
STOP_AFTER_UNIT:=fail;
INTERNAL_GUARD_MS:=1320000; START_UNIT:=1;
INITIAL_COUNTERS:=[0,0,0,0,0,0,0,0,0,0,0,0];
PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";
PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0;
PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";
CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD178_CHECKPOINT_GPT56SOL.txt";
CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD178_CHECKPOINT_TMP_GPT56SOL.txt";
EXPECTED_PROFILE_SHA256:="1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2";
EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard178_v7_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="D3A5F4023922B0DBCFEFC3C5D3DD187471B75DF9A343B6A76D1B2D831808EF22";
S178_RECORDS:=[
rec(k:=13296,first:=96,last:=576,unitFirst:=1,unitLast:=481,order:=24576,autOrder:=393216,parity:=7,classes:=576,raw:=14155776,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1776),
rec(k:=13297,first:=1,last:=40,unitFirst:=482,unitLast:=521,order:=24576,autOrder:=98304,parity:=3,classes:=40,raw:=983040,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=993),
rec(k:=13298,first:=1,last:=128,unitFirst:=522,unitLast:=649,order:=24576,autOrder:=196608,parity:=15,classes:=128,raw:=3145728,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1337),
rec(k:=13299,first:=1,last:=64,unitFirst:=650,unitLast:=713,order:=24576,autOrder:=98304,parity:=3,classes:=64,raw:=1572864,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=878),
rec(k:=13300,first:=1,last:=448,unitFirst:=714,unitLast:=1161,order:=24576,autOrder:=196608,parity:=15,classes:=448,raw:=11010048,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1119),
rec(k:=13301,first:=1,last:=128,unitFirst:=1162,unitLast:=1289,order:=24576,autOrder:=196608,parity:=15,classes:=128,raw:=3145728,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1308),
rec(k:=13302,first:=1,last:=448,unitFirst:=1290,unitLast:=1737,order:=24576,autOrder:=196608,parity:=15,classes:=448,raw:=11010048,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=999),
rec(k:=13303,first:=1,last:=40,unitFirst:=1738,unitLast:=1777,order:=24576,autOrder:=98304,parity:=3,classes:=40,raw:=983040,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=729),
rec(k:=13304,first:=1,last:=54,unitFirst:=1778,unitLast:=1831,order:=24576,autOrder:=98304,parity:=3,classes:=64,raw:=1572864,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=796)
];
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard178_v7_gpt56sol.g");
