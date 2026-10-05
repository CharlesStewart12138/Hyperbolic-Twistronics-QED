# Exact wrapper for sealed degree-24 seed workload shard628.
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD628_SEGMENT001_UNIT1_915_POSTVERIFY_V7_GPT56SOL.txt";
STOP_AFTER_UNIT:=fail;
INTERNAL_GUARD_MS:=1320000; START_UNIT:=1;
INITIAL_COUNTERS:=[0,0,0,0,0,0,0,0,0,0,0,0];
PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";
PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0;
PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";
CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD628_CHECKPOINT_GPT56SOL.txt";
CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD628_CHECKPOINT_TMP_GPT56SOL.txt";
EXPECTED_PROFILE_SHA256:="1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2";
EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard628_v7_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="A64AB425374CC9F411FE84DA0E24CC99C4BCE549D4392D550BD802AFB0A76FFF";
S628_RECORDS:=[
rec(k:=15630,first:=581,last:=960,unitFirst:=1,unitLast:=380,order:=49152,autOrder:=786432,parity:=7,classes:=960,raw:=47185920,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1965),
rec(k:=15631,first:=1,last:=96,unitFirst:=381,unitLast:=476,order:=49152,autOrder:=393216,parity:=3,classes:=96,raw:=4718592,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1579),
rec(k:=15632,first:=1,last:=160,unitFirst:=477,unitLast:=636,order:=49152,autOrder:=393216,parity:=7,classes:=160,raw:=7864320,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1945),
rec(k:=15633,first:=1,last:=208,unitFirst:=637,unitLast:=844,order:=49152,autOrder:=393216,parity:=3,classes:=208,raw:=10223616,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1360),
rec(k:=15634,first:=1,last:=71,unitFirst:=845,unitLast:=915,order:=49152,autOrder:=786432,parity:=7,classes:=960,raw:=47185920,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=2890)
];
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard628_v7_gpt56sol.g");
