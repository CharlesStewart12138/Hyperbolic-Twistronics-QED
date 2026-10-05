# Exact wrapper for sealed degree-24 seed workload shard222.
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD222_SEGMENT001_UNIT1_1831_POSTVERIFY_V7_GPT56SOL.txt";
STOP_AFTER_UNIT:=fail;
INTERNAL_GUARD_MS:=1320000; START_UNIT:=1;
INITIAL_COUNTERS:=[0,0,0,0,0,0,0,0,0,0,0,0];
PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";
PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0;
PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";
CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD222_CHECKPOINT_GPT56SOL.txt";
CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD222_CHECKPOINT_TMP_GPT56SOL.txt";
EXPECTED_PROFILE_SHA256:="1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2";
EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard222_v7_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="1B6C796CBA957487073B72D7F2E459AE2449B7A894ABD3613BE8DCC3DD22D738";
S222_RECORDS:=[
rec(k:=13573,first:=209,last:=600,unitFirst:=1,unitLast:=392,order:=24576,autOrder:=786432,parity:=3,classes:=600,raw:=14745600,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1732),
rec(k:=13574,first:=1,last:=120,unitFirst:=393,unitLast:=512,order:=24576,autOrder:=786432,parity:=7,classes:=120,raw:=2949120,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1769),
rec(k:=13575,first:=1,last:=72,unitFirst:=513,unitLast:=584,order:=24576,autOrder:=393216,parity:=3,classes:=72,raw:=1769472,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=903),
rec(k:=13576,first:=1,last:=544,unitFirst:=585,unitLast:=1128,order:=24576,autOrder:=393216,parity:=7,classes:=544,raw:=13369344,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1975),
rec(k:=13577,first:=1,last:=540,unitFirst:=1129,unitLast:=1668,order:=24576,autOrder:=786432,parity:=3,classes:=540,raw:=13271040,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1177),
rec(k:=13578,first:=1,last:=116,unitFirst:=1669,unitLast:=1784,order:=24576,autOrder:=786432,parity:=3,classes:=116,raw:=2850816,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1311),
rec(k:=13579,first:=1,last:=47,unitFirst:=1785,unitLast:=1831,order:=24576,autOrder:=393216,parity:=3,classes:=92,raw:=2260992,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=919)
];
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard222_v7_gpt56sol.g");
