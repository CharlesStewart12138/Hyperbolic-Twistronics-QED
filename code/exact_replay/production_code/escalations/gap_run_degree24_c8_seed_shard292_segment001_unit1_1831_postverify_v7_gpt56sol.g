# Exact wrapper for sealed degree-24 seed workload shard292.
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD292_SEGMENT001_UNIT1_1831_POSTVERIFY_V7_GPT56SOL.txt";
STOP_AFTER_UNIT:=fail;
INTERNAL_GUARD_MS:=1320000; START_UNIT:=1;
INITIAL_COUNTERS:=[0,0,0,0,0,0,0,0,0,0,0,0];
PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";
PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0;
PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";
CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD292_CHECKPOINT_GPT56SOL.txt";
CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD292_CHECKPOINT_TMP_GPT56SOL.txt";
EXPECTED_PROFILE_SHA256:="1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2";
EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard292_v7_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="7D39ED1011504B29DB85321D1B47E950D80E7EAD4B6BAB8EB15BD7B31D1BC3F4";
S292_RECORDS:=[
rec(k:=13910,first:=294,last:=1080,unitFirst:=1,unitLast:=787,order:=24576,autOrder:=3145728,parity:=7,classes:=1080,raw:=26542080,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=4031),
rec(k:=13911,first:=1,last:=592,unitFirst:=788,unitLast:=1379,order:=24576,autOrder:=3145728,parity:=7,classes:=592,raw:=14548992,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=3314),
rec(k:=13912,first:=1,last:=440,unitFirst:=1380,unitLast:=1819,order:=24576,autOrder:=196608,parity:=7,classes:=440,raw:=10813440,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1152),
rec(k:=13913,first:=1,last:=12,unitFirst:=1820,unitLast:=1831,order:=24576,autOrder:=786432,parity:=7,classes:=112,raw:=2752512,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1389)
];
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard292_v7_gpt56sol.g");
