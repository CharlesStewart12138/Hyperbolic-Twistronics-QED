# Exact wrapper for sealed degree-24 seed workload shard235.
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD235_SEGMENT001_UNIT1_1831_POSTVERIFY_V7_GPT56SOL.txt";
STOP_AFTER_UNIT:=fail;
INTERNAL_GUARD_MS:=1320000; START_UNIT:=1;
INITIAL_COUNTERS:=[0,0,0,0,0,0,0,0,0,0,0,0];
PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";
PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0;
PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";
CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD235_CHECKPOINT_GPT56SOL.txt";
CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD235_CHECKPOINT_TMP_GPT56SOL.txt";
EXPECTED_PROFILE_SHA256:="1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2";
EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard235_v7_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="95C882C56F5EF06BDE14BFA876BC3B7A9520A256E686224D3E900D928421EC1F";
S235_RECORDS:=[
rec(k:=13655,first:=104,last:=144,unitFirst:=1,unitLast:=41,order:=24576,autOrder:=393216,parity:=7,classes:=144,raw:=3538944,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1504),
rec(k:=13656,first:=1,last:=230,unitFirst:=42,unitLast:=271,order:=24576,autOrder:=28311552,parity:=15,classes:=230,raw:=5652480,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1859),
rec(k:=13657,first:=1,last:=72,unitFirst:=272,unitLast:=343,order:=24576,autOrder:=1179648,parity:=3,classes:=72,raw:=1769472,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=925),
rec(k:=13658,first:=1,last:=472,unitFirst:=344,unitLast:=815,order:=24576,autOrder:=3145728,parity:=15,classes:=472,raw:=11599872,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=5039),
rec(k:=13659,first:=1,last:=120,unitFirst:=816,unitLast:=935,order:=24576,autOrder:=9437184,parity:=15,classes:=120,raw:=2949120,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1796),
rec(k:=13660,first:=1,last:=728,unitFirst:=936,unitLast:=1663,order:=24576,autOrder:=4718592,parity:=3,classes:=728,raw:=17891328,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1752),
rec(k:=13661,first:=1,last:=168,unitFirst:=1664,unitLast:=1831,order:=24576,autOrder:=6291456,parity:=15,classes:=407,raw:=10002432,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=2975)
];
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard235_v7_gpt56sol.g");
