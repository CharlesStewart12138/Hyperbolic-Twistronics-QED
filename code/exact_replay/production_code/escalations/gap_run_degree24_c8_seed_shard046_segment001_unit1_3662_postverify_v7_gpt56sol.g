# Exact wrapper for sealed degree-24 seed workload shard046.
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD046_SEGMENT001_UNIT1_3662_POSTVERIFY_V7_GPT56SOL.txt";
STOP_AFTER_UNIT:=fail;
INTERNAL_GUARD_MS:=1320000; START_UNIT:=1;
INITIAL_COUNTERS:=[0,0,0,0,0,0,0,0,0,0,0,0];
PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";
PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0;
PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";
CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD046_CHECKPOINT_GPT56SOL.txt";
CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD046_CHECKPOINT_TMP_GPT56SOL.txt";
EXPECTED_PROFILE_SHA256:="1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2";
EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard046_v7_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="46DD618A76395ECF6A56C027A8E249E8012D8422211C1716396B857690214BF6";
S046_RECORDS:=[
rec(k:=10728,first:=30,last:=256,unitFirst:=1,unitLast:=227,order:=12288,autOrder:=786432,parity:=7,classes:=256,raw:=3145728,method:="pc",representation:="legacy_sealed_pc",pcOrder:=12288,profileMs:=2896),
rec(k:=10729,first:=1,last:=344,unitFirst:=228,unitLast:=571,order:=12288,autOrder:=1572864,parity:=7,classes:=344,raw:=4227072,method:="pc",representation:="legacy_sealed_pc",pcOrder:=12288,profileMs:=2664),
rec(k:=10730,first:=1,last:=344,unitFirst:=572,unitLast:=915,order:=12288,autOrder:=1572864,parity:=7,classes:=344,raw:=4227072,method:="pc",representation:="legacy_sealed_pc",pcOrder:=12288,profileMs:=2761),
rec(k:=10731,first:=1,last:=344,unitFirst:=916,unitLast:=1259,order:=12288,autOrder:=1572864,parity:=7,classes:=344,raw:=4227072,method:="pc",representation:="legacy_sealed_pc",pcOrder:=12288,profileMs:=3031),
rec(k:=10732,first:=1,last:=512,unitFirst:=1260,unitLast:=1771,order:=12288,autOrder:=1572864,parity:=7,classes:=512,raw:=6291456,method:="pc",representation:="legacy_sealed_pc",pcOrder:=12288,profileMs:=2200),
rec(k:=10733,first:=1,last:=112,unitFirst:=1772,unitLast:=1883,order:=12288,autOrder:=786432,parity:=7,classes:=112,raw:=1376256,method:="pc",representation:="legacy_sealed_pc",pcOrder:=12288,profileMs:=2835),
rec(k:=10735,first:=1,last:=120,unitFirst:=1884,unitLast:=2003,order:=12288,autOrder:=1572864,parity:=7,classes:=120,raw:=1474560,method:="pc",representation:="legacy_sealed_pc",pcOrder:=12288,profileMs:=2129),
rec(k:=10736,first:=1,last:=112,unitFirst:=2004,unitLast:=2115,order:=12288,autOrder:=786432,parity:=7,classes:=112,raw:=1376256,method:="pc",representation:="legacy_sealed_pc",pcOrder:=12288,profileMs:=2744),
rec(k:=10737,first:=1,last:=112,unitFirst:=2116,unitLast:=2227,order:=12288,autOrder:=786432,parity:=7,classes:=112,raw:=1376256,method:="pc",representation:="legacy_sealed_pc",pcOrder:=12288,profileMs:=2658),
rec(k:=10738,first:=1,last:=720,unitFirst:=2228,unitLast:=2947,order:=12288,autOrder:=3145728,parity:=7,classes:=720,raw:=8847360,method:="pc",representation:="legacy_sealed_pc",pcOrder:=12288,profileMs:=2918),
rec(k:=10739,first:=1,last:=184,unitFirst:=2948,unitLast:=3131,order:=12288,autOrder:=1572864,parity:=7,classes:=184,raw:=2260992,method:="pc",representation:="legacy_sealed_pc",pcOrder:=12288,profileMs:=2124),
rec(k:=10740,first:=1,last:=148,unitFirst:=3132,unitLast:=3279,order:=12288,autOrder:=393216,parity:=3,classes:=148,raw:=1818624,method:="pc",representation:="legacy_sealed_pc",pcOrder:=12288,profileMs:=861),
rec(k:=10741,first:=1,last:=96,unitFirst:=3280,unitLast:=3375,order:=12288,autOrder:=786432,parity:=3,classes:=96,raw:=1179648,method:="pc",representation:="legacy_sealed_pc",pcOrder:=12288,profileMs:=700),
rec(k:=10743,first:=1,last:=122,unitFirst:=3376,unitLast:=3497,order:=12288,autOrder:=393216,parity:=3,classes:=122,raw:=1499136,method:="pc",representation:="legacy_sealed_pc",pcOrder:=12288,profileMs:=893),
rec(k:=10744,first:=1,last:=165,unitFirst:=3498,unitLast:=3662,order:=12288,autOrder:=393216,parity:=3,classes:=368,raw:=4521984,method:="pc",representation:="legacy_sealed_pc",pcOrder:=12288,profileMs:=966)
];
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard046_v7_gpt56sol.g");
