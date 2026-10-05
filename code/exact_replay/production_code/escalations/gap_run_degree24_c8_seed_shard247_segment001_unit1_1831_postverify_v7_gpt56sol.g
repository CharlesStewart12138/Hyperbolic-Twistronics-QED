# Exact wrapper for sealed degree-24 seed workload shard247.
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD247_SEGMENT001_UNIT1_1831_POSTVERIFY_V7_GPT56SOL.txt";
STOP_AFTER_UNIT:=fail;
INTERNAL_GUARD_MS:=1320000; START_UNIT:=1;
INITIAL_COUNTERS:=[0,0,0,0,0,0,0,0,0,0,0,0];
PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";
PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0;
PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";
CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD247_CHECKPOINT_GPT56SOL.txt";
CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD247_CHECKPOINT_TMP_GPT56SOL.txt";
EXPECTED_PROFILE_SHA256:="1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2";
EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard247_v7_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="BB055B7185A47EFB0CDD7D20049D51AAF4A0C31A24555CCA7CA9106E58D04DEE";
S247_RECORDS:=[
rec(k:=13717,first:=534,last:=560,unitFirst:=1,unitLast:=27,order:=24576,autOrder:=393216,parity:=15,classes:=560,raw:=13762560,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1907),
rec(k:=13718,first:=1,last:=448,unitFirst:=28,unitLast:=475,order:=24576,autOrder:=393216,parity:=15,classes:=448,raw:=11010048,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1477),
rec(k:=13719,first:=1,last:=560,unitFirst:=476,unitLast:=1035,order:=24576,autOrder:=393216,parity:=15,classes:=560,raw:=13762560,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1104),
rec(k:=13720,first:=1,last:=448,unitFirst:=1036,unitLast:=1483,order:=24576,autOrder:=393216,parity:=15,classes:=448,raw:=11010048,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1498),
rec(k:=13721,first:=1,last:=348,unitFirst:=1484,unitLast:=1831,order:=24576,autOrder:=393216,parity:=15,classes:=560,raw:=13762560,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1525)
];
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard247_v7_gpt56sol.g");
