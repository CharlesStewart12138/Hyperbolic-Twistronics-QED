# Exact wrapper for sealed degree-24 seed workload shard164.
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD164_SEGMENT001_UNIT1_1831_POSTVERIFY_V7_GPT56SOL.txt";
STOP_AFTER_UNIT:=fail;
INTERNAL_GUARD_MS:=1320000; START_UNIT:=1;
INITIAL_COUNTERS:=[0,0,0,0,0,0,0,0,0,0,0,0];
PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";
PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0;
PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";
CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD164_CHECKPOINT_GPT56SOL.txt";
CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD164_CHECKPOINT_TMP_GPT56SOL.txt";
EXPECTED_PROFILE_SHA256:="1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2";
EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard164_v7_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="C1B170D4FCC7FEA77E420BF330776F2CAEE316D6AE996C8D286DE46E8249FE87";
S164_RECORDS:=[
rec(k:=13163,first:=75,last:=96,unitFirst:=1,unitLast:=22,order:=24576,autOrder:=786432,parity:=7,classes:=96,raw:=2359296,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1419),
rec(k:=13164,first:=1,last:=716,unitFirst:=23,unitLast:=738,order:=24576,autOrder:=1572864,parity:=7,classes:=716,raw:=17596416,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1742),
rec(k:=13165,first:=1,last:=96,unitFirst:=739,unitLast:=834,order:=24576,autOrder:=393216,parity:=15,classes:=96,raw:=2359296,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1063),
rec(k:=13166,first:=1,last:=560,unitFirst:=835,unitLast:=1394,order:=24576,autOrder:=786432,parity:=15,classes:=560,raw:=13762560,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1258),
rec(k:=13167,first:=1,last:=84,unitFirst:=1395,unitLast:=1478,order:=24576,autOrder:=393216,parity:=3,classes:=84,raw:=2064384,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1613),
rec(k:=13168,first:=1,last:=44,unitFirst:=1479,unitLast:=1522,order:=24576,autOrder:=393216,parity:=3,classes:=44,raw:=1081344,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1565),
rec(k:=13169,first:=1,last:=84,unitFirst:=1523,unitLast:=1606,order:=24576,autOrder:=393216,parity:=3,classes:=84,raw:=2064384,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1938),
rec(k:=13170,first:=1,last:=64,unitFirst:=1607,unitLast:=1670,order:=24576,autOrder:=393216,parity:=3,classes:=64,raw:=1572864,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1684),
rec(k:=13171,first:=1,last:=161,unitFirst:=1671,unitLast:=1831,order:=24576,autOrder:=786432,parity:=3,classes:=470,raw:=11550720,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=2082)
];
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard164_v7_gpt56sol.g");
