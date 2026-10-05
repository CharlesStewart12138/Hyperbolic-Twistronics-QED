# Exact wrapper for sealed degree-24 seed workload shard141.
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD141_SEGMENT001_UNIT1_1831_POSTVERIFY_V7_GPT56SOL.txt";
STOP_AFTER_UNIT:=fail;
INTERNAL_GUARD_MS:=1320000; START_UNIT:=1;
INITIAL_COUNTERS:=[0,0,0,0,0,0,0,0,0,0,0,0];
PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";
PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0;
PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";
CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD141_CHECKPOINT_GPT56SOL.txt";
CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD141_CHECKPOINT_TMP_GPT56SOL.txt";
EXPECTED_PROFILE_SHA256:="1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2";
EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard141_v7_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="AF65BC6855AC5D6A56FDAA49CDA1A3DBEA9576048CCAE2CAC8E5ACAF1EB0600A";
S141_RECORDS:=[
rec(k:=12966,first:=159,last:=160,unitFirst:=1,unitLast:=2,order:=24576,autOrder:=786432,parity:=1,classes:=160,raw:=3932160,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1368),
rec(k:=12967,first:=1,last:=96,unitFirst:=3,unitLast:=98,order:=24576,autOrder:=393216,parity:=3,classes:=96,raw:=2359296,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1474),
rec(k:=12968,first:=1,last:=160,unitFirst:=99,unitLast:=258,order:=24576,autOrder:=786432,parity:=1,classes:=160,raw:=3932160,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=960),
rec(k:=12969,first:=1,last:=164,unitFirst:=259,unitLast:=422,order:=24576,autOrder:=786432,parity:=7,classes:=164,raw:=4030464,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1357),
rec(k:=12970,first:=1,last:=128,unitFirst:=423,unitLast:=550,order:=24576,autOrder:=393216,parity:=3,classes:=128,raw:=3145728,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1221),
rec(k:=12971,first:=1,last:=64,unitFirst:=551,unitLast:=614,order:=24576,autOrder:=786432,parity:=1,classes:=64,raw:=1572864,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1694),
rec(k:=12972,first:=1,last:=1217,unitFirst:=615,unitLast:=1831,order:=24576,autOrder:=50331648,parity:=3,classes:=1700,raw:=41779200,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=5550)
];
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard141_v7_gpt56sol.g");
