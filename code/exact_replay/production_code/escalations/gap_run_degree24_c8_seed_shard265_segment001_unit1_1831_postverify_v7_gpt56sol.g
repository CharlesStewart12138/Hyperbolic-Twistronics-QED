# Exact wrapper for sealed degree-24 seed workload shard265.
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD265_SEGMENT001_UNIT1_1831_POSTVERIFY_V7_GPT56SOL.txt";
STOP_AFTER_UNIT:=fail;
INTERNAL_GUARD_MS:=1320000; START_UNIT:=1;
INITIAL_COUNTERS:=[0,0,0,0,0,0,0,0,0,0,0,0];
PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";
PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0;
PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";
CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD265_CHECKPOINT_GPT56SOL.txt";
CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD265_CHECKPOINT_TMP_GPT56SOL.txt";
EXPECTED_PROFILE_SHA256:="1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2";
EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard265_v7_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="8B14C715F7281E05006EBDB6FF47B64D4CF21605F00B9FAEC6BEDA18986CA0D9";
S265_RECORDS:=[
rec(k:=13785,first:=808,last:=1784,unitFirst:=1,unitLast:=977,order:=24576,autOrder:=6291456,parity:=1,classes:=1784,raw:=43843584,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=3046),
rec(k:=13786,first:=1,last:=156,unitFirst:=978,unitLast:=1133,order:=24576,autOrder:=3145728,parity:=1,classes:=156,raw:=3833856,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1377),
rec(k:=13787,first:=1,last:=64,unitFirst:=1134,unitLast:=1197,order:=24576,autOrder:=786432,parity:=1,classes:=64,raw:=1572864,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1458),
rec(k:=13788,first:=1,last:=156,unitFirst:=1198,unitLast:=1353,order:=24576,autOrder:=3145728,parity:=1,classes:=156,raw:=3833856,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1673),
rec(k:=13789,first:=1,last:=478,unitFirst:=1354,unitLast:=1831,order:=24576,autOrder:=603979776,parity:=1,classes:=784,raw:=19267584,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=12511)
];
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard265_v7_gpt56sol.g");
