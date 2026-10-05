# Exact wrapper for sealed degree-24 seed workload shard253.
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD253_SEGMENT001_UNIT1_1831_POSTVERIFY_V7_GPT56SOL.txt";
STOP_AFTER_UNIT:=fail;
INTERNAL_GUARD_MS:=1320000; START_UNIT:=1;
INITIAL_COUNTERS:=[0,0,0,0,0,0,0,0,0,0,0,0];
PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";
PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0;
PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";
CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD253_CHECKPOINT_GPT56SOL.txt";
CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD253_CHECKPOINT_TMP_GPT56SOL.txt";
EXPECTED_PROFILE_SHA256:="1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2";
EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard253_v7_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="2C1B53BD2EB6BABF55BA1B2669FF96663AA3D2CBF9CECA3C9F7C93990C2A733B";
S253_RECORDS:=[
rec(k:=13742,first:=428,last:=712,unitFirst:=1,unitLast:=285,order:=24576,autOrder:=1572864,parity:=1,classes:=712,raw:=17498112,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=2265),
rec(k:=13743,first:=1,last:=991,unitFirst:=286,unitLast:=1276,order:=24576,autOrder:=3145728,parity:=1,classes:=991,raw:=24354816,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=2539),
rec(k:=13744,first:=1,last:=356,unitFirst:=1277,unitLast:=1632,order:=24576,autOrder:=393216,parity:=1,classes:=356,raw:=8749056,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1133),
rec(k:=13745,first:=1,last:=199,unitFirst:=1633,unitLast:=1831,order:=24576,autOrder:=786432,parity:=1,classes:=428,raw:=10518528,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1314)
];
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard253_v7_gpt56sol.g");
