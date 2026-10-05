# Exact wrapper for sealed degree-24 seed workload shard108.
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD108_SEGMENT001_UNIT1_3662_POSTVERIFY_V7_GPT56SOL.txt";
STOP_AFTER_UNIT:=fail;
INTERNAL_GUARD_MS:=1320000; START_UNIT:=1;
INITIAL_COUNTERS:=[0,0,0,0,0,0,0,0,0,0,0,0];
PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";
PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0;
PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";
CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD108_CHECKPOINT_GPT56SOL.txt";
CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD108_CHECKPOINT_TMP_GPT56SOL.txt";
EXPECTED_PROFILE_SHA256:="1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2";
EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard108_v7_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="69E8819815B7479DA7BA19DE590059A71629B152471B4A9E7D89473CF5CE9775";
S108_RECORDS:=[
rec(k:=11976,first:=119,last:=640,unitFirst:=1,unitLast:=522,order:=12288,autOrder:=196608,parity:=3,classes:=640,raw:=7864320,method:="pc",representation:="pc_transport",pcOrder:=12288,profileMs:=1447),
rec(k:=11977,first:=1,last:=640,unitFirst:=523,unitLast:=1162,order:=12288,autOrder:=196608,parity:=3,classes:=640,raw:=7864320,method:="pc",representation:="pc_transport",pcOrder:=12288,profileMs:=1248),
rec(k:=11978,first:=1,last:=640,unitFirst:=1163,unitLast:=1802,order:=12288,autOrder:=196608,parity:=3,classes:=640,raw:=7864320,method:="pc",representation:="pc_transport",pcOrder:=12288,profileMs:=1711),
rec(k:=11979,first:=1,last:=640,unitFirst:=1803,unitLast:=2442,order:=12288,autOrder:=196608,parity:=3,classes:=640,raw:=7864320,method:="pc",representation:="pc_transport",pcOrder:=12288,profileMs:=1553),
rec(k:=11980,first:=1,last:=640,unitFirst:=2443,unitLast:=3082,order:=12288,autOrder:=196608,parity:=3,classes:=640,raw:=7864320,method:="pc",representation:="pc_transport",pcOrder:=12288,profileMs:=1368),
rec(k:=11981,first:=1,last:=580,unitFirst:=3083,unitLast:=3662,order:=12288,autOrder:=196608,parity:=3,classes:=640,raw:=7864320,method:="pc",representation:="pc_transport",pcOrder:=12288,profileMs:=1511)
];
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard108_v7_gpt56sol.g");
