# Exact wrapper for sealed degree-24 seed workload shard137.
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD137_SEGMENT001_UNIT1_1831_POSTVERIFY_V7_GPT56SOL.txt";
STOP_AFTER_UNIT:=fail;
INTERNAL_GUARD_MS:=1320000; START_UNIT:=1;
INITIAL_COUNTERS:=[0,0,0,0,0,0,0,0,0,0,0,0];
PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";
PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0;
PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";
CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD137_CHECKPOINT_GPT56SOL.txt";
CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD137_CHECKPOINT_TMP_GPT56SOL.txt";
EXPECTED_PROFILE_SHA256:="1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2";
EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard137_v7_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="2C3D9932E6F4E8B090AB79F48B077D40FD58EA744634D2E20DC1BBF2B71ED358";
S137_RECORDS:=[
rec(k:=12934,first:=164,last:=256,unitFirst:=1,unitLast:=93,order:=24576,autOrder:=75497472,parity:=3,classes:=256,raw:=6291456,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=3593),
rec(k:=12935,first:=1,last:=176,unitFirst:=94,unitLast:=269,order:=24576,autOrder:=1572864,parity:=7,classes:=176,raw:=4325376,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1157),
rec(k:=12936,first:=1,last:=104,unitFirst:=270,unitLast:=373,order:=24576,autOrder:=1572864,parity:=1,classes:=104,raw:=2555904,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1361),
rec(k:=12937,first:=1,last:=380,unitFirst:=374,unitLast:=753,order:=24576,autOrder:=3145728,parity:=1,classes:=380,raw:=9338880,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=2057),
rec(k:=12938,first:=1,last:=156,unitFirst:=754,unitLast:=909,order:=24576,autOrder:=786432,parity:=15,classes:=156,raw:=3833856,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1397),
rec(k:=12939,first:=1,last:=384,unitFirst:=910,unitLast:=1293,order:=24576,autOrder:=393216,parity:=15,classes:=384,raw:=9437184,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1970),
rec(k:=12940,first:=1,last:=366,unitFirst:=1294,unitLast:=1659,order:=24576,autOrder:=1572864,parity:=3,classes:=366,raw:=8994816,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1581),
rec(k:=12941,first:=1,last:=158,unitFirst:=1660,unitLast:=1817,order:=24576,autOrder:=786432,parity:=3,classes:=158,raw:=3883008,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1793),
rec(k:=12942,first:=1,last:=14,unitFirst:=1818,unitLast:=1831,order:=24576,autOrder:=786432,parity:=3,classes:=592,raw:=14548992,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1686)
];
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard137_v7_gpt56sol.g");
