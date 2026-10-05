# Exact wrapper for sealed degree-24 seed workload shard618.
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD618_SEGMENT001_UNIT1_915_POSTVERIFY_V7_GPT56SOL.txt";
STOP_AFTER_UNIT:=fail;
INTERNAL_GUARD_MS:=1320000; START_UNIT:=1;
INITIAL_COUNTERS:=[0,0,0,0,0,0,0,0,0,0,0,0];
PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";
PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0;
PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";
CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD618_CHECKPOINT_GPT56SOL.txt";
CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD618_CHECKPOINT_TMP_GPT56SOL.txt";
EXPECTED_PROFILE_SHA256:="1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2";
EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard618_v7_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="BEB1305D9E3B11E46D32DFCF35734D5A8EF5FCBD5313FBB093EFFCFF37DA6AF9";
S618_RECORDS:=[
rec(k:=15600,first:=51,last:=184,unitFirst:=1,unitLast:=134,order:=49152,autOrder:=1572864,parity:=3,classes:=184,raw:=9043968,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1909),
rec(k:=15601,first:=1,last:=152,unitFirst:=135,unitLast:=286,order:=49152,autOrder:=1572864,parity:=7,classes:=152,raw:=7471104,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1631),
rec(k:=15602,first:=1,last:=132,unitFirst:=287,unitLast:=418,order:=49152,autOrder:=1572864,parity:=3,classes:=132,raw:=6488064,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1270),
rec(k:=15603,first:=1,last:=96,unitFirst:=419,unitLast:=514,order:=49152,autOrder:=393216,parity:=3,classes:=96,raw:=4718592,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1197),
rec(k:=15604,first:=1,last:=152,unitFirst:=515,unitLast:=666,order:=49152,autOrder:=786432,parity:=3,classes:=152,raw:=7471104,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1168),
rec(k:=15605,first:=1,last:=160,unitFirst:=667,unitLast:=826,order:=49152,autOrder:=393216,parity:=7,classes:=160,raw:=7864320,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1092),
rec(k:=15606,first:=1,last:=89,unitFirst:=827,unitLast:=915,order:=49152,autOrder:=786432,parity:=7,classes:=960,raw:=47185920,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=2822)
];
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard618_v7_gpt56sol.g");
