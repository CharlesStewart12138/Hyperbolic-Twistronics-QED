# Exact wrapper for sealed degree-24 seed workload shard288.
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD288_SEGMENT001_UNIT1_1831_POSTVERIFY_V7_GPT56SOL.txt";
STOP_AFTER_UNIT:=fail;
INTERNAL_GUARD_MS:=1320000; START_UNIT:=1;
INITIAL_COUNTERS:=[0,0,0,0,0,0,0,0,0,0,0,0];
PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";
PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0;
PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";
CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD288_CHECKPOINT_GPT56SOL.txt";
CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD288_CHECKPOINT_TMP_GPT56SOL.txt";
EXPECTED_PROFILE_SHA256:="1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2";
EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard288_v7_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="B50ADA5719BF3BD11728417FD7B9B18353C4B64651E57CFDC2A50DA97A133E47";
S288_RECORDS:=[
rec(k:=13892,first:=216,last:=392,unitFirst:=1,unitLast:=177,order:=24576,autOrder:=196608,parity:=7,classes:=392,raw:=9633792,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1164),
rec(k:=13893,first:=1,last:=402,unitFirst:=178,unitLast:=579,order:=24576,autOrder:=393216,parity:=7,classes:=402,raw:=9879552,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=949),
rec(k:=13894,first:=1,last:=292,unitFirst:=580,unitLast:=871,order:=24576,autOrder:=196608,parity:=3,classes:=292,raw:=7176192,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=860),
rec(k:=13895,first:=1,last:=96,unitFirst:=872,unitLast:=967,order:=24576,autOrder:=393216,parity:=3,classes:=96,raw:=2359296,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1299),
rec(k:=13896,first:=1,last:=336,unitFirst:=968,unitLast:=1303,order:=24576,autOrder:=393216,parity:=3,classes:=336,raw:=8257536,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=812),
rec(k:=13897,first:=1,last:=344,unitFirst:=1304,unitLast:=1647,order:=24576,autOrder:=393216,parity:=3,classes:=344,raw:=8454144,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=930),
rec(k:=13898,first:=1,last:=184,unitFirst:=1648,unitLast:=1831,order:=24576,autOrder:=786432,parity:=7,classes:=754,raw:=18530304,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1379)
];
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard288_v7_gpt56sol.g");
