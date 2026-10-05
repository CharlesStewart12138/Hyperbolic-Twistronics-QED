# Exact wrapper for sealed degree-24 seed workload shard489.
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD489_SEGMENT002_UNIT891_915_POSTVERIFY_V7_GPT56SOL.txt";
STOP_AFTER_UNIT:=fail;
INTERNAL_GUARD_MS:=1320000; START_UNIT:=891;
INITIAL_COUNTERS:=[890,43745280,890,56,1048448,465408,266624,84864,0,0,0,0];
PREVIOUS_CHECKPOINT_SHA256:="8f6f88eaef541d66d0401115d00748da98134fb3fc793701aaa680c59c7de62c";
PREVIOUS_OUTPUT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD489_SEGMENT001_UNIT1_915_POSTVERIFY_V7_GPT56SOL.txt"; PREVIOUS_OUTPUT_PREFIX_BYTES:=670553;
PREVIOUS_OUTPUT_PREFIX_SHA256:="206b218e21419525e2c192bd0e0353c0ce889a89fa4e80a73bef0011578165ce";
CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD489_CHECKPOINT_GPT56SOL.txt";
CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD489_CHECKPOINT_TMP_GPT56SOL.txt";
EXPECTED_PROFILE_SHA256:="1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2";
EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard489_v7_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="864C518869762BD08E4653931D7DA1BBA4215FF180FCE6E51B10EE7AA0D2BF6A";
S489_RECORDS:=[
rec(k:=15259,first:=234,last:=320,unitFirst:=1,unitLast:=87,order:=49152,autOrder:=1572864,parity:=3,classes:=320,raw:=15728640,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1441),
rec(k:=15260,first:=1,last:=320,unitFirst:=88,unitLast:=407,order:=49152,autOrder:=1572864,parity:=3,classes:=320,raw:=15728640,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1704),
rec(k:=15261,first:=1,last:=320,unitFirst:=408,unitLast:=727,order:=49152,autOrder:=1572864,parity:=3,classes:=320,raw:=15728640,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1939),
rec(k:=15262,first:=1,last:=188,unitFirst:=728,unitLast:=915,order:=49152,autOrder:=1572864,parity:=3,classes:=320,raw:=15728640,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=2569)
];
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard489_v7_gpt56sol.g");
