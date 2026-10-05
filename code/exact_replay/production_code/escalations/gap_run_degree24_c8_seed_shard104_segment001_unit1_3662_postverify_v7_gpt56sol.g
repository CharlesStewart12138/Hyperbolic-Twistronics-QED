# Exact wrapper for sealed degree-24 seed workload shard104.
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD104_SEGMENT001_UNIT1_3662_POSTVERIFY_V7_GPT56SOL.txt";
STOP_AFTER_UNIT:=fail;
INTERNAL_GUARD_MS:=1320000; START_UNIT:=1;
INITIAL_COUNTERS:=[0,0,0,0,0,0,0,0,0,0,0,0];
PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";
PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0;
PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";
CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD104_CHECKPOINT_GPT56SOL.txt";
CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD104_CHECKPOINT_TMP_GPT56SOL.txt";
EXPECTED_PROFILE_SHA256:="1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2";
EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard104_v7_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="3E7655FF7C5B9DA04821D86804632C5028A5DA652404373305780C9F2EE9104C";
S104_RECORDS:=[
rec(k:=11932,first:=269,last:=434,unitFirst:=1,unitLast:=166,order:=12288,autOrder:=393216,parity:=3,classes:=434,raw:=5332992,method:="pc",representation:="pc_transport",pcOrder:=12288,profileMs:=1147),
rec(k:=11933,first:=1,last:=32,unitFirst:=167,unitLast:=198,order:=12288,autOrder:=98304,parity:=7,classes:=32,raw:=393216,method:="pc",representation:="pc_transport",pcOrder:=12288,profileMs:=605),
rec(k:=11934,first:=1,last:=170,unitFirst:=199,unitLast:=368,order:=12288,autOrder:=196608,parity:=1,classes:=170,raw:=2088960,method:="pc",representation:="pc_transport",pcOrder:=12288,profileMs:=830),
rec(k:=11935,first:=1,last:=560,unitFirst:=369,unitLast:=928,order:=12288,autOrder:=786432,parity:=15,classes:=560,raw:=6881280,method:="pc",representation:="pc_transport",pcOrder:=12288,profileMs:=1435),
rec(k:=11936,first:=1,last:=42,unitFirst:=929,unitLast:=970,order:=12288,autOrder:=196608,parity:=7,classes:=42,raw:=516096,method:="pc",representation:="pc_transport",pcOrder:=12288,profileMs:=591),
rec(k:=11937,first:=1,last:=8,unitFirst:=971,unitLast:=978,order:=12288,autOrder:=49152,parity:=7,classes:=8,raw:=98304,method:="pc",representation:="pc_transport",pcOrder:=12288,profileMs:=519),
rec(k:=11938,first:=1,last:=434,unitFirst:=979,unitLast:=1412,order:=12288,autOrder:=393216,parity:=3,classes:=434,raw:=5332992,method:="pc",representation:="pc_transport",pcOrder:=12288,profileMs:=1161),
rec(k:=11939,first:=1,last:=72,unitFirst:=1413,unitLast:=1484,order:=12288,autOrder:=49152,parity:=7,classes:=72,raw:=884736,method:="pc",representation:="pc_transport",pcOrder:=12288,profileMs:=719),
rec(k:=11940,first:=1,last:=170,unitFirst:=1485,unitLast:=1654,order:=12288,autOrder:=196608,parity:=1,classes:=170,raw:=2088960,method:="pc",representation:="pc_transport",pcOrder:=12288,profileMs:=823),
rec(k:=11941,first:=1,last:=200,unitFirst:=1655,unitLast:=1854,order:=12288,autOrder:=98304,parity:=7,classes:=200,raw:=2457600,method:="pc",representation:="pc_transport",pcOrder:=12288,profileMs:=830),
rec(k:=11942,first:=1,last:=297,unitFirst:=1855,unitLast:=2151,order:=12288,autOrder:=393216,parity:=3,classes:=297,raw:=3649536,method:="pc",representation:="pc_transport",pcOrder:=12288,profileMs:=901),
rec(k:=11943,first:=1,last:=280,unitFirst:=2152,unitLast:=2431,order:=12288,autOrder:=98304,parity:=7,classes:=280,raw:=3440640,method:="pc",representation:="pc_transport",pcOrder:=12288,profileMs:=859),
rec(k:=11944,first:=1,last:=160,unitFirst:=2432,unitLast:=2591,order:=12288,autOrder:=49152,parity:=7,classes:=160,raw:=1966080,method:="pc",representation:="pc_transport",pcOrder:=12288,profileMs:=736),
rec(k:=11945,first:=1,last:=434,unitFirst:=2592,unitLast:=3025,order:=12288,autOrder:=393216,parity:=3,classes:=434,raw:=5332992,method:="pc",representation:="pc_transport",pcOrder:=12288,profileMs:=1063),
rec(k:=11946,first:=1,last:=196,unitFirst:=3026,unitLast:=3221,order:=12288,autOrder:=98304,parity:=3,classes:=196,raw:=2408448,method:="pc",representation:="pc_transport",pcOrder:=12288,profileMs:=858),
rec(k:=11947,first:=1,last:=220,unitFirst:=3222,unitLast:=3441,order:=12288,autOrder:=98304,parity:=3,classes:=220,raw:=2703360,method:="pc",representation:="pc_transport",pcOrder:=12288,profileMs:=897),
rec(k:=11948,first:=1,last:=196,unitFirst:=3442,unitLast:=3637,order:=12288,autOrder:=98304,parity:=3,classes:=196,raw:=2408448,method:="pc",representation:="pc_transport",pcOrder:=12288,profileMs:=891),
rec(k:=11949,first:=1,last:=25,unitFirst:=3638,unitLast:=3662,order:=12288,autOrder:=98304,parity:=3,classes:=220,raw:=2703360,method:="pc",representation:="pc_transport",pcOrder:=12288,profileMs:=815)
];
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard104_v7_gpt56sol.g");
