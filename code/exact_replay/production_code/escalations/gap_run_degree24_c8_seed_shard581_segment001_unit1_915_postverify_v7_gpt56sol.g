# Exact wrapper for sealed degree-24 seed workload shard581.
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD581_SEGMENT001_UNIT1_915_POSTVERIFY_V7_GPT56SOL.txt";
STOP_AFTER_UNIT:=fail;
INTERNAL_GUARD_MS:=1320000; START_UNIT:=1;
INITIAL_COUNTERS:=[0,0,0,0,0,0,0,0,0,0,0,0];
PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";
PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0;
PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";
CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD581_CHECKPOINT_GPT56SOL.txt";
CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD581_CHECKPOINT_TMP_GPT56SOL.txt";
EXPECTED_PROFILE_SHA256:="1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2";
EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard581_v7_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="7284804D3F7B9A3A4D7CEF6D7BC6C6C3C360FC9F24759B6ED1723A1844969754";
S581_RECORDS:=[
rec(k:=15510,first:=296,last:=341,unitFirst:=1,unitLast:=46,order:=49152,autOrder:=6291456,parity:=3,classes:=341,raw:=16760832,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=2808),
rec(k:=15511,first:=1,last:=224,unitFirst:=47,unitLast:=270,order:=49152,autOrder:=1572864,parity:=3,classes:=224,raw:=11010048,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=3510),
rec(k:=15512,first:=1,last:=124,unitFirst:=271,unitLast:=394,order:=49152,autOrder:=9437184,parity:=3,classes:=124,raw:=6094848,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=3441),
rec(k:=15513,first:=1,last:=242,unitFirst:=395,unitLast:=636,order:=49152,autOrder:=9437184,parity:=3,classes:=242,raw:=11894784,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=2896),
rec(k:=15514,first:=1,last:=279,unitFirst:=637,unitLast:=915,order:=49152,autOrder:=3145728,parity:=3,classes:=334,raw:=16416768,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=3364)
];
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard581_v7_gpt56sol.g");
