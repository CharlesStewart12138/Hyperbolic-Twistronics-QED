# Exact wrapper for sealed degree-24 seed workload shard181.
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD181_SEGMENT001_UNIT1_1831_POSTVERIFY_V7_GPT56SOL.txt";
STOP_AFTER_UNIT:=fail;
INTERNAL_GUARD_MS:=1320000; START_UNIT:=1;
INITIAL_COUNTERS:=[0,0,0,0,0,0,0,0,0,0,0,0];
PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";
PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0;
PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";
CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD181_CHECKPOINT_GPT56SOL.txt";
CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD181_CHECKPOINT_TMP_GPT56SOL.txt";
EXPECTED_PROFILE_SHA256:="1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2";
EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard181_v7_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="E80167657C873548913C0F25CCA3C7C34898DD9D3BABB1DC80F57014F182EB04";
S181_RECORDS:=[
rec(k:=13326,first:=51,last:=128,unitFirst:=1,unitLast:=78,order:=24576,autOrder:=786432,parity:=3,classes:=128,raw:=3145728,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1128),
rec(k:=13327,first:=1,last:=64,unitFirst:=79,unitLast:=142,order:=24576,autOrder:=393216,parity:=3,classes:=64,raw:=1572864,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1056),
rec(k:=13328,first:=1,last:=120,unitFirst:=143,unitLast:=262,order:=24576,autOrder:=786432,parity:=3,classes:=120,raw:=2949120,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=937),
rec(k:=13329,first:=1,last:=504,unitFirst:=263,unitLast:=766,order:=24576,autOrder:=9059696640,parity:=7,classes:=504,raw:=12386304,method:="native",representation:="pc_transport",pcOrder:=24576,profileMs:=73924),
rec(k:=13330,first:=1,last:=348,unitFirst:=767,unitLast:=1114,order:=24576,autOrder:=1572864,parity:=3,classes:=348,raw:=8552448,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1585),
rec(k:=13331,first:=1,last:=72,unitFirst:=1115,unitLast:=1186,order:=24576,autOrder:=786432,parity:=3,classes:=72,raw:=1769472,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1077),
rec(k:=13332,first:=1,last:=64,unitFirst:=1187,unitLast:=1250,order:=24576,autOrder:=393216,parity:=3,classes:=64,raw:=1572864,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1204),
rec(k:=13333,first:=1,last:=64,unitFirst:=1251,unitLast:=1314,order:=24576,autOrder:=393216,parity:=3,classes:=64,raw:=1572864,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=974),
rec(k:=13334,first:=1,last:=32,unitFirst:=1315,unitLast:=1346,order:=24576,autOrder:=393216,parity:=3,classes:=32,raw:=786432,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=826),
rec(k:=13335,first:=1,last:=485,unitFirst:=1347,unitLast:=1831,order:=24576,autOrder:=6291456,parity:=7,classes:=925,raw:=22732800,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=2679)
];
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard181_v7_gpt56sol.g");
