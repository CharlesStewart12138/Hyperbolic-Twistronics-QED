# Exact wrapper for sealed degree-24 seed workload shard591.
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD591_SEGMENT002_UNIT275_915_POSTVERIFY_V7_GPT56SOL.txt";
STOP_AFTER_UNIT:=fail;
INTERNAL_GUARD_MS:=1320000; START_UNIT:=275;
INITIAL_COUNTERS:=[274,13467648,274,4,718976,614784,175360,35840,0,0,0,0];
PREVIOUS_CHECKPOINT_SHA256:="cc18845510a9d73bb182617637d430697dcd133043336ec6b7c92e0b8c885578";
PREVIOUS_OUTPUT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD591_SEGMENT001_UNIT1_915_POSTVERIFY_V7_GPT56SOL.txt"; PREVIOUS_OUTPUT_PREFIX_BYTES:=205867;
PREVIOUS_OUTPUT_PREFIX_SHA256:="712133e5aac4c3defcb15eb9fee140fcf390f7b22e6de9cd9cc53d6219c73f26";
CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD591_CHECKPOINT_GPT56SOL.txt";
CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD591_CHECKPOINT_TMP_GPT56SOL.txt";
EXPECTED_PROFILE_SHA256:="1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2";
EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard591_v7_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="1D3FB5D57059B897123759756108EBC445DEEBEF72AF68372BB2AC8268F97180";
S591_RECORDS:=[
rec(k:=15547,first:=93,last:=208,unitFirst:=1,unitLast:=116,order:=49152,autOrder:=1572864,parity:=15,classes:=208,raw:=10223616,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1396),
rec(k:=15548,first:=1,last:=799,unitFirst:=117,unitLast:=915,order:=49152,autOrder:=3145728,parity:=15,classes:=1228,raw:=60358656,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=3516)
];
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard591_v7_gpt56sol.g");
