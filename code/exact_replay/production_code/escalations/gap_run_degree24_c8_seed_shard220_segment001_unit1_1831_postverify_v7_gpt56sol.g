# Exact wrapper for sealed degree-24 seed workload shard220.
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD220_SEGMENT001_UNIT1_1831_POSTVERIFY_V7_GPT56SOL.txt";
STOP_AFTER_UNIT:=fail;
INTERNAL_GUARD_MS:=1320000; START_UNIT:=1;
INITIAL_COUNTERS:=[0,0,0,0,0,0,0,0,0,0,0,0];
PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";
PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0;
PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";
CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD220_CHECKPOINT_GPT56SOL.txt";
CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD220_CHECKPOINT_TMP_GPT56SOL.txt";
EXPECTED_PROFILE_SHA256:="1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2";
EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard220_v7_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="8284BE5B0F1109A124B99E6E948EFB04478935437CBA6614C873DA6558EF2A8F";
S220_RECORDS:=[
rec(k:=13563,first:=379,last:=420,unitFirst:=1,unitLast:=42,order:=24576,autOrder:=393216,parity:=3,classes:=420,raw:=10321920,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1365),
rec(k:=13564,first:=1,last:=416,unitFirst:=43,unitLast:=458,order:=24576,autOrder:=393216,parity:=3,classes:=416,raw:=10223616,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1028),
rec(k:=13565,first:=1,last:=600,unitFirst:=459,unitLast:=1058,order:=24576,autOrder:=786432,parity:=7,classes:=600,raw:=14745600,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1775),
rec(k:=13566,first:=1,last:=480,unitFirst:=1059,unitLast:=1538,order:=24576,autOrder:=393216,parity:=3,classes:=480,raw:=11796480,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=2017),
rec(k:=13567,first:=1,last:=88,unitFirst:=1539,unitLast:=1626,order:=24576,autOrder:=393216,parity:=3,classes:=88,raw:=2162688,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1355),
rec(k:=13568,first:=1,last:=120,unitFirst:=1627,unitLast:=1746,order:=24576,autOrder:=786432,parity:=7,classes:=120,raw:=2949120,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1810),
rec(k:=13569,first:=1,last:=85,unitFirst:=1747,unitLast:=1831,order:=24576,autOrder:=393216,parity:=3,classes:=432,raw:=10616832,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1414)
];
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard220_v7_gpt56sol.g");
