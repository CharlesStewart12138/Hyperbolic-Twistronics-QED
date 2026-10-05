parsed:=ReadAsFunction("/mnt/d/work/revise/production_code/escalations/degree24_v3_repair/gap_verify_native_key_manifest_membership_v5.g");
if parsed=fail then QUIT_GAP(1); fi;
Print("NATIVE_MEMBERSHIP_V5_PARSE_PASS\n");
QUIT_GAP(0);
