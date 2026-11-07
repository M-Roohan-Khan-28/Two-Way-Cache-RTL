#!/usr/bin/env python3
"""Run the preserved cache bench and independent contract scoreboard."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import time


def executable(name):
    prefix = os.environ.get("MODELSIM_BIN")
    choices = ([str(Path(prefix) / (name + ".exe")), str(Path(prefix) / name)]
               if prefix else []) + [name, name + ".exe"]
    for candidate in choices:
        found = shutil.which(candidate)
        if found:
            return found
    raise RuntimeError("Missing simulator tool: " + name)


def command(argv, cwd, logfile, timeout=120):
    try:
        result = subprocess.run(argv, cwd=cwd, capture_output=True, timeout=timeout,
                                check=False)
    except subprocess.TimeoutExpired as exc:
        logfile.write_bytes((exc.stdout or b"") + (exc.stderr or b""))
        raise RuntimeError("Timed out after %d seconds: %s" % (timeout, argv[0])) from exc
    raw = result.stdout + result.stderr
    logfile.write_bytes(raw)
    return result.returncode, raw.decode("utf-8", errors="replace")


def clean_simulation(code, log):
    return (code == 0 and not re.search(r"\*\*\s+(?:Error|Fatal):", log)
            and "# Errors: 0, Warnings: 0" in log and "$finish" in log)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--rtl", type=Path, help="Disposable fault source override")
    parser.add_argument("--capture-wave", action="store_true")
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    out = args.output_dir.resolve()
    if out.exists():
        raise RuntimeError("Output directory exists: " + str(out))
    out.mkdir(parents=True)
    rtl = (args.rtl or root / "rtl/design.sv").resolve()
    files = [rtl, root / "tb/tb_top.sv", root / "tb/cache_contract_test.sv"]
    report = {
        "repository": "Two-Way-Cache-RTL",
        "source_revision": subprocess.check_output(["git", "-C", str(root), "rev-parse", "HEAD"],
                                                    text=True).strip(),
        "source_dirty": bool(subprocess.check_output(["git", "-C", str(root),
                                                        "status", "--porcelain"])),
        "sources": [{"path": str(path), "sha256": hashlib.sha256(path.read_bytes()).hexdigest()}
                    for path in files],
        "seed": "0x28CACE17 (xorshift32 byte stimulus)",
        "timeout_seconds_per_command": 120,
        "simulations": [], "overall": "FAIL"
    }
    start = time.monotonic()
    try:
        vlib, vlog, vsim = (executable(name) for name in ("vlib", "vlog", "vsim"))
        report["simulator_version"] = command([vsim, "-version"], out,
                                               out / "version.log")[1].strip()
        if command([vlib, "work"], out, out / "library.log")[0]:
            raise RuntimeError("vlib failed")
        compile_code, compile_log = command([vlog, "-sv"] + [str(p) for p in files],
                                            out, out / "compile.log")
        if compile_code or "Errors: 0, Warnings: 0" not in compile_log:
            raise RuntimeError("vlog failed or reported diagnostics")
        for top in ("tb_cache_2way", "cache_contract_test"):
            do = "run -all; quit -code 0"
            if args.capture_wave and top == "cache_contract_test":
                signals = ("clk reset write way_select index tag data_in hit data_out").split()
                do = "vcd file cache-contract.vcd; " + "; ".join(
                    "vcd add /cache_contract_test/" + name for name in signals) + "; " + do
            argv = [vsim, "-c", "-onfinish", "exit", top, "-do", do]
            code, log = command(argv, out, out / (top + ".log"))
            entry = {"top": top, "simulator_exit_code": code, "command": argv,
                     "status": "FAIL"}
            report["simulations"].append(entry)
            if not clean_simulation(code, log):
                raise RuntimeError(top + " simulator error, fatal, missing $finish, or missing clean end")
            if top == "tb_cache_2way":
                if not re.search(r"TOTAL PASSED\s*=\s*7\b", log) or not re.search(
                        r"TOTAL FAILED\s*=\s*0\b", log) or "ALL CACHE TESTS PASSED" not in log:
                    raise RuntimeError("Legacy seven-check result missing or wrong")
                entry["checks"] = 7
            else:
                marker = re.search(r"CACHE_CONTRACT_PASS checks=(\d+) writes=(\d+) "
                                   r"resets=(\d+) seed=0x([0-9A-F]+)", log)
                if not marker or tuple(int(x) for x in marker.groups()[:3]) != (1639, 324, 2) \
                        or marker.group(4) != "28CACE17":
                    raise RuntimeError("Independent contract count/seed marker missing or wrong")
                entry.update({"checks": 1639, "writes": 324, "resets": 2})
            entry["status"] = "PASS"
            print("PASS " + top + " checks=" + str(entry["checks"]))
        if args.capture_wave:
            vcd = out / "cache-contract.vcd"
            if not vcd.is_file() or not vcd.stat().st_size:
                raise RuntimeError("Requested measured waveform was not produced")
            report["waveform"] = {"path": str(vcd),
                                  "sha256": hashlib.sha256(vcd.read_bytes()).hexdigest()}
            renderer = root / "tools/vcd_to_svg.py"
            signals = ["cache_contract_test." + s for s in
                       "clk reset write way_select index tag data_in hit".split()]
            signals.append("cache_contract_test.data_out*")
            render = [sys.executable, str(renderer), "--vcd", str(vcd), "--signals",
                      *signals, "--start", "0", "--end", "500000",
                      "--output", str(out / "cache-contract.svg"),
                      "--origin", "simulator", "--title", "Measured cache contract"]
            if command(render, out, out / "render.log")[0]:
                raise RuntimeError("VCD render failed")
        report["overall"] = "PASS"
    except Exception as exc:
        report["error"] = str(exc)
        print("FAIL: " + str(exc), file=sys.stderr)
    finally:
        report["elapsed_seconds"] = round(time.monotonic() - start, 3)
        (out / "results.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    return 0 if report["overall"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
