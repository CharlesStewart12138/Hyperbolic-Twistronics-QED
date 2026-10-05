# Exact wrapper for sealed degree-24 seed workload shard158.
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD158_SEGMENT001_UNIT1_1831_POSTVERIFY_V7_GPT56SOL.txt";
STOP_AFTER_UNIT:=fail;
INTERNAL_GUARD_MS:=1320000; START_UNIT:=1;
INITIAL_COUNTERS:=[0,0,0,0,0,0,0,0,0,0,0,0];
PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";
PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0;
PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";
CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD158_CHECKPOINT_GPT56SOL.txt";
CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD158_CHECKPOINT_TMP_GPT56SOL.txt";
EXPECTED_PROFILE_SHA256:="1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2";
EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard158_v7_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="B93F7EF21783186D6C79F298982CDF9A89CC2980B9C10F87834F5DE40B04C609";
S158_RECORDS:=[
rec(k:=13122,first:=54,last:=206,unitFirst:=1,unitLast:=153,order:=24576,autOrder:=3145728,parity:=3,classes:=206,raw:=5062656,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1955),
rec(k:=13123,first:=1,last:=48,unitFirst:=154,unitLast:=201,order:=24576,autOrder:=786432,parity:=3,classes:=48,raw:=1179648,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1519),
rec(k:=13124,first:=1,last:=294,unitFirst:=202,unitLast:=495,order:=24576,autOrder:=6291456,parity:=3,classes:=294,raw:=7225344,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1518),
rec(k:=13125,first:=1,last:=48,unitFirst:=496,unitLast:=543,order:=24576,autOrder:=786432,parity:=3,classes:=48,raw:=1179648,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1673),
rec(k:=13126,first:=1,last:=261,unitFirst:=544,unitLast:=804,order:=24576,autOrder:=6291456,parity:=3,classes:=261,raw:=6414336,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1473),
rec(k:=13127,first:=1,last:=192,unitFirst:=805,unitLast:=996,order:=24576,autOrder:=1572864,parity:=7,classes:=192,raw:=4718592,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1487),
rec(k:=13128,first:=1,last:=344,unitFirst:=997,unitLast:=1340,order:=24576,autOrder:=3145728,parity:=7,classes:=344,raw:=8454144,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1762),
rec(k:=13129,first:=1,last:=240,unitFirst:=1341,unitLast:=1580,order:=24576,autOrder:=1572864,parity:=7,classes:=240,raw:=5898240,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=2217),
rec(k:=13130,first:=1,last:=251,unitFirst:=1581,unitLast:=1831,order:=24576,autOrder:=3145728,parity:=7,classes:=972,raw:=23887872,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=3465)
];
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard158_v7_gpt56sol.g");
