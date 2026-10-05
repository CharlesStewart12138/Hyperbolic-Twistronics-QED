# Exact wrapper for sealed degree-24 seed workload shard135.
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD135_SEGMENT002_UNIT400_1831_POSTVERIFY_V7_GPT56SOL.txt";
STOP_AFTER_UNIT:=fail;
INTERNAL_GUARD_MS:=1320000; START_UNIT:=400;
INITIAL_COUNTERS:=[399,9805824,399,40,270528,91776,61824,12928,0,0,0,0];
PREVIOUS_CHECKPOINT_SHA256:="2f7a845e2a26fffa2e624e75e296c34b03e259b36d14c924f5d442ca34c173e4";
PREVIOUS_OUTPUT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD135_SEGMENT001_UNIT1_1831_POSTVERIFY_V7_GPT56SOL.txt"; PREVIOUS_OUTPUT_PREFIX_BYTES:=298673;
PREVIOUS_OUTPUT_PREFIX_SHA256:="604a6adb33e841f6fdf3fc171e5de017d4cd70ce843ad2cef17a294ecd7e622e";
CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD135_CHECKPOINT_GPT56SOL.txt";
CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD135_CHECKPOINT_TMP_GPT56SOL.txt";
EXPECTED_PROFILE_SHA256:="1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2";
EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard135_v7_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="92DBE8C0C814C4DB12A9D00CF8FD47FE5CD57F345E674F52ACE37A9D037A63EB";
S135_RECORDS:=[
rec(k:=12922,first:=65,last:=277,unitFirst:=1,unitLast:=213,order:=24576,autOrder:=3145728,parity:=1,classes:=277,raw:=6807552,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=866),
rec(k:=12923,first:=1,last:=160,unitFirst:=214,unitLast:=373,order:=24576,autOrder:=786432,parity:=1,classes:=160,raw:=3932160,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1253),
rec(k:=12924,first:=1,last:=137,unitFirst:=374,unitLast:=510,order:=24576,autOrder:=1572864,parity:=1,classes:=137,raw:=3366912,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=894),
rec(k:=12925,first:=1,last:=136,unitFirst:=511,unitLast:=646,order:=24576,autOrder:=1572864,parity:=1,classes:=136,raw:=3342336,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1741),
rec(k:=12926,first:=1,last:=104,unitFirst:=647,unitLast:=750,order:=24576,autOrder:=1572864,parity:=1,classes:=104,raw:=2555904,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1224),
rec(k:=12927,first:=1,last:=574,unitFirst:=751,unitLast:=1324,order:=24576,autOrder:=6291456,parity:=3,classes:=574,raw:=14106624,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=2112),
rec(k:=12928,first:=1,last:=277,unitFirst:=1325,unitLast:=1601,order:=24576,autOrder:=3145728,parity:=1,classes:=277,raw:=6807552,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=948),
rec(k:=12929,first:=1,last:=160,unitFirst:=1602,unitLast:=1761,order:=24576,autOrder:=786432,parity:=1,classes:=160,raw:=3932160,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1349),
rec(k:=12930,first:=1,last:=70,unitFirst:=1762,unitLast:=1831,order:=24576,autOrder:=1572864,parity:=1,classes:=576,raw:=14155776,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=2019)
];
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard135_v7_gpt56sol.g");
