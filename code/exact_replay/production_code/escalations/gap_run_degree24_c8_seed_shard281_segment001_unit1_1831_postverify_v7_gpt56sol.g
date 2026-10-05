# Exact wrapper for sealed degree-24 seed workload shard281.
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD281_SEGMENT001_UNIT1_1831_POSTVERIFY_V7_GPT56SOL.txt";
STOP_AFTER_UNIT:=fail;
INTERNAL_GUARD_MS:=1320000; START_UNIT:=1;
INITIAL_COUNTERS:=[0,0,0,0,0,0,0,0,0,0,0,0];
PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";
PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0;
PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";
CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD281_CHECKPOINT_GPT56SOL.txt";
CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD281_CHECKPOINT_TMP_GPT56SOL.txt";
EXPECTED_PROFILE_SHA256:="1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2";
EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard281_v7_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="D43571389F72DF89C26FF2C1747AB631DF7A6052F8692C1FC7E81065A851DCF1";
S281_RECORDS:=[
rec(k:=13858,first:=176,last:=452,unitFirst:=1,unitLast:=277,order:=24576,autOrder:=786432,parity:=7,classes:=452,raw:=11108352,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1581),
rec(k:=13859,first:=1,last:=144,unitFirst:=278,unitLast:=421,order:=24576,autOrder:=393216,parity:=7,classes:=144,raw:=3538944,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1637),
rec(k:=13860,first:=1,last:=96,unitFirst:=422,unitLast:=517,order:=24576,autOrder:=196608,parity:=3,classes:=96,raw:=2359296,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1211),
rec(k:=13861,first:=1,last:=128,unitFirst:=518,unitLast:=645,order:=24576,autOrder:=786432,parity:=7,classes:=128,raw:=3145728,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1508),
rec(k:=13862,first:=1,last:=72,unitFirst:=646,unitLast:=717,order:=24576,autOrder:=393216,parity:=3,classes:=72,raw:=1769472,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1250),
rec(k:=13863,first:=1,last:=242,unitFirst:=718,unitLast:=959,order:=24576,autOrder:=393216,parity:=3,classes:=242,raw:=5947392,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1448),
rec(k:=13864,first:=1,last:=348,unitFirst:=960,unitLast:=1307,order:=24576,autOrder:=786432,parity:=7,classes:=348,raw:=8552448,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1647),
rec(k:=13865,first:=1,last:=16,unitFirst:=1308,unitLast:=1323,order:=24576,autOrder:=196608,parity:=15,classes:=16,raw:=393216,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=742),
rec(k:=13866,first:=1,last:=508,unitFirst:=1324,unitLast:=1831,order:=24576,autOrder:=196608,parity:=15,classes:=560,raw:=13762560,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=2858)
];
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard281_v7_gpt56sol.g");
