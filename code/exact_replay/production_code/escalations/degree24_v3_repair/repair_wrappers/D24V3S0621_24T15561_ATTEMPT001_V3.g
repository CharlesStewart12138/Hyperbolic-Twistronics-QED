SEGMENT_FILE:="/mnt/d/work/revise/production_code/escalations/degree24_v3_repair/repair_plan_segments/D24V3S0621_24T15561.g"; EXPECTED_SEGMENT_FILE_SHA256:="45208f0299d6f2cca1d268e2a4d749a2c09453fc12e6d3d2d8b1b12e248fa58d";
OUT:="/mnt/d/work/revise/production_code/escalations/degree24_v3_repair/repair_outputs/D24V3S0621_24T15561_ATTEMPT001_V3.txt"; CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/degree24_v3_repair/repair_checkpoints/D24V3S0621_24T15561_CHECKPOINT_V3.txt"; CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/degree24_v3_repair/repair_checkpoints/D24V3S0621_24T15561_CHECKPOINT_TMP_V3.txt";
START_INDEX:=1; INITIAL_COUNTERS:=[0,0,0,0,0,0,0,0,0,0,0,0]; PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";
PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0; PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";
INTERNAL_GUARD_MS:=1320000; STOP_AFTER_INDEX:=fail;
Read("/mnt/d/work/revise/production_code/escalations/degree24_v3_repair/gap_run_degree24_split_heavy_segment_v3.g");
