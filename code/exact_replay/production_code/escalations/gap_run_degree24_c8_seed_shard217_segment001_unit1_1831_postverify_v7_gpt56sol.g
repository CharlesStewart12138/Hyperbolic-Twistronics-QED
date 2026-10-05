# Exact wrapper for sealed degree-24 seed workload shard217.
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD217_SEGMENT001_UNIT1_1831_POSTVERIFY_V7_GPT56SOL.txt";
STOP_AFTER_UNIT:=fail;
INTERNAL_GUARD_MS:=1320000; START_UNIT:=1;
INITIAL_COUNTERS:=[0,0,0,0,0,0,0,0,0,0,0,0];
PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";
PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0;
PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";
CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD217_CHECKPOINT_GPT56SOL.txt";
CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD217_CHECKPOINT_TMP_GPT56SOL.txt";
EXPECTED_PROFILE_SHA256:="1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2";
EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard217_v7_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="429F2ECDC388D395E36059B2C26649751BD8E38F00C23562A50EC61DD4F722B6";
S217_RECORDS:=[
rec(k:=13547,first:=100,last:=226,unitFirst:=1,unitLast:=127,order:=24576,autOrder:=1572864,parity:=7,classes:=226,raw:=5554176,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1539),
rec(k:=13548,first:=1,last:=640,unitFirst:=128,unitLast:=767,order:=24576,autOrder:=786432,parity:=7,classes:=640,raw:=15728640,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1438),
rec(k:=13549,first:=1,last:=420,unitFirst:=768,unitLast:=1187,order:=24576,autOrder:=393216,parity:=3,classes:=420,raw:=10321920,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1323),
rec(k:=13550,first:=1,last:=88,unitFirst:=1188,unitLast:=1275,order:=24576,autOrder:=393216,parity:=3,classes:=88,raw:=2162688,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1083),
rec(k:=13551,first:=1,last:=420,unitFirst:=1276,unitLast:=1695,order:=24576,autOrder:=393216,parity:=7,classes:=420,raw:=10321920,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1245),
rec(k:=13552,first:=1,last:=136,unitFirst:=1696,unitLast:=1831,order:=24576,autOrder:=393216,parity:=7,classes:=512,raw:=12582912,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1702)
];
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard217_v7_gpt56sol.g");
