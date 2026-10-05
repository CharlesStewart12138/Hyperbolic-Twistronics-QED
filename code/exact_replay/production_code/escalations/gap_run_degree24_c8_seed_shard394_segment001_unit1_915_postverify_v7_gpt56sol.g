# Exact wrapper for sealed degree-24 seed workload shard394.
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD394_SEGMENT001_UNIT1_915_POSTVERIFY_V7_GPT56SOL.txt";
STOP_AFTER_UNIT:=fail;
INTERNAL_GUARD_MS:=1320000; START_UNIT:=1;
INITIAL_COUNTERS:=[0,0,0,0,0,0,0,0,0,0,0,0];
PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";
PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0;
PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";
CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD394_CHECKPOINT_GPT56SOL.txt";
CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD394_CHECKPOINT_TMP_GPT56SOL.txt";
EXPECTED_PROFILE_SHA256:="1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2";
EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard394_v7_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="1B16CEE2871474086E8C5D34B6D127B3332D85A948A1A52ABDA2045CC4493764";
S394_RECORDS:=[
rec(k:=15022,first:=236,last:=272,unitFirst:=1,unitLast:=37,order:=49152,autOrder:=3145728,parity:=3,classes:=272,raw:=13369344,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=2571),
rec(k:=15023,first:=1,last:=320,unitFirst:=38,unitLast:=357,order:=49152,autOrder:=393216,parity:=7,classes:=320,raw:=15728640,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=944),
rec(k:=15024,first:=1,last:=96,unitFirst:=358,unitLast:=453,order:=49152,autOrder:=1572864,parity:=3,classes:=96,raw:=4718592,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=2089),
rec(k:=15025,first:=1,last:=334,unitFirst:=454,unitLast:=787,order:=49152,autOrder:=3145728,parity:=3,classes:=334,raw:=16416768,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=3650),
rec(k:=15026,first:=1,last:=96,unitFirst:=788,unitLast:=883,order:=49152,autOrder:=1572864,parity:=3,classes:=96,raw:=4718592,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=2292),
rec(k:=15027,first:=1,last:=32,unitFirst:=884,unitLast:=915,order:=49152,autOrder:=9437184,parity:=3,classes:=242,raw:=11894784,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1075)
];
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard394_v7_gpt56sol.g");
