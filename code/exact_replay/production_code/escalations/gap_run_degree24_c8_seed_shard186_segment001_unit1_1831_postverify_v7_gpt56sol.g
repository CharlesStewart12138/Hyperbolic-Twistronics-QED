# Exact wrapper for sealed degree-24 seed workload shard186.
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD186_SEGMENT001_UNIT1_1831_POSTVERIFY_V7_GPT56SOL.txt";
STOP_AFTER_UNIT:=fail;
INTERNAL_GUARD_MS:=1320000; START_UNIT:=1;
INITIAL_COUNTERS:=[0,0,0,0,0,0,0,0,0,0,0,0];
PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";
PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0;
PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";
CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD186_CHECKPOINT_GPT56SOL.txt";
CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD186_CHECKPOINT_TMP_GPT56SOL.txt";
EXPECTED_PROFILE_SHA256:="1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2";
EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard186_v7_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="1DB0937AA98CAA778289CE8214368D67F38918AA86D0E0A2F3E49BCB305DCEBF";
S186_RECORDS:=[
rec(k:=13375,first:=243,last:=420,unitFirst:=1,unitLast:=178,order:=24576,autOrder:=4718592,parity:=3,classes:=420,raw:=10321920,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=2641),
rec(k:=13376,first:=1,last:=98,unitFirst:=179,unitLast:=276,order:=24576,autOrder:=4718592,parity:=3,classes:=98,raw:=2408448,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1012),
rec(k:=13377,first:=1,last:=644,unitFirst:=277,unitLast:=920,order:=24576,autOrder:=786432,parity:=15,classes:=644,raw:=15826944,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1756),
rec(k:=13378,first:=1,last:=144,unitFirst:=921,unitLast:=1064,order:=24576,autOrder:=393216,parity:=15,classes:=144,raw:=3538944,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=985),
rec(k:=13379,first:=1,last:=212,unitFirst:=1065,unitLast:=1276,order:=24576,autOrder:=786432,parity:=15,classes:=212,raw:=5210112,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=808),
rec(k:=13380,first:=1,last:=555,unitFirst:=1277,unitLast:=1831,order:=24576,autOrder:=393216,parity:=15,classes:=640,raw:=15728640,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1415)
];
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard186_v7_gpt56sol.g");
