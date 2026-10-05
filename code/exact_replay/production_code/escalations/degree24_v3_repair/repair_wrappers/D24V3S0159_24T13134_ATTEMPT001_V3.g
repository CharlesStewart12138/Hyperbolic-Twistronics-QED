SEGMENT_FILE:="/mnt/d/work/revise/production_code/escalations/degree24_v3_repair/repair_plan_segments/D24V3S0159_24T13134.g"; EXPECTED_SEGMENT_FILE_SHA256:="ecebe16bdf6707290b9a152baaf6a9cc529328103a35b724b2c206b98fb8e5c5";
OUT:="/mnt/d/work/revise/production_code/escalations/degree24_v3_repair/repair_outputs/D24V3S0159_24T13134_ATTEMPT001_V3.txt"; CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/degree24_v3_repair/repair_checkpoints/D24V3S0159_24T13134_CHECKPOINT_V3.txt"; CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/degree24_v3_repair/repair_checkpoints/D24V3S0159_24T13134_CHECKPOINT_TMP_V3.txt";
START_INDEX:=1; INITIAL_COUNTERS:=[0,0,0,0,0,0,0,0,0,0,0,0]; PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";
PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0; PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";
INTERNAL_GUARD_MS:=1320000; STOP_AFTER_INDEX:=fail;
Read("/mnt/d/work/revise/production_code/escalations/degree24_v3_repair/gap_run_degree24_split_heavy_segment_v3.g");
