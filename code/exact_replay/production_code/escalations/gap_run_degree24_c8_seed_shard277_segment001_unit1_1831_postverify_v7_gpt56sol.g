# Exact wrapper for sealed degree-24 seed workload shard277.
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD277_SEGMENT001_UNIT1_1831_POSTVERIFY_V7_GPT56SOL.txt";
STOP_AFTER_UNIT:=fail;
INTERNAL_GUARD_MS:=1320000; START_UNIT:=1;
INITIAL_COUNTERS:=[0,0,0,0,0,0,0,0,0,0,0,0];
PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";
PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0;
PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";
CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD277_CHECKPOINT_GPT56SOL.txt";
CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD277_CHECKPOINT_TMP_GPT56SOL.txt";
EXPECTED_PROFILE_SHA256:="1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2";
EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard277_v7_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="BB7470B16CEE090AD4783B290EF04103ADC512B000651D9599A72D260D3291ED";
S277_RECORDS:=[
rec(k:=13822,first:=170,last:=348,unitFirst:=1,unitLast:=179,order:=24576,autOrder:=393216,parity:=7,classes:=348,raw:=8552448,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1140),
rec(k:=13823,first:=1,last:=348,unitFirst:=180,unitLast:=527,order:=24576,autOrder:=393216,parity:=7,classes:=348,raw:=8552448,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1284),
rec(k:=13824,first:=1,last:=348,unitFirst:=528,unitLast:=875,order:=24576,autOrder:=393216,parity:=7,classes:=348,raw:=8552448,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=982),
rec(k:=13825,first:=1,last:=48,unitFirst:=876,unitLast:=923,order:=24576,autOrder:=196608,parity:=7,classes:=48,raw:=1179648,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=666),
rec(k:=13826,first:=1,last:=48,unitFirst:=924,unitLast:=971,order:=24576,autOrder:=196608,parity:=7,classes:=48,raw:=1179648,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=632),
rec(k:=13827,first:=1,last:=48,unitFirst:=972,unitLast:=1019,order:=24576,autOrder:=196608,parity:=7,classes:=48,raw:=1179648,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=659),
rec(k:=13828,first:=1,last:=48,unitFirst:=1020,unitLast:=1067,order:=24576,autOrder:=196608,parity:=7,classes:=48,raw:=1179648,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=716),
rec(k:=13829,first:=1,last:=112,unitFirst:=1068,unitLast:=1179,order:=24576,autOrder:=196608,parity:=7,classes:=112,raw:=2752512,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=784),
rec(k:=13830,first:=1,last:=112,unitFirst:=1180,unitLast:=1291,order:=24576,autOrder:=196608,parity:=7,classes:=112,raw:=2752512,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=926),
rec(k:=13831,first:=1,last:=112,unitFirst:=1292,unitLast:=1403,order:=24576,autOrder:=196608,parity:=7,classes:=112,raw:=2752512,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=937),
rec(k:=13832,first:=1,last:=112,unitFirst:=1404,unitLast:=1515,order:=24576,autOrder:=196608,parity:=7,classes:=112,raw:=2752512,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1270),
rec(k:=13833,first:=1,last:=128,unitFirst:=1516,unitLast:=1643,order:=24576,autOrder:=393216,parity:=7,classes:=128,raw:=3145728,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=2832),
rec(k:=13834,first:=1,last:=128,unitFirst:=1644,unitLast:=1771,order:=24576,autOrder:=393216,parity:=7,classes:=128,raw:=3145728,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1106),
rec(k:=13835,first:=1,last:=60,unitFirst:=1772,unitLast:=1831,order:=24576,autOrder:=393216,parity:=7,classes:=128,raw:=3145728,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1306)
];
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard277_v7_gpt56sol.g");
