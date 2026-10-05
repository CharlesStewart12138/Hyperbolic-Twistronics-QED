# Exact wrapper for sealed degree-24 seed workload shard471.
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD471_SEGMENT002_UNIT153_915_POSTVERIFY_V7_GPT56SOL.txt";
STOP_AFTER_UNIT:=fail;
INTERNAL_GUARD_MS:=1320000; START_UNIT:=153;
INITIAL_COUNTERS:=[152,7471104,152,20,377216,110976,9984,9984,0,0,0,0];
PREVIOUS_CHECKPOINT_SHA256:="820a38471cf010bf996eac7820958269080e4d595dd42a9d9f978e20fcf7e3cf";
PREVIOUS_OUTPUT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD471_SEGMENT001_UNIT1_915_POSTVERIFY_V7_GPT56SOL.txt"; PREVIOUS_OUTPUT_PREFIX_BYTES:=114098;
PREVIOUS_OUTPUT_PREFIX_SHA256:="01c37cf50e0299e3cc755bd9d08777ae753fd1aab1a6ca9dd287609e53b4ea91";
CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD471_CHECKPOINT_GPT56SOL.txt";
CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD471_CHECKPOINT_TMP_GPT56SOL.txt";
EXPECTED_PROFILE_SHA256:="1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2";
EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard471_v7_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="C1C2E364AC01F6D6414274E930AC6FDB6F9C202F36C7F3AA5234FB7E61200472";
S471_RECORDS:=[
rec(k:=15214,first:=299,last:=368,unitFirst:=1,unitLast:=70,order:=49152,autOrder:=6291456,parity:=3,classes:=368,raw:=18087936,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=3183),
rec(k:=15215,first:=1,last:=208,unitFirst:=71,unitLast:=278,order:=49152,autOrder:=6291456,parity:=3,classes:=208,raw:=10223616,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=2594),
rec(k:=15216,first:=1,last:=199,unitFirst:=279,unitLast:=477,order:=49152,autOrder:=37748736,parity:=7,classes:=199,raw:=9781248,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=2636),
rec(k:=15217,first:=1,last:=320,unitFirst:=478,unitLast:=797,order:=49152,autOrder:=1572864,parity:=3,classes:=320,raw:=15728640,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=2231),
rec(k:=15218,first:=1,last:=118,unitFirst:=798,unitLast:=915,order:=49152,autOrder:=1572864,parity:=3,classes:=320,raw:=15728640,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1371)
];
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard471_v7_gpt56sol.g");
