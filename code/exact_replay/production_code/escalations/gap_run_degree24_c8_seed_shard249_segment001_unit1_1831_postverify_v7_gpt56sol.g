# Exact wrapper for sealed degree-24 seed workload shard249.
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD249_SEGMENT001_UNIT1_1831_POSTVERIFY_V7_GPT56SOL.txt";
STOP_AFTER_UNIT:=fail;
INTERNAL_GUARD_MS:=1320000; START_UNIT:=1;
INITIAL_COUNTERS:=[0,0,0,0,0,0,0,0,0,0,0,0];
PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";
PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0;
PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";
CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD249_CHECKPOINT_GPT56SOL.txt";
CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD249_CHECKPOINT_TMP_GPT56SOL.txt";
EXPECTED_PROFILE_SHA256:="1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2";
EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard249_v7_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="7BEC6449AE8525EDAFABF731828DB1EE9BF3D45ABC3F6E9EBC5D1D78E627A0F7";
S249_RECORDS:=[
rec(k:=13726,first:=436,last:=640,unitFirst:=1,unitLast:=205,order:=24576,autOrder:=786432,parity:=15,classes:=640,raw:=15728640,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=2064),
rec(k:=13727,first:=1,last:=144,unitFirst:=206,unitLast:=349,order:=24576,autOrder:=393216,parity:=15,classes:=144,raw:=3538944,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1231),
rec(k:=13728,first:=1,last:=344,unitFirst:=350,unitLast:=693,order:=24576,autOrder:=786432,parity:=15,classes:=344,raw:=8454144,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1884),
rec(k:=13729,first:=1,last:=384,unitFirst:=694,unitLast:=1077,order:=24576,autOrder:=393216,parity:=15,classes:=384,raw:=9437184,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1847),
rec(k:=13730,first:=1,last:=752,unitFirst:=1078,unitLast:=1829,order:=24576,autOrder:=1572864,parity:=15,classes:=752,raw:=18481152,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=2469),
rec(k:=13731,first:=1,last:=2,unitFirst:=1830,unitLast:=1831,order:=24576,autOrder:=786432,parity:=15,classes:=960,raw:=23592960,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=3290)
];
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard249_v7_gpt56sol.g");
