# Two-Way Set-Associative Cache RTL

**SystemVerilog · Four sets · Tag and data lookup**

A compact two-way, four-set cache array with valid bits, 3-bit tags, and one 8-bit data item per entry. Writes explicitly select the destination way; reads compare both ways and return hit status and matching data.

The supplied implementation covers storage and lookup. It does not include an automatic replacement policy, a memory refill or writeback engine, or a cache-coherence mechanism.

See [original source documentation](SOURCE_README.md) for the baseline files and the verification-status section below for the retained directed-test evidence.

## Run

From the repository root, with the required ModelSim/Questa executables and appropriate licence available:

```bash
bash sim/run.sh
```

Existing Windows instructions, where supplied, are retained in `scripts/`. Do not assume the testbench will run in every edition of a simulator. Check [the retained validation report](source-docs/VALIDATION.md) and the original README.

## Verification status

The included logs are historical evidence copied from the source repository. **The extracted copy has not been simulated by this extraction script.** Re-run before reporting fresh results. Some original exercises were blocked by verification-feature licence restrictions; those restrictions are not changed by packaging.

## Provenance and changes

Source commit: `df8d6f66898a08df75cd2071ddac7bbba9ba9b16`. Source path: `projects/two-way-cache`.

[SOURCE_PROVENANCE.json](SOURCE_PROVENANCE.json) records checksums of every original file. `SOURCE_README.md` is the unchanged original README. No RTL or testbench functionality was changed during extraction. Source history remains available in the original repository; this is a snapshot, not a rewrite of its authorship.

## Next engineering work

Planned tests will exercise both ways in every set, tag conflicts, reset invalidation, and duplicate-tag priority. A refill or replacement controller would be a separately specified RTL enhancement.
