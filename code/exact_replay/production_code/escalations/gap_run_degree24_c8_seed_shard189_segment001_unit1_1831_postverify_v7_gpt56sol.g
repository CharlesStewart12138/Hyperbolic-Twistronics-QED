# Exact wrapper for sealed degree-24 seed workload shard189.
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD189_SEGMENT001_UNIT1_1831_POSTVERIFY_V7_GPT56SOL.txt";
STOP_AFTER_UNIT:=fail;
INTERNAL_GUARD_MS:=1320000; START_UNIT:=1;
INITIAL_COUNTERS:=[0,0,0,0,0,0,0,0,0,0,0,0];
PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";
PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0;
PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";
CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD189_CHECKPOINT_GPT56SOL.txt";
CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD189_CHECKPOINT_TMP_GPT56SOL.txt";
EXPECTED_PROFILE_SHA256:="1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2";
EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard189_v7_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="32530809BBF0B8709D53C23563BEB0D02231E6E1F5BE91265293E0DC91639767";
S189_RECORDS:=[
rec(k:=13393,first:=473,last:=576,unitFirst:=1,unitLast:=104,order:=24576,autOrder:=393216,parity:=7,classes:=576,raw:=14155776,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1537),
rec(k:=13394,first:=1,last:=528,unitFirst:=105,unitLast:=632,order:=24576,autOrder:=786432,parity:=7,classes:=528,raw:=12976128,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1156),
rec(k:=13395,first:=1,last:=860,unitFirst:=633,unitLast:=1492,order:=24576,autOrder:=1572864,parity:=15,classes:=860,raw:=21135360,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=2143),
rec(k:=13396,first:=1,last:=120,unitFirst:=1493,unitLast:=1612,order:=24576,autOrder:=786432,parity:=7,classes:=120,raw:=2949120,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1396),
rec(k:=13397,first:=1,last:=128,unitFirst:=1613,unitLast:=1740,order:=24576,autOrder:=393216,parity:=7,classes:=128,raw:=3145728,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1946),
rec(k:=13398,first:=1,last:=91,unitFirst:=1741,unitLast:=1831,order:=24576,autOrder:=393216,parity:=7,classes:=128,raw:=3145728,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1769)
];
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard189_v7_gpt56sol.g");
