#!/usr/bin/env python3
"""Test C math extracted from LF sources, without a robot or LF compiler.

This does not validate LF syntax, scheduling, peripherals, or motor behavior.
"""
from pathlib import Path
import os
import re
import shlex
import shutil
import subprocess
import sys
import tempfile

REPO_ROOT = Path(__file__).resolve().parents[1]


def build_harness() -> str:
    hill_source = (REPO_ROOT / "src/HillClimbSolution.lf").read_text()
    tilt_source = (REPO_ROOT / "src/lib/Tilt.lf").read_text()
    preambles = re.findall(r"preamble\s*\{=(.*?)=\}", hill_source, re.S)
    reactions = re.findall(
        r"reaction\s*\(\s*x\s*,\s*y\s*,\s*z\s*\)"
        r"\s*->\s*pitch\s*,\s*roll\s*\{=(.*?)=\}",
        tilt_source, re.S,
    )
    if len(preambles) != 1 or len(reactions) != 1:
        raise ValueError("Expected one hill preamble and one tilt reaction; review the adapter.")
    return (
        '#include <math.h>\n#include <stdio.h>\n#include <stdlib.h>\n'
        + preambles[0]
        + '\ntypedef struct { float value; } TestPort;\n'
        + '#define lf_set(port, result) do { (port)->value = (result); } while (0)\n'
        + 'static void evaluate_tilt(TestPort* x, TestPort* y, TestPort* z, '
        + 'TestPort* pitch, TestPort* roll) {\n'
        + reactions[0] + '\n}\n'
        + r"""
static int assertions = 0;
static void expect_close(const char* name, float actual, float expected) {
    ++assertions;
    if (!isfinite(actual) || fabsf(actual - expected) > 0.001f) {
        fprintf(stderr, "FAIL %s: expected %.6f, got %.6f\n", name, expected, actual);
        exit(EXIT_FAILURE);
    }
}
static void check_tilt(const char* name, float ax, float ay, float az,
                       float expected_pitch, float expected_roll) {
    TestPort x = {ax}, y = {ay}, z = {az};
    TestPort pitch = {0}, roll = {0};
    evaluate_tilt(&x, &y, &z, &pitch, &roll);
    expect_close(name, pitch.value, expected_pitch);
    expect_close(name, roll.value, expected_roll);
    printf("PASS %s\n", name);
}
int main(void) {
    check_tilt("flat", 0, 0, 9.81f, 0, 0);
    check_tilt("positive pitch", 9.81f, 0, 9.81f, 45, 0);
    check_tilt("negative pitch", -9.81f, 0, 9.81f, -45, 0);
    check_tilt("positive roll", 0, 9.81f, 9.81f, 0, 45);
    check_tilt("negative roll", 0, -9.81f, 9.81f, 0, -45);
    check_tilt("vertical pitch", 9.81f, 0, 0, 90, 0);
    expect_close("clamp lower", clamp_value(-99, -0.01f, 0.01f), -0.01f);
    expect_close("clamp upper", clamp_value(99, -0.01f, 0.01f), 0.01f);
    expect_close("clamp interior", clamp_value(0.005f, -0.01f, 0.01f), 0.005f);
    expect_close("clamp lower boundary", clamp_value(-0.01f, -0.01f, 0.01f), -0.01f);
    expect_close("clamp upper boundary", clamp_value(0.01f, -0.01f, 0.01f), 0.01f);
    printf("PASS: %d numerical assertions (6 tilt cases, 5 clamp cases)\n", assertions);
    return EXIT_SUCCESS;
}
"""
    )


def main() -> int:
    compiler = shlex.split(os.environ.get("CC", "cc"))
    if not compiler or shutil.which(compiler[0]) is None:
        print("A host C compiler is required. Install one or set CC.", file=sys.stderr)
        return 1
    try:
        harness = build_harness()
        with tempfile.TemporaryDirectory(prefix="pololu-numeric-tests-") as directory:
            source = Path(directory) / "numeric_tests.c"
            executable = Path(directory) / "numeric_tests"
            source.write_text(harness)
            subprocess.run(
                compiler + ["-std=c11", "-Wall", "-Wextra", "-Werror", "-pedantic",
                            str(source), "-lm", "-o", str(executable)],
                check=True,
            )
            subprocess.run([str(executable)], check=True)
    except (OSError, ValueError, subprocess.CalledProcessError) as error:
        print(f"Numerical tests failed: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
