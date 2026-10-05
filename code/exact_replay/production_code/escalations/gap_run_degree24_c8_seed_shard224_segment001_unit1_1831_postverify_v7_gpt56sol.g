# Exact wrapper for sealed degree-24 seed workload shard224.
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD224_SEGMENT001_UNIT1_1831_POSTVERIFY_V7_GPT56SOL.txt";
STOP_AFTER_UNIT:=fail;
INTERNAL_GUARD_MS:=1320000; START_UNIT:=1;
INITIAL_COUNTERS:=[0,0,0,0,0,0,0,0,0,0,0,0];
PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";
PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0;
PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";
CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD224_CHECKPOINT_GPT56SOL.txt";
CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD224_CHECKPOINT_TMP_GPT56SOL.txt";
EXPECTED_PROFILE_SHA256:="1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2";
EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard224_v7_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="9BE408667821C9545C06056B80FC71291DEE6333FC38D3D8AE0BDC893BAE8FA3";
S224_RECORDS:=[
rec(k:=13585,first:=477,last:=640,unitFirst:=1,unitLast:=164,order:=24576,autOrder:=393216,parity:=3,classes:=640,raw:=15728640,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1982),
rec(k:=13586,first:=1,last:=584,unitFirst:=165,unitLast:=748,order:=24576,autOrder:=786432,parity:=3,classes:=584,raw:=14352384,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1871),
rec(k:=13587,first:=1,last:=192,unitFirst:=749,unitLast:=940,order:=24576,autOrder:=786432,parity:=7,classes:=192,raw:=4718592,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1524),
rec(k:=13588,first:=1,last:=72,unitFirst:=941,unitLast:=1012,order:=24576,autOrder:=393216,parity:=3,classes:=72,raw:=1769472,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1187),
rec(k:=13589,first:=1,last:=164,unitFirst:=1013,unitLast:=1176,order:=24576,autOrder:=786432,parity:=7,classes:=164,raw:=4030464,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1574),
rec(k:=13590,first:=1,last:=128,unitFirst:=1177,unitLast:=1304,order:=24576,autOrder:=393216,parity:=3,classes:=128,raw:=3145728,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1178),
rec(k:=13591,first:=1,last:=527,unitFirst:=1305,unitLast:=1831,order:=24576,autOrder:=1572864,parity:=7,classes:=737,raw:=18112512,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=2267)
];
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard224_v7_gpt56sol.g");
