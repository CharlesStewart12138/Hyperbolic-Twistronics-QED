SEGMENT_FILE:="/mnt/d/work/revise/production_code/escalations/degree24_v3_repair/repair_plan_segments/D24V3S0748_24T15735.g"; EXPECTED_SEGMENT_FILE_SHA256:="ff1fb994a0a5dd4201f91cf4ff44793cafdc2e25c0ad5730ecc8f1c531fe4fe1";
OUT:="/mnt/d/work/revise/production_code/escalations/degree24_v3_repair/repair_outputs/D24V3S0748_24T15735_ATTEMPT001_V3.txt"; CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/degree24_v3_repair/repair_checkpoints/D24V3S0748_24T15735_CHECKPOINT_V3.txt"; CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/degree24_v3_repair/repair_checkpoints/D24V3S0748_24T15735_CHECKPOINT_TMP_V3.txt";
START_INDEX:=1; INITIAL_COUNTERS:=[0,0,0,0,0,0,0,0,0,0,0,0]; PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";
PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0; PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";
INTERNAL_GUARD_MS:=1320000; STOP_AFTER_INDEX:=fail;
Read("/mnt/d/work/revise/production_code/escalations/degree24_v3_repair/gap_run_degree24_split_heavy_segment_v3.g");
