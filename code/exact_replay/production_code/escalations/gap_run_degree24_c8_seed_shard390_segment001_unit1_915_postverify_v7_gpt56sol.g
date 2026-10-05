# Exact wrapper for sealed degree-24 seed workload shard390.
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD390_SEGMENT001_UNIT1_915_POSTVERIFY_V7_GPT56SOL.txt";
STOP_AFTER_UNIT:=fail;
INTERNAL_GUARD_MS:=1320000; START_UNIT:=1;
INITIAL_COUNTERS:=[0,0,0,0,0,0,0,0,0,0,0,0];
PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";
PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0;
PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";
CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD390_CHECKPOINT_GPT56SOL.txt";
CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD390_CHECKPOINT_TMP_GPT56SOL.txt";
EXPECTED_PROFILE_SHA256:="1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2";
EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard390_v7_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="6F7E1116D13D7A313F67AEB679AC3965F64BC772922EBC4CA1C0BE83943E09FA";
S390_RECORDS:=[
rec(k:=15005,first:=68,last:=206,unitFirst:=1,unitLast:=139,order:=49152,autOrder:=9437184,parity:=3,classes:=206,raw:=10125312,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1799),
rec(k:=15006,first:=1,last:=96,unitFirst:=140,unitLast:=235,order:=49152,autOrder:=4718592,parity:=3,classes:=96,raw:=4718592,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1462),
rec(k:=15007,first:=1,last:=96,unitFirst:=236,unitLast:=331,order:=49152,autOrder:=1572864,parity:=7,classes:=96,raw:=4718592,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1592),
rec(k:=15008,first:=1,last:=64,unitFirst:=332,unitLast:=395,order:=49152,autOrder:=1572864,parity:=7,classes:=64,raw:=3145728,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1834),
rec(k:=15009,first:=1,last:=160,unitFirst:=396,unitLast:=555,order:=49152,autOrder:=393216,parity:=7,classes:=160,raw:=7864320,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=1183),
rec(k:=15010,first:=1,last:=96,unitFirst:=556,unitLast:=651,order:=49152,autOrder:=1572864,parity:=3,classes:=96,raw:=4718592,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=2623),
rec(k:=15011,first:=1,last:=264,unitFirst:=652,unitLast:=915,order:=49152,autOrder:=3145728,parity:=7,classes:=272,raw:=13369344,method:="pc",representation:="pc_transport",pcOrder:=49152,profileMs:=2453)
];
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard390_v7_gpt56sol.g");
