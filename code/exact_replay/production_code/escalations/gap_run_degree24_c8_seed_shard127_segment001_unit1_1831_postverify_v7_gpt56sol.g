# Exact wrapper for sealed degree-24 seed workload shard127.
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD127_SEGMENT001_UNIT1_1831_POSTVERIFY_V7_GPT56SOL.txt";
STOP_AFTER_UNIT:=fail;
INTERNAL_GUARD_MS:=1320000; START_UNIT:=1;
INITIAL_COUNTERS:=[0,0,0,0,0,0,0,0,0,0,0,0];
PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";
PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0;
PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";
CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD127_CHECKPOINT_GPT56SOL.txt";
CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD127_CHECKPOINT_TMP_GPT56SOL.txt";
EXPECTED_PROFILE_SHA256:="1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2";
EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard127_v7_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="2D29F2B1550341D3B3F7F61A40F788895D77E671B886F59264EC453219138E71";
S127_RECORDS:=[
rec(k:=12793,first:=126,last:=128,unitFirst:=1,unitLast:=3,order:=24576,autOrder:=393216,parity:=7,classes:=128,raw:=3145728,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1441),
rec(k:=12794,first:=1,last:=96,unitFirst:=4,unitLast:=99,order:=24576,autOrder:=786432,parity:=7,classes:=96,raw:=2359296,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=811),
rec(k:=12795,first:=1,last:=128,unitFirst:=100,unitLast:=227,order:=24576,autOrder:=393216,parity:=7,classes:=128,raw:=3145728,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=883),
rec(k:=12796,first:=1,last:=128,unitFirst:=228,unitLast:=355,order:=24576,autOrder:=786432,parity:=7,classes:=128,raw:=3145728,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1256),
rec(k:=12797,first:=1,last:=96,unitFirst:=356,unitLast:=451,order:=24576,autOrder:=786432,parity:=7,classes:=96,raw:=2359296,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=753),
rec(k:=12798,first:=1,last:=128,unitFirst:=452,unitLast:=579,order:=24576,autOrder:=786432,parity:=7,classes:=128,raw:=3145728,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1214),
rec(k:=12799,first:=1,last:=112,unitFirst:=580,unitLast:=691,order:=24576,autOrder:=786432,parity:=7,classes:=112,raw:=2752512,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1075),
rec(k:=12800,first:=1,last:=120,unitFirst:=692,unitLast:=811,order:=24576,autOrder:=786432,parity:=7,classes:=120,raw:=2949120,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1144),
rec(k:=12801,first:=1,last:=120,unitFirst:=812,unitLast:=931,order:=24576,autOrder:=786432,parity:=7,classes:=120,raw:=2949120,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=964),
rec(k:=12802,first:=1,last:=144,unitFirst:=932,unitLast:=1075,order:=24576,autOrder:=786432,parity:=15,classes:=144,raw:=3538944,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1636),
rec(k:=12803,first:=1,last:=128,unitFirst:=1076,unitLast:=1203,order:=24576,autOrder:=786432,parity:=15,classes:=128,raw:=3145728,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=769),
rec(k:=12804,first:=1,last:=120,unitFirst:=1204,unitLast:=1323,order:=24576,autOrder:=786432,parity:=7,classes:=120,raw:=2949120,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=985),
rec(k:=12805,first:=1,last:=120,unitFirst:=1324,unitLast:=1443,order:=24576,autOrder:=786432,parity:=7,classes:=120,raw:=2949120,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=976),
rec(k:=12806,first:=1,last:=144,unitFirst:=1444,unitLast:=1587,order:=24576,autOrder:=393216,parity:=15,classes:=144,raw:=3538944,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1273),
rec(k:=12807,first:=1,last:=88,unitFirst:=1588,unitLast:=1675,order:=24576,autOrder:=393216,parity:=3,classes:=88,raw:=2162688,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1033),
rec(k:=12808,first:=1,last:=96,unitFirst:=1676,unitLast:=1771,order:=24576,autOrder:=393216,parity:=15,classes:=96,raw:=2359296,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=903),
rec(k:=12809,first:=1,last:=60,unitFirst:=1772,unitLast:=1831,order:=24576,autOrder:=393216,parity:=3,classes:=88,raw:=2162688,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=920)
];
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard127_v7_gpt56sol.g");
