# Exact wrapper for sealed degree-24 seed workload shard151.
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD151_SEGMENT001_UNIT1_1831_POSTVERIFY_V7_GPT56SOL.txt";
STOP_AFTER_UNIT:=fail;
INTERNAL_GUARD_MS:=1320000; START_UNIT:=1;
INITIAL_COUNTERS:=[0,0,0,0,0,0,0,0,0,0,0,0];
PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";
PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0;
PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";
CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD151_CHECKPOINT_GPT56SOL.txt";
CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD151_CHECKPOINT_TMP_GPT56SOL.txt";
EXPECTED_PROFILE_SHA256:="1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2";
EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard151_v7_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="45AC1D055ABE66E798632A5F437C6468491198B12E00779345ED4F212B832941";
S151_RECORDS:=[
rec(k:=13046,first:=34,last:=262,unitFirst:=1,unitLast:=229,order:=24576,autOrder:=1572864,parity:=7,classes:=262,raw:=6438912,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1165),
rec(k:=13047,first:=1,last:=144,unitFirst:=230,unitLast:=373,order:=24576,autOrder:=393216,parity:=7,classes:=144,raw:=3538944,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1470),
rec(k:=13048,first:=1,last:=32,unitFirst:=374,unitLast:=405,order:=24576,autOrder:=393216,parity:=3,classes:=32,raw:=786432,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=905),
rec(k:=13049,first:=1,last:=180,unitFirst:=406,unitLast:=585,order:=24576,autOrder:=1572864,parity:=7,classes:=180,raw:=4423680,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1318),
rec(k:=13050,first:=1,last:=560,unitFirst:=586,unitLast:=1145,order:=24576,autOrder:=6291456,parity:=3,classes:=560,raw:=13762560,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1899),
rec(k:=13051,first:=1,last:=40,unitFirst:=1146,unitLast:=1185,order:=24576,autOrder:=98304,parity:=3,classes:=40,raw:=983040,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=679),
rec(k:=13052,first:=1,last:=160,unitFirst:=1186,unitLast:=1345,order:=24576,autOrder:=786432,parity:=1,classes:=160,raw:=3932160,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=889),
rec(k:=13053,first:=1,last:=60,unitFirst:=1346,unitLast:=1405,order:=24576,autOrder:=393216,parity:=1,classes:=60,raw:=1474560,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=998),
rec(k:=13054,first:=1,last:=240,unitFirst:=1406,unitLast:=1645,order:=24576,autOrder:=1572864,parity:=7,classes:=240,raw:=5898240,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=3097),
rec(k:=13055,first:=1,last:=128,unitFirst:=1646,unitLast:=1773,order:=24576,autOrder:=196608,parity:=15,classes:=128,raw:=3145728,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1369),
rec(k:=13056,first:=1,last:=58,unitFirst:=1774,unitLast:=1831,order:=24576,autOrder:=786432,parity:=7,classes:=600,raw:=14745600,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1768)
];
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard151_v7_gpt56sol.g");
