# Exact wrapper for sealed degree-24 seed workload shard278.
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD278_SEGMENT001_UNIT1_1831_POSTVERIFY_V7_GPT56SOL.txt";
STOP_AFTER_UNIT:=fail;
INTERNAL_GUARD_MS:=1320000; START_UNIT:=1;
INITIAL_COUNTERS:=[0,0,0,0,0,0,0,0,0,0,0,0];
PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";
PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0;
PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";
CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD278_CHECKPOINT_GPT56SOL.txt";
CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD278_CHECKPOINT_TMP_GPT56SOL.txt";
EXPECTED_PROFILE_SHA256:="1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2";
EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard278_v7_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="F9CE0BC1619FEC069AB9212421144E2ED1DAA039ADF9DAB7475821F040EFA35C";
S278_RECORDS:=[
rec(k:=13835,first:=61,last:=128,unitFirst:=1,unitLast:=68,order:=24576,autOrder:=393216,parity:=7,classes:=128,raw:=3145728,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1306),
rec(k:=13836,first:=1,last:=128,unitFirst:=69,unitLast:=196,order:=24576,autOrder:=393216,parity:=7,classes:=128,raw:=3145728,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1030),
rec(k:=13837,first:=1,last:=308,unitFirst:=197,unitLast:=504,order:=24576,autOrder:=18874368,parity:=15,classes:=308,raw:=7569408,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1781),
rec(k:=13838,first:=1,last:=308,unitFirst:=505,unitLast:=812,order:=24576,autOrder:=18874368,parity:=7,classes:=308,raw:=7569408,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1911),
rec(k:=13839,first:=1,last:=308,unitFirst:=813,unitLast:=1120,order:=24576,autOrder:=18874368,parity:=7,classes:=308,raw:=7569408,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=3586),
rec(k:=13840,first:=1,last:=308,unitFirst:=1121,unitLast:=1428,order:=24576,autOrder:=18874368,parity:=7,classes:=308,raw:=7569408,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1608),
rec(k:=13841,first:=1,last:=192,unitFirst:=1429,unitLast:=1620,order:=24576,autOrder:=393216,parity:=7,classes:=192,raw:=4718592,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1218),
rec(k:=13842,first:=1,last:=192,unitFirst:=1621,unitLast:=1812,order:=24576,autOrder:=393216,parity:=7,classes:=192,raw:=4718592,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1125),
rec(k:=13843,first:=1,last:=19,unitFirst:=1813,unitLast:=1831,order:=24576,autOrder:=393216,parity:=7,classes:=192,raw:=4718592,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1185)
];
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard278_v7_gpt56sol.g");
