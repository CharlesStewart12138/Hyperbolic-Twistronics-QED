# Exact wrapper for sealed degree-24 seed workload shard245.
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD245_SEGMENT001_UNIT1_1831_POSTVERIFY_V7_GPT56SOL.txt";
STOP_AFTER_UNIT:=fail;
INTERNAL_GUARD_MS:=1320000; START_UNIT:=1;
INITIAL_COUNTERS:=[0,0,0,0,0,0,0,0,0,0,0,0];
PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";
PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0;
PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";
CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD245_CHECKPOINT_GPT56SOL.txt";
CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD245_CHECKPOINT_TMP_GPT56SOL.txt";
EXPECTED_PROFILE_SHA256:="1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2";
EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard245_v7_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="B678E9DB2F2DE6190CDD5B64DC007AF6F51FEB56A158DBF854E55336287104F3";
S245_RECORDS:=[
rec(k:=13698,first:=312,last:=640,unitFirst:=1,unitLast:=329,order:=24576,autOrder:=393216,parity:=15,classes:=640,raw:=15728640,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1400),
rec(k:=13699,first:=1,last:=128,unitFirst:=330,unitLast:=457,order:=24576,autOrder:=196608,parity:=15,classes:=128,raw:=3145728,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1837),
rec(k:=13700,first:=1,last:=128,unitFirst:=458,unitLast:=585,order:=24576,autOrder:=196608,parity:=15,classes:=128,raw:=3145728,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1146),
rec(k:=13701,first:=1,last:=128,unitFirst:=586,unitLast:=713,order:=24576,autOrder:=196608,parity:=15,classes:=128,raw:=3145728,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1953),
rec(k:=13702,first:=1,last:=128,unitFirst:=714,unitLast:=841,order:=24576,autOrder:=196608,parity:=15,classes:=128,raw:=3145728,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1380),
rec(k:=13703,first:=1,last:=120,unitFirst:=842,unitLast:=961,order:=24576,autOrder:=786432,parity:=15,classes:=120,raw:=2949120,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=959),
rec(k:=13704,first:=1,last:=48,unitFirst:=962,unitLast:=1009,order:=24576,autOrder:=393216,parity:=15,classes:=48,raw:=1179648,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1060),
rec(k:=13705,first:=1,last:=24,unitFirst:=1010,unitLast:=1033,order:=24576,autOrder:=393216,parity:=15,classes:=24,raw:=589824,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=814),
rec(k:=13706,first:=1,last:=108,unitFirst:=1034,unitLast:=1141,order:=24576,autOrder:=786432,parity:=15,classes:=108,raw:=2654208,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1295),
rec(k:=13707,first:=1,last:=128,unitFirst:=1142,unitLast:=1269,order:=24576,autOrder:=196608,parity:=15,classes:=128,raw:=3145728,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1236),
rec(k:=13708,first:=1,last:=144,unitFirst:=1270,unitLast:=1413,order:=24576,autOrder:=393216,parity:=15,classes:=144,raw:=3538944,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1059),
rec(k:=13709,first:=1,last:=128,unitFirst:=1414,unitLast:=1541,order:=24576,autOrder:=196608,parity:=15,classes:=128,raw:=3145728,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1305),
rec(k:=13710,first:=1,last:=176,unitFirst:=1542,unitLast:=1717,order:=24576,autOrder:=786432,parity:=15,classes:=176,raw:=4325376,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1217),
rec(k:=13711,first:=1,last:=114,unitFirst:=1718,unitLast:=1831,order:=24576,autOrder:=196608,parity:=15,classes:=128,raw:=3145728,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1300)
];
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard245_v7_gpt56sol.g");
