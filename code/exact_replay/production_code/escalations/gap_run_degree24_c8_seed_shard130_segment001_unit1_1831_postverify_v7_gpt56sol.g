# Exact wrapper for sealed degree-24 seed workload shard130.
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD130_SEGMENT001_UNIT1_1831_POSTVERIFY_V7_GPT56SOL.txt";
STOP_AFTER_UNIT:=fail;
INTERNAL_GUARD_MS:=1320000; START_UNIT:=1;
INITIAL_COUNTERS:=[0,0,0,0,0,0,0,0,0,0,0,0];
PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";
PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0;
PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";
CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD130_CHECKPOINT_GPT56SOL.txt";
CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD130_CHECKPOINT_TMP_GPT56SOL.txt";
EXPECTED_PROFILE_SHA256:="1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2";
EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard130_v7_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="DB7FC9CD81C0F5AF2863AB026462F57A8941F0FC5D125F5B7B66EA80ED077609";
S130_RECORDS:=[
rec(k:=12850,first:=63,last:=208,unitFirst:=1,unitLast:=146,order:=24576,autOrder:=3145728,parity:=3,classes:=208,raw:=5111808,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=2780),
rec(k:=12851,first:=1,last:=238,unitFirst:=147,unitLast:=384,order:=24576,autOrder:=3145728,parity:=3,classes:=238,raw:=5849088,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=2265),
rec(k:=12852,first:=1,last:=326,unitFirst:=385,unitLast:=710,order:=24576,autOrder:=6291456,parity:=3,classes:=326,raw:=8011776,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=2262),
rec(k:=12853,first:=1,last:=214,unitFirst:=711,unitLast:=924,order:=24576,autOrder:=3145728,parity:=3,classes:=214,raw:=5259264,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=2354),
rec(k:=12855,first:=1,last:=376,unitFirst:=925,unitLast:=1300,order:=24576,autOrder:=3145728,parity:=1,classes:=376,raw:=9240576,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1620),
rec(k:=12856,first:=1,last:=156,unitFirst:=1301,unitLast:=1456,order:=24576,autOrder:=3145728,parity:=1,classes:=156,raw:=3833856,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1591),
rec(k:=12857,first:=1,last:=256,unitFirst:=1457,unitLast:=1712,order:=24576,autOrder:=75497472,parity:=3,classes:=256,raw:=6291456,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=2323),
rec(k:=12858,first:=1,last:=119,unitFirst:=1713,unitLast:=1831,order:=24576,autOrder:=6291456,parity:=1,classes:=142,raw:=3489792,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1437)
];
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard130_v7_gpt56sol.g");
