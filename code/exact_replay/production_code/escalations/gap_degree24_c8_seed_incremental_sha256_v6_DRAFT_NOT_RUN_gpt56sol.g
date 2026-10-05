# DRAFT_NOT_RUN. Static helper design only; never Read() this file from a
# production wrapper until the dedicated GAP 4.12.1 probe and equivalence
# smokes described in the companion audit note have passed.
#
# This module is deliberately not a complete engine.  Its functions are the
# proposed V6 replacement for V5's repeated StringFile(OUT)+HexSHA256 calls.
# All tracked output is ASCII, so GAP string Length equals the emitted byte
# count under the sealed Ubuntu/GAP execution environment.

D24C8PadSHA256HexV6:=function(h)
 h:=LowercaseString(h);
 while Length(h)<64 do h:=Concatenation("0",h); od;
 if Length(h)<>64 then Error("SHA256 width"); fi;
 return h;
end;

D24C8SHA256WordsHexV6:=function(words) local value,i,word;
 if Length(words)<>8 then Error("incremental SHA256 word count"); fi;
 value:=0;
 for i in [0..7] do
  word:=words[8-i];
  if not IsInt(word) or word<0 or word>=2^32 then
   Error("incremental SHA256 word range");
  fi;
  value:=value+word*2^(32*i);
 od;
 return D24C8PadSHA256HexV6(HexStringInt(value));
end;

# GAP_SHA256_FINAL is treated as destructive.  Finalize only a copy, leaving
# the live state available for later CHECKPOINT_COMMITTED and alpha records.
D24C8SHA256StateHexV6:=function(state) local stateCopy;
 stateCopy:=ShallowCopy(state);
 return D24C8SHA256WordsHexV6(GAP_SHA256_FINAL(stateCopy));
end;

# This is the in-engine version of gap_probe_sha256_incremental_copy_gpt56sol.g.
# It must execute before OUT is created.  The second snapshot after the first
# finalization detects a copy that aliases/destructively changes the live state.
D24C8RequireIncrementalSHA256V6:=function() local state,h0,h1,h1Again,h2;
 state:=GAP_SHA256_INIT();
 h0:=D24C8SHA256StateHexV6(state);
 if h0<>D24C8PadSHA256HexV6(HexSHA256("")) then
  Error("incremental SHA256 empty mismatch");
 fi;
 GAP_SHA256_UPDATE(state,"a");
 h1:=D24C8SHA256StateHexV6(state);
 h1Again:=D24C8SHA256StateHexV6(state);
 if h1<>D24C8PadSHA256HexV6(HexSHA256("a")) or h1Again<>h1 then
  Error("incremental SHA256 copy mismatch after a");
 fi;
 GAP_SHA256_UPDATE(state,"b");
 h2:=D24C8SHA256StateHexV6(state);
 if h2<>D24C8PadSHA256HexV6(HexSHA256("ab")) then
  Error("incremental SHA256 copy mismatch after ab");
 fi;
end;

# Reconstruct and authenticate exactly the committed prefix of the previous
# segment once at continuation startup.  A longer file is intentional and
# permitted: bytes after prefixBytes are an uncheckpointed/summary tail.  The
# returned state represents precisely that prefix, but MUST NOT seed the new
# segment's tracker because V5 OUTPUT_PREFIX_* values are per-OUT-file.
D24C8ValidatePriorPrefixV6:=function(path,prefixBytes,expectedSha)
 local text,state,actual;
 if prefixBytes<0 then Error("negative prior output prefix length"); fi;
 if not IsExistingFile(path) then Error("prior output missing"); fi;
 text:=StringFile(path);
 if Length(text)<prefixBytes then Error("prior output prefix truncated"); fi;
 state:=GAP_SHA256_INIT();
 if prefixBytes>0 then
  GAP_SHA256_UPDATE(state,text{[1..prefixBytes]});
 fi;
 actual:=D24C8SHA256StateHexV6(state);
 if actual<>LowercaseString(expectedSha) then
  Error("prior output prefix hash");
 fi;
 return rec(state:=state,bytes:=prefixBytes,fileBytes:=Length(text),sha256:=actual);
end;

# Every write to the new segment OUT must pass through these two functions.
# AppendTo/PrintTo complete before the matching state update.  Therefore an I/O
# error cannot advance a checkpoint; an update failure can only leave an
# uncheckpointed orphan/tail, which the existing recovery model already allows.
D24C8NewOutputTrackerV6:=function(path)
 if IsExistingFile(path) then Error("refusing to overwrite output"); fi;
 return rec(path:=path,state:=GAP_SHA256_INIT(),bytes:=0,created:=false);
end;

D24C8TrackedCreateV6:=function(tracker,text)
 if tracker.created or tracker.bytes<>0 or IsExistingFile(tracker.path) then
  Error("tracked output create state");
 fi;
 if not IsString(text) then Error("tracked output requires one string"); fi;
 PrintTo(tracker.path,text);
 GAP_SHA256_UPDATE(tracker.state,text);
 tracker.bytes:=Length(text);
 tracker.created:=true;
end;

D24C8TrackedAppendV6:=function(tracker,text)
 if not tracker.created or not IsExistingFile(tracker.path) then
  Error("tracked output append state");
 fi;
 if not IsString(text) then Error("tracked output requires one string"); fi;
 AppendTo(tracker.path,text);
 GAP_SHA256_UPDATE(tracker.state,text);
 tracker.bytes:=tracker.bytes+Length(text);
end;

D24C8TrackedSnapshotV6:=function(tracker)
 if not tracker.created then Error("tracked output snapshot before create"); fi;
 return rec(bytes:=tracker.bytes,sha256:=D24C8SHA256StateHexV6(tracker.state));
end;

