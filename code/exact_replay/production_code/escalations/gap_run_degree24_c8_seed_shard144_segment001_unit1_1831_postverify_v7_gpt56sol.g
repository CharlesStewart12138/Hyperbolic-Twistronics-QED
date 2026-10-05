# Exact wrapper for sealed degree-24 seed workload shard144.
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD144_SEGMENT001_UNIT1_1831_POSTVERIFY_V7_GPT56SOL.txt";
STOP_AFTER_UNIT:=fail;
INTERNAL_GUARD_MS:=1320000; START_UNIT:=1;
INITIAL_COUNTERS:=[0,0,0,0,0,0,0,0,0,0,0,0];
PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";
PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0;
PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";
CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD144_CHECKPOINT_GPT56SOL.txt";
CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD144_CHECKPOINT_TMP_GPT56SOL.txt";
EXPECTED_PROFILE_SHA256:="1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2";
EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard144_v7_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="D21EC8391BFB4464D690536B8A4DDA18342611AC6BDEAEA4E53F212DFF0FCECC";
S144_RECORDS:=[
rec(k:=12991,first:=21,last:=142,unitFirst:=1,unitLast:=122,order:=24576,autOrder:=6291456,parity:=1,classes:=142,raw:=3489792,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=2061),
rec(k:=12992,first:=1,last:=490,unitFirst:=123,unitLast:=612,order:=24576,autOrder:=3145728,parity:=7,classes:=490,raw:=12042240,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1919),
rec(k:=12993,first:=1,last:=640,unitFirst:=613,unitLast:=1252,order:=24576,autOrder:=786432,parity:=15,classes:=640,raw:=15728640,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=2232),
rec(k:=12994,first:=1,last:=144,unitFirst:=1253,unitLast:=1396,order:=24576,autOrder:=786432,parity:=15,classes:=144,raw:=3538944,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=2135),
rec(k:=12995,first:=1,last:=137,unitFirst:=1397,unitLast:=1533,order:=24576,autOrder:=1572864,parity:=1,classes:=137,raw:=3366912,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1047),
rec(k:=12996,first:=1,last:=298,unitFirst:=1534,unitLast:=1831,order:=24576,autOrder:=6291456,parity:=3,classes:=560,raw:=13762560,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1386)
];
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard144_v7_gpt56sol.g");
