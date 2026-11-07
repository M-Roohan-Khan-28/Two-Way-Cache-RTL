# Cache contract and verification plan

`cache_2way` stores two ways x four sets of valid, 3-bit tag, and 8-bit data.
`way_select` chooses the written way; there is no automatic replacement,
refill, writeback, or coherence. A rising clock edge writes the selected entry
when `write=1`. Active-high asynchronous reset invalidates all entries and
has priority over writes. Lookup is combinational, returns zero on a miss,
and prefers way 0 if both ways have the same matching tag. Checks of a write
result occur after nonblocking assignments settle.

The original [seven-check bench](../tb/tb_top.sv) remains unchanged. The new
[contract bench](../tb/cache_contract_test.sv) maintains separate valid, tag,
and data arrays. Expected hit/data come only from those arrays and the public
inputs; no DUT memory or DUT output is used as the expected value.

| Requirement | Directed or enumerated test |
| --- | --- |
| All ways, sets, and tags | 2 x 4 x 8 write/tag sweeps, then all set/tag lookups |
| Byte data and entry isolation | All 256 byte values at way 0/set 0/tag 0; unrelated tags queried |
| Way-0 duplicate priority and overwrite | Two ways filled with tag 5, then way 0 changed to tag 4 |
| Reset, held reset/write, refill | Between-edge reset, reset across clocked write, post-reset queries and refill |
| Combinational hit/miss and no-write preservation | Queries before the next rising edge and after idle cycles |
| Bounded progress | 200,000 ns simulation watchdog and 120-second process timeout |

At source commit `73805b661e131c4f61b6258dc1abe99d0a12c3af`, the old bench
reported 7 checks and the new bench reported 1,639 comparisons, 324 writes,
2 later resets, seed `0x28CACE17`. The [passing result](../reports/technical-completion-2026-11-07/passing/results.json)
records a clean source and the actual simulator version. A [disposable way-0
priority fault](../reports/technical-completion-2026-11-07/duplicate-priority-fault/fault-summary.json)
caused the new bench to fatal with `CACHE_MISMATCH` and wrapper exit 1 while
the original seven checks passed. The mutation is retained only as evidence,
outside active RTL.

The optional VCD export uses public testbench signals. The three measured
SVGs and their renderer metadata are in the passing report. No measured code,
functional, or assertion coverage denominator is available; comparison count
does not imply coverage closure. The original RTL and source provenance were
not modified. UVM/SVA/covergroups require a working licensed simulator path
before any execution result can be claimed.

