# Exact wrapper for sealed degree-24 seed workload shard213.
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD213_SEGMENT001_UNIT1_1831_POSTVERIFY_V7_GPT56SOL.txt";
STOP_AFTER_UNIT:=fail;
INTERNAL_GUARD_MS:=1320000; START_UNIT:=1;
INITIAL_COUNTERS:=[0,0,0,0,0,0,0,0,0,0,0,0];
PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";
PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0;
PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";
CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD213_CHECKPOINT_GPT56SOL.txt";
CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD213_CHECKPOINT_TMP_GPT56SOL.txt";
EXPECTED_PROFILE_SHA256:="1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2";
EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard213_v7_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="5C9E3B862220F52FC6A808AB54F8A28031B31DB96B73978E62465F0F87238B34";
S213_RECORDS:=[
rec(k:=13523,first:=230,last:=470,unitFirst:=1,unitLast:=241,order:=24576,autOrder:=786432,parity:=7,classes:=470,raw:=11550720,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1453),
rec(k:=13524,first:=1,last:=850,unitFirst:=242,unitLast:=1091,order:=24576,autOrder:=1572864,parity:=7,classes:=850,raw:=20889600,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=2466),
rec(k:=13525,first:=1,last:=64,unitFirst:=1092,unitLast:=1155,order:=24576,autOrder:=98304,parity:=3,classes:=64,raw:=1572864,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=756),
rec(k:=13526,first:=1,last:=64,unitFirst:=1156,unitLast:=1219,order:=24576,autOrder:=393216,parity:=3,classes:=64,raw:=1572864,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1720),
rec(k:=13527,first:=1,last:=220,unitFirst:=1220,unitLast:=1439,order:=24576,autOrder:=3145728,parity:=3,classes:=220,raw:=5406720,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1343),
rec(k:=13528,first:=1,last:=64,unitFirst:=1440,unitLast:=1503,order:=24576,autOrder:=98304,parity:=3,classes:=64,raw:=1572864,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=841),
rec(k:=13529,first:=1,last:=112,unitFirst:=1504,unitLast:=1615,order:=24576,autOrder:=786432,parity:=7,classes:=112,raw:=2752512,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1624),
rec(k:=13530,first:=1,last:=40,unitFirst:=1616,unitLast:=1655,order:=24576,autOrder:=98304,parity:=3,classes:=40,raw:=983040,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=916),
rec(k:=13531,first:=1,last:=176,unitFirst:=1656,unitLast:=1831,order:=24576,autOrder:=786432,parity:=3,classes:=640,raw:=15728640,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=2291)
];
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard213_v7_gpt56sol.g");
