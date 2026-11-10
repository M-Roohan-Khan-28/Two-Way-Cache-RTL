# Deterministic cache UVM/SVA adapter

The reusable environment lives in [AMBA-Protocol-Verification PR #16](https://github.com/M-Roohan-Khan-28/AMBA-Protocol-Verification/pull/16)
at review head `676a8b4ab0c128e1bfd6776198734b0810bc7adf`. The executed source is `9c74c35e0c2616a09af8824d2d85754738b5303a`;
this cache RTL remains locked to `b6246eff1380aa0fb7812de9fccaf12b849fa1ca`.

The adapter maps only `clk`, `reset`, `write`, `way_select`, `index`, `tag`,
`data_in`, `hit` and `data_out` into the unchanged `cache_2way`. Independent
valid/tag/data arrays observe public writes at rising clocks and asynchronous
active-high reset. Settled combinational outputs are checked without DUT
internal reads. Way 0 wins duplicate tags; inactive write inputs are unconstrained.
No handshake, automatic replacement, refill, writeback or coherence is added.

The fresh detached run passed **20/20 required substeps**, **79 named scenarios**,
**10,222 independent comparisons**, six separately identified negative
assertion controls plus one legal compound control, 27 runner record fixtures
and all nine fault parents. Each fault child exited 1; all three underlying
tools exited 0 without timeout. The original portable gate passed its separate
**7 legacy checks and 1,639 comparisons**. [Immutable full evidence](https://github.com/M-Roohan-Khan-28/AMBA-Protocol-Verification/blob/676a8b4ab0c128e1bfd6776198734b0810bc7adf/reports/cache-uvm-2026-11-10/SUMMARY.md)
includes raw logs, JSON, source hashes, measured VCD figures and byte provenance.

## Reproduce

Use the qualified Questa 2025.2/UVM 1.2 installation and ModelSim 2020.1 portable
configuration described in the [AMBA guide](https://github.com/M-Roohan-Khan-28/AMBA-Protocol-Verification/blob/676a8b4ab0c128e1bfd6776198734b0810bc7adf/docs/DETERMINISTIC_CACHE_UVM.md).
Choose unused short paths:

```powershell
$python = 'C:\Users\CG\AppData\Local\Python\pythoncore-3.14-64\python.exe'
git clone --config core.longpaths=true --config core.autocrlf=false https://github.com/M-Roohan-Khan-28/AMBA-Protocol-Verification.git C:\short\cache-uvm-source-new
git -C C:\short\cache-uvm-source-new checkout --detach 9c74c35e0c2616a09af8824d2d85754738b5303a
& $python C:\short\cache-uvm-source-new\scripts\run_cache_uvm.py --expected-env-sha 9c74c35e0c2616a09af8824d2d85754738b5303a --output C:\short\cache-uvm-results-new
if ($LASTEXITCODE -ne 0) { throw 'Required cache milestone failed or was blocked' }
```

## Status and limits

This documentation PR does not change RTL, existing benches, runners, source
provenance, licences, attribution or historical reports. Both PRs are open for
review; no merged milestone is claimed.

Functional coverage, constrained randomization and the original licence-blocked
advanced ALU/APB environments remain NOT RUN. These deterministic results do
not establish full cache compliance, replacement, refill, writeback, coherence,
coverage closure, synthesis, timing, FPGA or hardware operation.
