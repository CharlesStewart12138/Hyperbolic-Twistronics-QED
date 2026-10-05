# Exact wrapper for sealed degree-24 seed workload shard107.
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD107_SEGMENT001_UNIT1_3662_POSTVERIFY_V7_GPT56SOL.txt";
STOP_AFTER_UNIT:=fail;
INTERNAL_GUARD_MS:=1320000; START_UNIT:=1;
INITIAL_COUNTERS:=[0,0,0,0,0,0,0,0,0,0,0,0];
PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";
PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0;
PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";
CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD107_CHECKPOINT_GPT56SOL.txt";
CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD107_CHECKPOINT_TMP_GPT56SOL.txt";
EXPECTED_PROFILE_SHA256:="1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2";
EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard107_v7_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="8423D887C6162EAF5D3A0EF54A67197EF0E4C9C413122D9352D0441CADF5A9C1";
S107_RECORDS:=[
rec(k:=11968,first:=69,last:=396,unitFirst:=1,unitLast:=328,order:=12288,autOrder:=12582912,parity:=3,classes:=396,raw:=4866048,method:="pc",representation:="pc_transport",pcOrder:=12288,profileMs:=5790),
rec(k:=11969,first:=1,last:=460,unitFirst:=329,unitLast:=788,order:=12288,autOrder:=301989888,parity:=7,classes:=460,raw:=5652480,method:="pc",representation:="pc_transport",pcOrder:=12288,profileMs:=2501),
rec(k:=11970,first:=1,last:=48,unitFirst:=789,unitLast:=836,order:=12288,autOrder:=6291456,parity:=3,classes:=48,raw:=589824,method:="pc",representation:="pc_transport",pcOrder:=12288,profileMs:=9203),
rec(k:=11971,first:=1,last:=414,unitFirst:=837,unitLast:=1250,order:=12288,autOrder:=25165824,parity:=3,classes:=414,raw:=5087232,method:="pc",representation:="pc_transport",pcOrder:=12288,profileMs:=3831),
rec(k:=11972,first:=1,last:=384,unitFirst:=1251,unitLast:=1634,order:=12288,autOrder:=12582912,parity:=3,classes:=384,raw:=4718592,method:="pc",representation:="pc_transport",pcOrder:=12288,profileMs:=4124),
rec(k:=11973,first:=1,last:=630,unitFirst:=1635,unitLast:=2264,order:=12288,autOrder:=25165824,parity:=7,classes:=630,raw:=7741440,method:="pc",representation:="pc_transport",pcOrder:=12288,profileMs:=7434),
rec(k:=11974,first:=1,last:=640,unitFirst:=2265,unitLast:=2904,order:=12288,autOrder:=196608,parity:=3,classes:=640,raw:=7864320,method:="pc",representation:="pc_transport",pcOrder:=12288,profileMs:=1588),
rec(k:=11975,first:=1,last:=640,unitFirst:=2905,unitLast:=3544,order:=12288,autOrder:=196608,parity:=3,classes:=640,raw:=7864320,method:="pc",representation:="pc_transport",pcOrder:=12288,profileMs:=1725),
rec(k:=11976,first:=1,last:=118,unitFirst:=3545,unitLast:=3662,order:=12288,autOrder:=196608,parity:=3,classes:=640,raw:=7864320,method:="pc",representation:="pc_transport",pcOrder:=12288,profileMs:=1447)
];
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard107_v7_gpt56sol.g");
