# Exact wrapper for sealed degree-24 seed workload shard238.
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD238_SEGMENT001_UNIT1_1831_POSTVERIFY_V7_GPT56SOL.txt";
STOP_AFTER_UNIT:=fail;
INTERNAL_GUARD_MS:=1320000; START_UNIT:=1;
INITIAL_COUNTERS:=[0,0,0,0,0,0,0,0,0,0,0,0];
PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";
PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0;
PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";
CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD238_CHECKPOINT_GPT56SOL.txt";
CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD238_CHECKPOINT_TMP_GPT56SOL.txt";
EXPECTED_PROFILE_SHA256:="1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2";
EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard238_v7_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="5AD1E9FFB0C97D1553D6B949FFD6F1BFB23B805B597B2903A2F483A690232A41";
S238_RECORDS:=[
rec(k:=13665,first:=348,last:=348,unitFirst:=1,unitLast:=1,order:=24576,autOrder:=786432,parity:=3,classes:=348,raw:=8552448,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1348),
rec(k:=13666,first:=1,last:=728,unitFirst:=2,unitLast:=729,order:=24576,autOrder:=4718592,parity:=3,classes:=728,raw:=17891328,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=2001),
rec(k:=13667,first:=1,last:=96,unitFirst:=730,unitLast:=825,order:=24576,autOrder:=196608,parity:=3,classes:=96,raw:=2359296,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1044),
rec(k:=13668,first:=1,last:=242,unitFirst:=826,unitLast:=1067,order:=24576,autOrder:=393216,parity:=3,classes:=242,raw:=5947392,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1323),
rec(k:=13669,first:=1,last:=112,unitFirst:=1068,unitLast:=1179,order:=24576,autOrder:=196608,parity:=7,classes:=112,raw:=2752512,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=946),
rec(k:=13670,first:=1,last:=348,unitFirst:=1180,unitLast:=1527,order:=24576,autOrder:=393216,parity:=7,classes:=348,raw:=8552448,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1398),
rec(k:=13671,first:=1,last:=304,unitFirst:=1528,unitLast:=1831,order:=24576,autOrder:=3145728,parity:=3,classes:=560,raw:=13762560,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1566)
];
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard238_v7_gpt56sol.g");
