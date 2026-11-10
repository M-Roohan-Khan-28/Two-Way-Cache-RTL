# Deterministic cache UVM/SVA adapter - merged-source closeout

The reusable environment lives in AMBA-Protocol-Verification at tested merged
source `b9c35a85113c99715ede572ab1f5dd94574b23e6`. [AMBA PR #16](https://github.com/M-Roohan-Khan-28/AMBA-Protocol-Verification/pull/16) merged normally
at that commit; [cache documentation PR #3](https://github.com/M-Roohan-Khan-28/Two-Way-Cache-RTL/pull/3) merged at
`b96e33907c8e33e37aa7ce17d912f67bec5e4b9a`. The environment's runner and inventory last-change revisions remain
`9c74c35e0c2616a09af8824d2d85754738b5303a`. Cache RTL remains locked to `b6246eff1380aa0fb7812de9fccaf12b849fa1ca`; documentation merges do not
change that production source pin.

The adapter maps only `clk`, `reset`, `write`, `way_select`, `index`, `tag`,
`data_in`, `hit` and `data_out` into the unchanged `cache_2way`. Independent
valid/tag/data arrays observe public writes at rising clocks and asynchronous
active-high reset. Settled combinational outputs are checked without DUT
internal reads. Way 0 wins duplicate tags; inactive write inputs are unconstrained.
No handshake, automatic replacement, refill, writeback or coherence is added.

## Actual merged-source results

A fresh ordinary GitHub clone, explicitly detached at the merged AMBA source,
passed **20/20 named required substeps**, aggregate and actual outer wrapper
exits **0**, with clean source and matching 12 execution-input hashes.
Results: **27 synthetic runner-record fixtures**, **six individually identified
negative SVA controls and one legal control**, **79 named HDL scenarios**,
**5,111 observations / 10,222 independent comparisons**, **402 allowed writes**,
**two reset-blocked write clocks**, and **all nine fault parents PASS**.
Each intended fault child exits 1 with its exact diagnostic; vlib/vlog/vsim
each exit 0 without timeout. Unrelated crashes/errors cannot qualify a parent.
Every per-case count matches the independent schedule ledger and prior qualified
run. These procedural counts are not coverage bins or a coverage percentage.

```text
5111 lookups = 1566 hits + 3545 misses
10222 comparisons = 2 x 5111 observations
420 rising clocks; 402 write commits; 2 reset-blocked clocks; 87 reset edges
```

The original portable gate separately passed **7 legacy checks** and **1,639
contract comparisons** (324 writes/two later resets), wrapper exit 0.
Simulator: Questa Altera Starter FPGA Edition-64 2025.2, runtime QUESTA_UVM-1.2.3;
seed 0x28A6BEEF / 682016495. Portable ModelSim 2020.1 uses seed 0x28CACE17.
Counted vopt-10908 from +acc and separate onerror warning remain in raw logs.

[Immutable merged-source summary](https://github.com/M-Roohan-Khan-28/AMBA-Protocol-Verification/blob/4496a567b852fb17c44b94ff8a23c1fccf9ffaa9/reports/cache-uvm-merged-2026-11-10/SUMMARY.md),
[raw results](https://github.com/M-Roohan-Khan-28/AMBA-Protocol-Verification/blob/4496a567b852fb17c44b94ff8a23c1fccf9ffaa9/reports/cache-uvm-merged-2026-11-10/run/results.json), [actual wrapper exit](https://github.com/M-Roohan-Khan-28/AMBA-Protocol-Verification/blob/4496a567b852fb17c44b94ff8a23c1fccf9ffaa9/reports/cache-uvm-merged-2026-11-10/run/wrapper.json),
[source/input locks](https://github.com/M-Roohan-Khan-28/AMBA-Protocol-Verification/blob/4496a567b852fb17c44b94ff8a23c1fccf9ffaa9/reports/cache-uvm-merged-2026-11-10/SOURCE_LOCKS.json), and [byte audit](https://github.com/M-Roohan-Khan-28/AMBA-Protocol-Verification/blob/4496a567b852fb17c44b94ff8a23c1fccf9ffaa9/reports/cache-uvm-merged-2026-11-10/BYTE_AUDIT.json)
were published through [AMBA evidence PR](https://github.com/M-Roohan-Khan-28/AMBA-Protocol-Verification/pull/17) at
`4496a567b852fb17c44b94ff8a23c1fccf9ffaa9`. Four new figures identify their actual merged-run
VCDs, tests, windows and hashes. Scoped -text preserves original bytes.
The [original review report and figures](https://github.com/M-Roohan-Khan-28/AMBA-Protocol-Verification/blob/676a8b4ab0c128e1bfd6776198734b0810bc7adf/reports/cache-uvm-2026-11-10/SUMMARY.md)
retain their original capture and source identities.

## Reproduce

[Full reproduction instructions](https://github.com/M-Roohan-Khan-28/AMBA-Protocol-Verification/blob/4496a567b852fb17c44b94ff8a23c1fccf9ffaa9/reports/cache-uvm-merged-2026-11-10/REPRODUCE.md) use the qualified Questa
2025.2/UVM installation and ModelSim portable configuration. Keep the host awake
for serial execution; choose unused short paths:

```powershell
$python = 'C:\Users\CG\AppData\Local\Python\pythoncore-3.14-64\python.exe'
git clone --config core.longpaths=true --config core.autocrlf=false https://github.com/M-Roohan-Khan-28/AMBA-Protocol-Verification.git C:\short\cache-merged-source-new
git -C C:\short\cache-merged-source-new config core.longpaths true
git -C C:\short\cache-merged-source-new config core.autocrlf false
git -C C:\short\cache-merged-source-new checkout --detach b9c35a85113c99715ede572ab1f5dd94574b23e6
& $python C:\short\cache-merged-source-new\scripts\run_cache_uvm.py --expected-env-sha b9c35a85113c99715ede572ab1f5dd94574b23e6 --output C:\short\cache-merged-results-new
if ($LASTEXITCODE -ne 0) { throw 'Required cache milestone failed or was blocked' }
```

## Scope and limits

This documentation closeout changes no RTL, benches, runners, source provenance,
licences, attribution, previous release locks or historical reports. Subsequent
evidence/docs commits need no HDL rerun while tested execution inputs match.
The implemented contract remains two ways/four sets/3-bit tags/8-bit entries,
selected-way synchronous writes, asynchronous active-high reset and combinational
lookup with way-0 duplicate-tag priority.

Functional coverage, constrained randomization and preserved licence-blocked
original advanced ALU/APB environments remain **NOT RUN**. No X-injection
qualification is claimed for the known-output assertion guard. Automatic
replacement, refill, writeback, coherence, broader compliance, coverage closure,
synthesis, timing, FPGA and hardware remain separate work. No mandatory
deterministic cache execution blocker remains.
