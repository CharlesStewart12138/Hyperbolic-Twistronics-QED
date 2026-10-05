# Exact wrapper for sealed degree-24 seed workload shard261.
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD261_SEGMENT001_UNIT1_1831_POSTVERIFY_V7_GPT56SOL.txt";
STOP_AFTER_UNIT:=fail;
INTERNAL_GUARD_MS:=1320000; START_UNIT:=1;
INITIAL_COUNTERS:=[0,0,0,0,0,0,0,0,0,0,0,0];
PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";
PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0;
PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";
CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD261_CHECKPOINT_GPT56SOL.txt";
CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD261_CHECKPOINT_TMP_GPT56SOL.txt";
EXPECTED_PROFILE_SHA256:="1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2";
EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard261_v7_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="1EADA5D1DC30D63EB63EB54DB742874073903A5D1C9A6ABFF4358679AF75AEF0";
S261_RECORDS:=[
rec(k:=13775,first:=482,last:=800,unitFirst:=1,unitLast:=319,order:=24576,autOrder:=393216,parity:=7,classes:=800,raw:=19660800,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1922),
rec(k:=13776,first:=1,last:=128,unitFirst:=320,unitLast:=447,order:=24576,autOrder:=393216,parity:=7,classes:=128,raw:=3145728,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1671),
rec(k:=13777,first:=1,last:=128,unitFirst:=448,unitLast:=575,order:=24576,autOrder:=393216,parity:=7,classes:=128,raw:=3145728,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=2068),
rec(k:=13778,first:=1,last:=128,unitFirst:=576,unitLast:=703,order:=24576,autOrder:=393216,parity:=7,classes:=128,raw:=3145728,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1369),
rec(k:=13779,first:=1,last:=128,unitFirst:=704,unitLast:=831,order:=24576,autOrder:=393216,parity:=7,classes:=128,raw:=3145728,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1277),
rec(k:=13780,first:=1,last:=991,unitFirst:=832,unitLast:=1822,order:=24576,autOrder:=3145728,parity:=1,classes:=991,raw:=24354816,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=2844),
rec(k:=13781,first:=1,last:=9,unitFirst:=1823,unitLast:=1831,order:=24576,autOrder:=3145728,parity:=1,classes:=1088,raw:=26738688,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=3199)
];
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard261_v7_gpt56sol.g");
