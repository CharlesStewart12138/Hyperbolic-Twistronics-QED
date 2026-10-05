# Exact wrapper for sealed degree-24 seed workload shard160.
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD160_SEGMENT001_UNIT1_1831_POSTVERIFY_V7_GPT56SOL.txt";
STOP_AFTER_UNIT:=fail;
INTERNAL_GUARD_MS:=1320000; START_UNIT:=1;
INITIAL_COUNTERS:=[0,0,0,0,0,0,0,0,0,0,0,0];
PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";
PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0;
PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";
CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD160_CHECKPOINT_GPT56SOL.txt";
CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD160_CHECKPOINT_TMP_GPT56SOL.txt";
EXPECTED_PROFILE_SHA256:="1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2";
EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard160_v7_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="C42A4644FACE6276F9DCA65656118720A3B6A4882C8E16C12A6F76EFC60DB5ED";
S160_RECORDS:=[
rec(k:=13134,first:=769,last:=815,unitFirst:=1,unitLast:=47,order:=24576,autOrder:=3145728,parity:=15,classes:=815,raw:=20029440,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=3127),
rec(k:=13135,first:=1,last:=64,unitFirst:=48,unitLast:=111,order:=24576,autOrder:=98304,parity:=3,classes:=64,raw:=1572864,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=835),
rec(k:=13136,first:=1,last:=407,unitFirst:=112,unitLast:=518,order:=24576,autOrder:=6291456,parity:=15,classes:=407,raw:=10002432,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=2327),
rec(k:=13137,first:=1,last:=675,unitFirst:=519,unitLast:=1193,order:=24576,autOrder:=18874368,parity:=15,classes:=675,raw:=16588800,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=2481),
rec(k:=13138,first:=1,last:=472,unitFirst:=1194,unitLast:=1665,order:=24576,autOrder:=3145728,parity:=15,classes:=472,raw:=11599872,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=4996),
rec(k:=13139,first:=1,last:=120,unitFirst:=1666,unitLast:=1785,order:=24576,autOrder:=9437184,parity:=15,classes:=120,raw:=2949120,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=2226),
rec(k:=13140,first:=1,last:=46,unitFirst:=1786,unitLast:=1831,order:=24576,autOrder:=12582912,parity:=15,classes:=403,raw:=9904128,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=3255)
];
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard160_v7_gpt56sol.g");
