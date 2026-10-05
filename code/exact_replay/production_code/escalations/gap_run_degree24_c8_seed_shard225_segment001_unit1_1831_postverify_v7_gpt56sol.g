# Exact wrapper for sealed degree-24 seed workload shard225.
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD225_SEGMENT001_UNIT1_1831_POSTVERIFY_V7_GPT56SOL.txt";
STOP_AFTER_UNIT:=fail;
INTERNAL_GUARD_MS:=1320000; START_UNIT:=1;
INITIAL_COUNTERS:=[0,0,0,0,0,0,0,0,0,0,0,0];
PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";
PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0;
PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";
CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD225_CHECKPOINT_GPT56SOL.txt";
CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD225_CHECKPOINT_TMP_GPT56SOL.txt";
EXPECTED_PROFILE_SHA256:="1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2";
EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard225_v7_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="C2A9B4E63EA7C8191034516641C38D9E7949695C5D44092B702E57E016589713";
S225_RECORDS:=[
rec(k:=13591,first:=528,last:=737,unitFirst:=1,unitLast:=210,order:=24576,autOrder:=1572864,parity:=7,classes:=737,raw:=18112512,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=2267),
rec(k:=13592,first:=1,last:=128,unitFirst:=211,unitLast:=338,order:=24576,autOrder:=393216,parity:=3,classes:=128,raw:=3145728,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1484),
rec(k:=13593,first:=1,last:=120,unitFirst:=339,unitLast:=458,order:=24576,autOrder:=786432,parity:=7,classes:=120,raw:=2949120,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1333),
rec(k:=13594,first:=1,last:=180,unitFirst:=459,unitLast:=638,order:=24576,autOrder:=786432,parity:=7,classes:=180,raw:=4423680,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=2153),
rec(k:=13595,first:=1,last:=120,unitFirst:=639,unitLast:=758,order:=24576,autOrder:=786432,parity:=7,classes:=120,raw:=2949120,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1372),
rec(k:=13596,first:=1,last:=168,unitFirst:=759,unitLast:=926,order:=24576,autOrder:=786432,parity:=7,classes:=168,raw:=4128768,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1098),
rec(k:=13597,first:=1,last:=124,unitFirst:=927,unitLast:=1050,order:=24576,autOrder:=393216,parity:=3,classes:=124,raw:=3047424,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1599),
rec(k:=13598,first:=1,last:=98,unitFirst:=1051,unitLast:=1148,order:=24576,autOrder:=4718592,parity:=3,classes:=98,raw:=2408448,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1118),
rec(k:=13599,first:=1,last:=160,unitFirst:=1149,unitLast:=1308,order:=24576,autOrder:=393216,parity:=3,classes:=160,raw:=3932160,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=891),
rec(k:=13600,first:=1,last:=88,unitFirst:=1309,unitLast:=1396,order:=24576,autOrder:=393216,parity:=3,classes:=88,raw:=2162688,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=959),
rec(k:=13601,first:=1,last:=140,unitFirst:=1397,unitLast:=1536,order:=24576,autOrder:=393216,parity:=7,classes:=140,raw:=3440640,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1726),
rec(k:=13602,first:=1,last:=295,unitFirst:=1537,unitLast:=1831,order:=24576,autOrder:=393216,parity:=7,classes:=640,raw:=15728640,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1409)
];
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard225_v7_gpt56sol.g");
