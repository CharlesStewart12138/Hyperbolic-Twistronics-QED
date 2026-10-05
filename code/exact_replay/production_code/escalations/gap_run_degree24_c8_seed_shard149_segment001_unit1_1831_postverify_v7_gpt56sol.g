# Exact wrapper for sealed degree-24 seed workload shard149.
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD149_SEGMENT001_UNIT1_1831_POSTVERIFY_V7_GPT56SOL.txt";
STOP_AFTER_UNIT:=fail;
INTERNAL_GUARD_MS:=1320000; START_UNIT:=1;
INITIAL_COUNTERS:=[0,0,0,0,0,0,0,0,0,0,0,0];
PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";
PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0;
PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";
CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD149_CHECKPOINT_GPT56SOL.txt";
CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD149_CHECKPOINT_TMP_GPT56SOL.txt";
EXPECTED_PROFILE_SHA256:="1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2";
EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard149_v7_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="6C08D21365A77F1C5A4CA94ABC866ABB5E341C36F63BA2A33E441C6B495AB37C";
S149_RECORDS:=[
rec(k:=13030,first:=144,last:=752,unitFirst:=1,unitLast:=609,order:=24576,autOrder:=1572864,parity:=15,classes:=752,raw:=18481152,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=2084),
rec(k:=13031,first:=1,last:=32,unitFirst:=610,unitLast:=641,order:=24576,autOrder:=393216,parity:=3,classes:=32,raw:=786432,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1736),
rec(k:=13032,first:=1,last:=568,unitFirst:=642,unitLast:=1209,order:=24576,autOrder:=786432,parity:=3,classes:=568,raw:=13959168,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1630),
rec(k:=13033,first:=1,last:=144,unitFirst:=1210,unitLast:=1353,order:=24576,autOrder:=393216,parity:=15,classes:=144,raw:=3538944,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=2012),
rec(k:=13034,first:=1,last:=478,unitFirst:=1354,unitLast:=1831,order:=24576,autOrder:=6291456,parity:=3,classes:=560,raw:=13762560,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1877)
];
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard149_v7_gpt56sol.g");
