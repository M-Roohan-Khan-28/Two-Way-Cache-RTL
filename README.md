# Two-Way Set-Associative Cache RTL

**SystemVerilog · Four sets · Tag and data lookup**

A compact two-way, four-set cache array with valid bits, 3-bit tags, and one 8-bit data item per entry. Writes explicitly select the destination way; reads compare both ways and return hit status and matching data.

The supplied implementation covers storage and lookup. It does not include an automatic replacement policy, a memory refill or writeback engine, or a cache-coherence mechanism.

See [original source documentation](SOURCE_README.md) for the baseline files and the verification-status section below for the retained directed-test evidence.

## Run

From the repository root, with Python 3.9+ and ModelSim/Questa `vlib`, `vlog`,
and `vsim` available, use a new output directory for each run:

```powershell
$env:MODELSIM_BIN = 'C:\intelFPGA\20.1\modelsim_ase\win32aloem'
powershell.exe -NoProfile -ExecutionPolicy Bypass -File scripts/run_sim.ps1 -OutputDir C:\short\cache-run-unique -CaptureWave
```

The shell entry point is `bash sim/run.sh /new/output/path` on systems with
Python 3 and a compatible simulator. The new runner refuses to overwrite its
output, checks exact completion markers and counts, enforces 120-second
subprocess limits, and returns nonzero on a missing tool, compile error,
simulator fatal, timeout, or mismatch. The shell launcher has only been syntax
checked here; no Linux simulator run is claimed. See the [retained validation
report](source-docs/VALIDATION.md) for earlier evidence.

## Verification status

The extraction-time logs remain historical evidence. A separate committed-source
run at `73805b661e131c4f61b6258dc1abe99d0a12c3af` passed the preserved
**7 legacy checks** and **1,639 independent contract comparisons** over 324
writes and two later resets, using deterministic xorshift seed `0x28CACE17`.
The PowerShell wrapper exited 0 under ModelSim Intel FPGA Starter Edition
`vsim 2020.1 Simulator 2020.02 Feb 28 2020`. The [new raw logs and
JSON](reports/technical-completion-2026-11-07/passing/) are separate from
earlier reports. A disposable duplicate-tag-priority mutation left the legacy
seven checks passing but triggered `CACHE_MISMATCH` in the new oracle; the
[fault run](reports/technical-completion-2026-11-07/duplicate-priority-fault/)
returned wrapper exit 1. No RTL correction was needed.

The [measured write/lookup waveform](reports/technical-completion-2026-11-07/passing/cache-contract.svg),
[late duplicate/reset window](reports/technical-completion-2026-11-07/passing/cache-duplicate-window.svg),
and [reset/refill window](reports/technical-completion-2026-11-07/passing/cache-reset-window.svg)
were rendered from the [actual selected-signal VCD](reports/technical-completion-2026-11-07/passing/cache-contract.vcd).
The sibling JSON files record the 1 ps VCD timebase, crop windows, and raw
trace hash. These figures are measured samples; `tools/vcd_to_svg.py` does not
assess functional correctness. [Verification plan](docs/verification_plan.md)
maps the bounded contract to the checks.

The installed Starter simulator passed basic SV/interfaces but did not execute
the probed randomization, covergroups, SVA, or UVM flows; those advanced
workstreams remain blocked or NOT RUN. The portable check count is not a
functional/code coverage percentage. Synthesis, timing, FPGA, and hardware
were not run.

## Provenance and changes

Source commit: `df8d6f66898a08df75cd2071ddac7bbba9ba9b16`. Source path: `projects/two-way-cache`.

[SOURCE_PROVENANCE.json](SOURCE_PROVENANCE.json) records checksums of every original file. `SOURCE_README.md` is the unchanged original README. No RTL or testbench functionality was changed during extraction. Source history remains available in the original repository; this is a snapshot, not a rewrite of its authorship.

## Next engineering work

The next milestone is licensed advanced verification or target-specific
implementation evidence. A refill or replacement controller remains a
separately specified RTL enhancement.
