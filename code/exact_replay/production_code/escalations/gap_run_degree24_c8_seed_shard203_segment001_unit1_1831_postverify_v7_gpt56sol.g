# Exact wrapper for sealed degree-24 seed workload shard203.
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD203_SEGMENT001_UNIT1_1831_POSTVERIFY_V7_GPT56SOL.txt";
STOP_AFTER_UNIT:=fail;
INTERNAL_GUARD_MS:=1320000; START_UNIT:=1;
INITIAL_COUNTERS:=[0,0,0,0,0,0,0,0,0,0,0,0];
PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";
PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0;
PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";
CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD203_CHECKPOINT_GPT56SOL.txt";
CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD203_CHECKPOINT_TMP_GPT56SOL.txt";
EXPECTED_PROFILE_SHA256:="1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2";
EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard203_v7_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="91DA0A88CB63243100DE856D3A69D11BB75CA0DEC8A42B90DD8B077CB57DC696";
S203_RECORDS:=[
rec(k:=13462,first:=64,last:=420,unitFirst:=1,unitLast:=357,order:=24576,autOrder:=786432,parity:=3,classes:=420,raw:=10321920,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1295),
rec(k:=13463,first:=1,last:=192,unitFirst:=358,unitLast:=549,order:=24576,autOrder:=1572864,parity:=7,classes:=192,raw:=4718592,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1940),
rec(k:=13464,first:=1,last:=240,unitFirst:=550,unitLast:=789,order:=24576,autOrder:=1572864,parity:=7,classes:=240,raw:=5898240,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1638),
rec(k:=13465,first:=1,last:=548,unitFirst:=790,unitLast:=1337,order:=24576,autOrder:=786432,parity:=3,classes:=548,raw:=13467648,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1830),
rec(k:=13466,first:=1,last:=320,unitFirst:=1338,unitLast:=1657,order:=24576,autOrder:=786432,parity:=3,classes:=320,raw:=7864320,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1546),
rec(k:=13467,first:=1,last:=174,unitFirst:=1658,unitLast:=1831,order:=24576,autOrder:=1572864,parity:=3,classes:=880,raw:=21626880,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=2600)
];
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard203_v7_gpt56sol.g");
