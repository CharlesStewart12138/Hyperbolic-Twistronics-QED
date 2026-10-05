SEGMENT_FILE:="/mnt/d/work/revise/production_code/escalations/degree24_v3_repair/repair_plan_segments/D24V3S0551_24T15367.g"; EXPECTED_SEGMENT_FILE_SHA256:="a20a1f3d99ff8991505d8435c5c1bbcce7e405056af659f98b974ca9236b3285";
OUT:="/mnt/d/work/revise/production_code/escalations/degree24_v3_repair/repair_outputs/D24V3S0551_24T15367_ATTEMPT001_V3.txt"; CHECKPOINT_FILE:="/mnt/d/work/revise/production_code/escalations/degree24_v3_repair/repair_checkpoints/D24V3S0551_24T15367_CHECKPOINT_V3.txt"; CHECKPOINT_TMP:="/mnt/d/work/revise/production_code/escalations/degree24_v3_repair/repair_checkpoints/D24V3S0551_24T15367_CHECKPOINT_TMP_V3.txt";
START_INDEX:=1; INITIAL_COUNTERS:=[0,0,0,0,0,0,0,0,0,0,0,0]; PREVIOUS_CHECKPOINT_SHA256:="NONE_FRESH_START";
PREVIOUS_OUTPUT_FILE:="NONE_FRESH_START"; PREVIOUS_OUTPUT_PREFIX_BYTES:=0; PREVIOUS_OUTPUT_PREFIX_SHA256:="NONE_FRESH_START";
INTERNAL_GUARD_MS:=1320000; STOP_AFTER_INDEX:=fail;
Read("/mnt/d/work/revise/production_code/escalations/degree24_v3_repair/gap_run_degree24_split_heavy_segment_v3.g");
