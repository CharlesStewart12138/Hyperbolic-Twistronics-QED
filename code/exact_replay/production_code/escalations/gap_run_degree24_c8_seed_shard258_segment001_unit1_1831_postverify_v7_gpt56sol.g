# Exact wrapper for sealed degree-24 seed workload shard258.
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD258_SEGMENT001_UNIT1_1831_POSTVERIFY_V7_GPT56SOL.txt";
STOP_AFTER_UNIT:=fail;
INTERNAL_GUARD_MS:=1320000; START_UNIT:=1;
INITIAL_COUNTERS:=[0,0,0,0,0,0,0,0,0,0,0,0];
PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";
PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0;
PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";
CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD258_CHECKPOINT_GPT56SOL.txt";
CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD258_CHECKPOINT_TMP_GPT56SOL.txt";
EXPECTED_PROFILE_SHA256:="1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2";
EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard258_v7_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="CA20B4917B39F7EB66C0535AF2304659C26B6F15F5459F2CF75CCD03FBDE8E33";
S258_RECORDS:=[
rec(k:=13763,first:=317,last:=880,unitFirst:=1,unitLast:=564,order:=24576,autOrder:=393216,parity:=7,classes:=880,raw:=21626880,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=2346),
rec(k:=13764,first:=1,last:=128,unitFirst:=565,unitLast:=692,order:=24576,autOrder:=393216,parity:=7,classes:=128,raw:=3145728,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1294),
rec(k:=13765,first:=1,last:=128,unitFirst:=693,unitLast:=820,order:=24576,autOrder:=393216,parity:=7,classes:=128,raw:=3145728,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1049),
rec(k:=13766,first:=1,last:=128,unitFirst:=821,unitLast:=948,order:=24576,autOrder:=393216,parity:=7,classes:=128,raw:=3145728,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1097),
rec(k:=13767,first:=1,last:=128,unitFirst:=949,unitLast:=1076,order:=24576,autOrder:=393216,parity:=7,classes:=128,raw:=3145728,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1335),
rec(k:=13768,first:=1,last:=384,unitFirst:=1077,unitLast:=1460,order:=24576,autOrder:=196608,parity:=7,classes:=384,raw:=9437184,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1297),
rec(k:=13769,first:=1,last:=371,unitFirst:=1461,unitLast:=1831,order:=24576,autOrder:=196608,parity:=7,classes:=384,raw:=9437184,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1170)
];
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard258_v7_gpt56sol.g");
