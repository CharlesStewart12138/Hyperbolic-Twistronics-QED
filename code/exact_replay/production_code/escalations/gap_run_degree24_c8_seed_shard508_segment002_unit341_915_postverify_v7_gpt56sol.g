# Exact wrapper for sealed degree-24 seed workload shard508.
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD508_SEGMENT002_UNIT341_915_POSTVERIFY_V7_GPT56SOL.txt";
STOP_AFTER_UNIT:=fail;
INTERNAL_GUARD_MS:=1320000; START_UNIT:=341;
INITIAL_COUNTERS:=[340,16711680,340,20,231424,79104,29952,29952,0,0,0,0];
PREVIOUS_CHECKPOINT_SHA256:="cc1887e131e252ed441f58f8516478e581ecedf343bbe90f4f39b3ec40855a5a";
PREVIOUS_OUTPUT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD508_SEGMENT001_UNIT1_915_POSTVERIFY_V7_GPT56SOL.txt"; PREVIOUS_OUTPUT_PREFIX_BYTES:=253986;
PREVIOUS_OUTPUT_PREFIX_SHA256:="2ab4efe7e714f384171f4e9f46effcf4e4b13845e3a3ff6bb49d9754f057a2d6";
CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD508_CHECKPOINT_GPT56SOL.txt";
CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD508_CHECKPOINT_TMP_GPT56SOL.txt";
EXPECTED_PROFILE_SHA256:="1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2";
EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard508_v7_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="5B6CEC046A5005D0F6983A024B0C00947C51B5C802DCE778916FEC1AD5D8C621";
S508_RECORDS:=[
rec(k:=15309,first:=258,last:=288,unitFirst:=1,unitLast:=31,order:=49152,autOrder:=1572864,parity:=3,classes:=288,raw:=14155776,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1805),
rec(k:=15310,first:=1,last:=320,unitFirst:=32,unitLast:=351,order:=49152,autOrder:=1572864,parity:=3,classes:=320,raw:=15728640,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1749),
rec(k:=15311,first:=1,last:=241,unitFirst:=352,unitLast:=592,order:=49152,autOrder:=6291456,parity:=3,classes:=241,raw:=11845632,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1628),
rec(k:=15312,first:=1,last:=128,unitFirst:=593,unitLast:=720,order:=49152,autOrder:=1572864,parity:=1,classes:=128,raw:=6291456,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1499),
rec(k:=15313,first:=1,last:=128,unitFirst:=721,unitLast:=848,order:=49152,autOrder:=1572864,parity:=1,classes:=128,raw:=6291456,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1116),
rec(k:=15314,first:=1,last:=67,unitFirst:=849,unitLast:=915,order:=49152,autOrder:=6291456,parity:=3,classes:=1784,raw:=87687168,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=4730)
];
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard508_v7_gpt56sol.g");
