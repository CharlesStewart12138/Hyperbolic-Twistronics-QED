# Exact wrapper for sealed degree-24 seed workload shard707.
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD707_SEGMENT001_UNIT1_915_POSTVERIFY_V7_GPT56SOL.txt";
STOP_AFTER_UNIT:=fail;
INTERNAL_GUARD_MS:=1320000; START_UNIT:=1;
INITIAL_COUNTERS:=[0,0,0,0,0,0,0,0,0,0,0,0];
PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";
PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0;
PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";
CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD707_CHECKPOINT_GPT56SOL.txt";
CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD707_CHECKPOINT_TMP_GPT56SOL.txt";
EXPECTED_PROFILE_SHA256:="1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2";
EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard707_v7_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="9AACB6C1AF08683011C60D2EA03BE1AE490F584F51B45870E255D45AC25FB133";
S707_RECORDS:=[
rec(k:=15745,first:=206,last:=606,unitFirst:=1,unitLast:=401,order:=49152,autOrder:=6291456,parity:=1,classes:=606,raw:=29786112,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1810),
rec(k:=15746,first:=1,last:=76,unitFirst:=402,unitLast:=477,order:=49152,autOrder:=1572864,parity:=1,classes:=76,raw:=3735552,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1724),
rec(k:=15747,first:=1,last:=438,unitFirst:=478,unitLast:=915,order:=49152,autOrder:=3145728,parity:=1,classes:=1064,raw:=52297728,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1905)
];
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard707_v7_gpt56sol.g");
