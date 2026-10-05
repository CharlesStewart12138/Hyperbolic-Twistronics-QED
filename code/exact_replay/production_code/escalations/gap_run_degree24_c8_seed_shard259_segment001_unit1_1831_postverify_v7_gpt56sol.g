# Exact wrapper for sealed degree-24 seed workload shard259.
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD259_SEGMENT001_UNIT1_1831_POSTVERIFY_V7_GPT56SOL.txt";
STOP_AFTER_UNIT:=fail;
INTERNAL_GUARD_MS:=1320000; START_UNIT:=1;
INITIAL_COUNTERS:=[0,0,0,0,0,0,0,0,0,0,0,0];
PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";
PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0;
PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";
CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD259_CHECKPOINT_GPT56SOL.txt";
CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD259_CHECKPOINT_TMP_GPT56SOL.txt";
EXPECTED_PROFILE_SHA256:="1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2";
EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard259_v7_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="7D459B834FF9286783FE54F841DF6803B443D82B1463D3BDF0354147F52B2696";
S259_RECORDS:=[
rec(k:=13769,first:=372,last:=384,unitFirst:=1,unitLast:=13,order:=24576,autOrder:=196608,parity:=7,classes:=384,raw:=9437184,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1170),
rec(k:=13770,first:=1,last:=384,unitFirst:=14,unitLast:=397,order:=24576,autOrder:=196608,parity:=7,classes:=384,raw:=9437184,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1185),
rec(k:=13771,first:=1,last:=384,unitFirst:=398,unitLast:=781,order:=24576,autOrder:=196608,parity:=7,classes:=384,raw:=9437184,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1243),
rec(k:=13772,first:=1,last:=800,unitFirst:=782,unitLast:=1581,order:=24576,autOrder:=393216,parity:=7,classes:=800,raw:=19660800,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1908),
rec(k:=13773,first:=1,last:=250,unitFirst:=1582,unitLast:=1831,order:=24576,autOrder:=393216,parity:=7,classes:=800,raw:=19660800,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1856)
];
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard259_v7_gpt56sol.g");
