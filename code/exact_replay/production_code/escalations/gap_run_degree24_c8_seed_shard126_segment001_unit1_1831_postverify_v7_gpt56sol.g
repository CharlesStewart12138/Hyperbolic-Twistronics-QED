# Exact wrapper for sealed degree-24 seed workload shard126.
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD126_SEGMENT001_UNIT1_1831_POSTVERIFY_V7_GPT56SOL.txt";
STOP_AFTER_UNIT:=fail;
INTERNAL_GUARD_MS:=1320000; START_UNIT:=1;
INITIAL_COUNTERS:=[0,0,0,0,0,0,0,0,0,0,0,0];
PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";
PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0;
PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";
CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD126_CHECKPOINT_GPT56SOL.txt";
CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD126_CHECKPOINT_TMP_GPT56SOL.txt";
EXPECTED_PROFILE_SHA256:="1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2";
EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard126_v7_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="6FB9C63D1CE9C366E4679B9132AE6CD85E89FEBABAC17B749BA0F9BA462198E7";
S126_RECORDS:=[
rec(k:=12782,first:=91,last:=112,unitFirst:=1,unitLast:=22,order:=24576,autOrder:=786432,parity:=3,classes:=112,raw:=2752512,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1567),
rec(k:=12783,first:=1,last:=96,unitFirst:=23,unitLast:=118,order:=24576,autOrder:=393216,parity:=3,classes:=96,raw:=2359296,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=951),
rec(k:=12784,first:=1,last:=112,unitFirst:=119,unitLast:=230,order:=24576,autOrder:=786432,parity:=7,classes:=112,raw:=2752512,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1228),
rec(k:=12785,first:=1,last:=98,unitFirst:=231,unitLast:=328,order:=24576,autOrder:=1572864,parity:=7,classes:=98,raw:=2408448,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1072),
rec(k:=12786,first:=1,last:=316,unitFirst:=329,unitLast:=644,order:=24576,autOrder:=6291456,parity:=15,classes:=316,raw:=7766016,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1448),
rec(k:=12787,first:=1,last:=116,unitFirst:=645,unitLast:=760,order:=24576,autOrder:=786432,parity:=3,classes:=116,raw:=2850816,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1253),
rec(k:=12788,first:=1,last:=236,unitFirst:=761,unitLast:=996,order:=24576,autOrder:=3145728,parity:=15,classes:=236,raw:=5799936,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1425),
rec(k:=12789,first:=1,last:=154,unitFirst:=997,unitLast:=1150,order:=24576,autOrder:=786432,parity:=3,classes:=154,raw:=3784704,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=910),
rec(k:=12790,first:=1,last:=208,unitFirst:=1151,unitLast:=1358,order:=24576,autOrder:=3145728,parity:=3,classes:=208,raw:=5111808,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1904),
rec(k:=12791,first:=1,last:=220,unitFirst:=1359,unitLast:=1578,order:=24576,autOrder:=3145728,parity:=3,classes:=220,raw:=5406720,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1155),
rec(k:=12792,first:=1,last:=128,unitFirst:=1579,unitLast:=1706,order:=24576,autOrder:=786432,parity:=7,classes:=128,raw:=3145728,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1127),
rec(k:=12793,first:=1,last:=125,unitFirst:=1707,unitLast:=1831,order:=24576,autOrder:=393216,parity:=7,classes:=128,raw:=3145728,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1441)
];
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard126_v7_gpt56sol.g");
