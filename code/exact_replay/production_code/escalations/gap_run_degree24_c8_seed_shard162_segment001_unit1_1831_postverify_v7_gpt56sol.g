# Exact wrapper for sealed degree-24 seed workload shard162.
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD162_SEGMENT001_UNIT1_1831_POSTVERIFY_V7_GPT56SOL.txt";
STOP_AFTER_UNIT:=fail;
INTERNAL_GUARD_MS:=1320000; START_UNIT:=1;
INITIAL_COUNTERS:=[0,0,0,0,0,0,0,0,0,0,0,0];
PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";
PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0;
PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";
CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD162_CHECKPOINT_GPT56SOL.txt";
CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD162_CHECKPOINT_TMP_GPT56SOL.txt";
EXPECTED_PROFILE_SHA256:="1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2";
EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard162_v7_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="DD0E98D5322DB9438E10B412B8E04D8210176E04BD2175C5FF29FB1AB64F582D";
S162_RECORDS:=[
rec(k:=13147,first:=419,last:=743,unitFirst:=1,unitLast:=325,order:=24576,autOrder:=3145728,parity:=7,classes:=743,raw:=18259968,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=2471),
rec(k:=13148,first:=1,last:=303,unitFirst:=326,unitLast:=628,order:=24576,autOrder:=3145728,parity:=7,classes:=303,raw:=7446528,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1094),
rec(k:=13151,first:=1,last:=420,unitFirst:=629,unitLast:=1048,order:=24576,autOrder:=786432,parity:=3,classes:=420,raw:=10321920,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=2082),
rec(k:=13152,first:=1,last:=200,unitFirst:=1049,unitLast:=1248,order:=24576,autOrder:=786432,parity:=3,classes:=200,raw:=4915200,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1617),
rec(k:=13153,first:=1,last:=525,unitFirst:=1249,unitLast:=1773,order:=24576,autOrder:=1572864,parity:=3,classes:=525,raw:=12902400,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=2267),
rec(k:=13154,first:=1,last:=58,unitFirst:=1774,unitLast:=1831,order:=24576,autOrder:=786432,parity:=3,classes:=76,raw:=1867776,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1710)
];
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard162_v7_gpt56sol.g");
