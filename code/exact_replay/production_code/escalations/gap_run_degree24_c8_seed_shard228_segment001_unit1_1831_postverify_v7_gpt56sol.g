# Exact wrapper for sealed degree-24 seed workload shard228.
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD228_SEGMENT001_UNIT1_1831_POSTVERIFY_V7_GPT56SOL.txt";
STOP_AFTER_UNIT:=fail;
INTERNAL_GUARD_MS:=1320000; START_UNIT:=1;
INITIAL_COUNTERS:=[0,0,0,0,0,0,0,0,0,0,0,0];
PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";
PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0;
PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";
CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD228_CHECKPOINT_GPT56SOL.txt";
CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD228_CHECKPOINT_TMP_GPT56SOL.txt";
EXPECTED_PROFILE_SHA256:="1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2";
EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard228_v7_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="B4CB963C9A469BE6361B05AF83D3FB383837B9416DF5A794F8285256B9C37E0D";
S228_RECORDS:=[
rec(k:=13613,first:=159,last:=160,unitFirst:=1,unitLast:=2,order:=24576,autOrder:=393216,parity:=7,classes:=160,raw:=3932160,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=909),
rec(k:=13614,first:=1,last:=160,unitFirst:=3,unitLast:=162,order:=24576,autOrder:=393216,parity:=7,classes:=160,raw:=3932160,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=937),
rec(k:=13615,first:=1,last:=160,unitFirst:=163,unitLast:=322,order:=24576,autOrder:=393216,parity:=7,classes:=160,raw:=3932160,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1498),
rec(k:=13616,first:=1,last:=160,unitFirst:=323,unitLast:=482,order:=24576,autOrder:=393216,parity:=15,classes:=160,raw:=3932160,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=847),
rec(k:=13617,first:=1,last:=160,unitFirst:=483,unitLast:=642,order:=24576,autOrder:=393216,parity:=7,classes:=160,raw:=3932160,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=849),
rec(k:=13618,first:=1,last:=192,unitFirst:=643,unitLast:=834,order:=24576,autOrder:=393216,parity:=7,classes:=192,raw:=4718592,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1371),
rec(k:=13619,first:=1,last:=192,unitFirst:=835,unitLast:=1026,order:=24576,autOrder:=393216,parity:=7,classes:=192,raw:=4718592,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1317),
rec(k:=13620,first:=1,last:=192,unitFirst:=1027,unitLast:=1218,order:=24576,autOrder:=393216,parity:=7,classes:=192,raw:=4718592,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1137),
rec(k:=13621,first:=1,last:=192,unitFirst:=1219,unitLast:=1410,order:=24576,autOrder:=393216,parity:=7,classes:=192,raw:=4718592,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1657),
rec(k:=13622,first:=1,last:=192,unitFirst:=1411,unitLast:=1602,order:=24576,autOrder:=393216,parity:=7,classes:=192,raw:=4718592,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1217),
rec(k:=13623,first:=1,last:=192,unitFirst:=1603,unitLast:=1794,order:=24576,autOrder:=393216,parity:=7,classes:=192,raw:=4718592,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1028),
rec(k:=13624,first:=1,last:=37,unitFirst:=1795,unitLast:=1831,order:=24576,autOrder:=393216,parity:=7,classes:=160,raw:=3932160,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=946)
];
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard228_v7_gpt56sol.g");
