# Exact wrapper for sealed degree-24 seed workload shard174.
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD174_SEGMENT001_UNIT1_1831_POSTVERIFY_V7_GPT56SOL.txt";
STOP_AFTER_UNIT:=fail;
INTERNAL_GUARD_MS:=1320000; START_UNIT:=1;
INITIAL_COUNTERS:=[0,0,0,0,0,0,0,0,0,0,0,0];
PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";
PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0;
PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";
CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD174_CHECKPOINT_GPT56SOL.txt";
CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD174_CHECKPOINT_TMP_GPT56SOL.txt";
EXPECTED_PROFILE_SHA256:="1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2";
EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard174_v7_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="841F70D9B5E394FE48871DEB60663CE35E07CC237CAEF13D846F8F8676B2C93B";
S174_RECORDS:=[
rec(k:=13254,first:=12,last:=154,unitFirst:=1,unitLast:=143,order:=24576,autOrder:=9437184,parity:=3,classes:=154,raw:=3784704,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=2444),
rec(k:=13255,first:=1,last:=66,unitFirst:=144,unitLast:=209,order:=24576,autOrder:=4718592,parity:=3,classes:=66,raw:=1622016,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=2413),
rec(k:=13256,first:=1,last:=148,unitFirst:=210,unitLast:=357,order:=24576,autOrder:=9437184,parity:=3,classes:=148,raw:=3637248,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1451),
rec(k:=13257,first:=1,last:=24,unitFirst:=358,unitLast:=381,order:=24576,autOrder:=393216,parity:=15,classes:=24,raw:=589824,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=719),
rec(k:=13258,first:=1,last:=60,unitFirst:=382,unitLast:=441,order:=24576,autOrder:=393216,parity:=3,classes:=60,raw:=1474560,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1152),
rec(k:=13259,first:=1,last:=92,unitFirst:=442,unitLast:=533,order:=24576,autOrder:=393216,parity:=3,classes:=92,raw:=2260992,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=955),
rec(k:=13260,first:=1,last:=128,unitFirst:=534,unitLast:=661,order:=24576,autOrder:=393216,parity:=3,classes:=128,raw:=3145728,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=936),
rec(k:=13261,first:=1,last:=128,unitFirst:=662,unitLast:=789,order:=24576,autOrder:=393216,parity:=3,classes:=128,raw:=3145728,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1227),
rec(k:=13262,first:=1,last:=288,unitFirst:=790,unitLast:=1077,order:=24576,autOrder:=393216,parity:=15,classes:=288,raw:=7077888,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=810),
rec(k:=13263,first:=1,last:=124,unitFirst:=1078,unitLast:=1201,order:=24576,autOrder:=393216,parity:=3,classes:=124,raw:=3047424,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1839),
rec(k:=13264,first:=1,last:=120,unitFirst:=1202,unitLast:=1321,order:=24576,autOrder:=393216,parity:=3,classes:=120,raw:=2949120,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1886),
rec(k:=13265,first:=1,last:=72,unitFirst:=1322,unitLast:=1393,order:=24576,autOrder:=393216,parity:=3,classes:=72,raw:=1769472,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=874),
rec(k:=13266,first:=1,last:=60,unitFirst:=1394,unitLast:=1453,order:=24576,autOrder:=393216,parity:=3,classes:=60,raw:=1474560,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1226),
rec(k:=13267,first:=1,last:=112,unitFirst:=1454,unitLast:=1565,order:=24576,autOrder:=393216,parity:=15,classes:=112,raw:=2752512,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1034),
rec(k:=13268,first:=1,last:=100,unitFirst:=1566,unitLast:=1665,order:=24576,autOrder:=393216,parity:=3,classes:=100,raw:=2457600,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1168),
rec(k:=13269,first:=1,last:=160,unitFirst:=1666,unitLast:=1825,order:=24576,autOrder:=393216,parity:=3,classes:=160,raw:=3932160,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1521),
rec(k:=13270,first:=1,last:=6,unitFirst:=1826,unitLast:=1831,order:=24576,autOrder:=393216,parity:=3,classes:=108,raw:=2654208,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1749)
];
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard174_v7_gpt56sol.g");
