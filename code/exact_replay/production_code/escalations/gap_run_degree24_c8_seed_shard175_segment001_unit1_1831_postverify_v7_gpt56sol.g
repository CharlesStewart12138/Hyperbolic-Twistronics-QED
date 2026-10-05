# Exact wrapper for sealed degree-24 seed workload shard175.
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD175_SEGMENT001_UNIT1_1831_POSTVERIFY_V7_GPT56SOL.txt";
STOP_AFTER_UNIT:=fail;
INTERNAL_GUARD_MS:=1320000; START_UNIT:=1;
INITIAL_COUNTERS:=[0,0,0,0,0,0,0,0,0,0,0,0];
PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";
PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0;
PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";
CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD175_CHECKPOINT_GPT56SOL.txt";
CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD175_CHECKPOINT_TMP_GPT56SOL.txt";
EXPECTED_PROFILE_SHA256:="1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2";
EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard175_v7_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="36ED3E1CB8EE777AD2544557CB02848EEE98C42408CAD8BC6FEE4B6E5C1883AE";
S175_RECORDS:=[
rec(k:=13270,first:=7,last:=108,unitFirst:=1,unitLast:=102,order:=24576,autOrder:=393216,parity:=3,classes:=108,raw:=2654208,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1749),
rec(k:=13271,first:=1,last:=128,unitFirst:=103,unitLast:=230,order:=24576,autOrder:=393216,parity:=3,classes:=128,raw:=3145728,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1473),
rec(k:=13272,first:=1,last:=240,unitFirst:=231,unitLast:=470,order:=24576,autOrder:=393216,parity:=15,classes:=240,raw:=5898240,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1583),
rec(k:=13273,first:=1,last:=136,unitFirst:=471,unitLast:=606,order:=24576,autOrder:=786432,parity:=7,classes:=136,raw:=3342336,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1253),
rec(k:=13274,first:=1,last:=164,unitFirst:=607,unitLast:=770,order:=24576,autOrder:=786432,parity:=7,classes:=164,raw:=4030464,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1489),
rec(k:=13275,first:=1,last:=156,unitFirst:=771,unitLast:=926,order:=24576,autOrder:=786432,parity:=7,classes:=156,raw:=3833856,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=983),
rec(k:=13276,first:=1,last:=184,unitFirst:=927,unitLast:=1110,order:=24576,autOrder:=786432,parity:=7,classes:=184,raw:=4521984,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1697),
rec(k:=13277,first:=1,last:=132,unitFirst:=1111,unitLast:=1242,order:=24576,autOrder:=786432,parity:=7,classes:=132,raw:=3244032,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=991),
rec(k:=13278,first:=1,last:=176,unitFirst:=1243,unitLast:=1418,order:=24576,autOrder:=786432,parity:=7,classes:=176,raw:=4325376,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1076),
rec(k:=13279,first:=1,last:=168,unitFirst:=1419,unitLast:=1586,order:=24576,autOrder:=786432,parity:=7,classes:=168,raw:=4128768,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1123),
rec(k:=13280,first:=1,last:=180,unitFirst:=1587,unitLast:=1766,order:=24576,autOrder:=786432,parity:=7,classes:=180,raw:=4423680,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1313),
rec(k:=13281,first:=1,last:=65,unitFirst:=1767,unitLast:=1831,order:=24576,autOrder:=786432,parity:=15,classes:=120,raw:=2949120,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=875)
];
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard175_v7_gpt56sol.g");
