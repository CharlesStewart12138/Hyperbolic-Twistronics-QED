# Exact wrapper for sealed degree-24 seed workload shard237.
OUT:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD237_SEGMENT001_UNIT1_1831_POSTVERIFY_V7_GPT56SOL.txt";
STOP_AFTER_UNIT:=fail;
INTERNAL_GUARD_MS:=1320000; START_UNIT:=1;
INITIAL_COUNTERS:=[0,0,0,0,0,0,0,0,0,0,0,0];
PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";
PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0;
PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";
CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD237_CHECKPOINT_GPT56SOL.txt";
CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_SHARD237_CHECKPOINT_TMP_GPT56SOL.txt";
EXPECTED_PROFILE_SHA256:="1D1A363463C8A0EFACD59EB5220555E7ADD2BD6AD4F686CC1CED9653706A70D2";
EXPECTED_PLAN_SHA256:="0CBD0E7205976B7634A09FFA567A515259C1F2A087004680D32B9ADAB87B67C2";
PROFILE_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_FULL_MERGED_GPT56SOL.txt";
PLAN_FILE:="/mnt/d/work/revise/production_code/escalations/GAP_TRANSITIVE_DEGREE24_C8_SEED_WORKLOAD_PLAN_GPT56SOL.tsv";
ENGINE_FILE:="/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard237_v7_gpt56sol.g";
EXPECTED_ENGINE_SHA256:="05B41DBAFBED883281BEA201FA37FF3776698D10204DDEF4266CFF4299A5C513";
S237_RECORDS:=[
rec(k:=13662,first:=1593,last:=1700,unitFirst:=1,unitLast:=108,order:=24576,autOrder:=50331648,parity:=3,classes:=1700,raw:=41779200,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=5832),
rec(k:=13663,first:=1,last:=560,unitFirst:=109,unitLast:=668,order:=24576,autOrder:=6291456,parity:=3,classes:=560,raw:=13762560,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=2539),
rec(k:=13664,first:=1,last:=816,unitFirst:=669,unitLast:=1484,order:=24576,autOrder:=1572864,parity:=1,classes:=816,raw:=20054016,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=2719),
rec(k:=13665,first:=1,last:=347,unitFirst:=1485,unitLast:=1831,order:=24576,autOrder:=786432,parity:=3,classes:=348,raw:=8552448,method:="pc",representation:="pc_transport",pcOrder:=24576,profileMs:=1348)
];
Read("/mnt/d/work/revise/production_code/escalations/gap_transitive_degree24_c8_seed_plan_alpha_checkpoint_shard237_v7_gpt56sol.g");
