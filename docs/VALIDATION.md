# Validation and demo record

## Host numerical checks

```bash
make test
```

The adapter extracts `clamp_value` from the C preamble in `HillClimbSolution.lf` and the C reaction body from `src/lib/Tilt.lf`. A small host-side port adapter lets a C compiler execute the original numerical code.

**2026-11-19:** passed on the Linux review host with six tilt cases and five clamp cases, totaling 17 numerical assertions. The harness uses C11, strict compiler warnings, and temporary files. It requires no Python packages.

**2026-11-19, owner's Mac:** `make test` also passed all 17 numerical assertions, as confirmed by the owner's terminal output.

These checks do not cover LF parsing/code generation, scheduling, interrupts, sensor noise, motor stability, or firmware timing.

## Firmware compilation

In the configured development environment:

```bash
make doctor
make build-all
```

### Owner's Mac, November 19, 2026

| Item | Recorded evidence |
| --- | --- |
| Source revision | `54b6a73c6334f396dab18a18a97745ecee74d70f` on `portfolio-cleanup` |
| Host | macOS; exact OS version not recorded |
| Environment | Existing local development setup, after entering `nix develop` |
| Lingua Franca | `lfc 0.13.0` |
| Build | Owner ran `make build-all`; final program, `ToolsPrintfSolution`, reported successful compilation |
| Artifacts | Owner's `ls -1 bin/*Solution.elf` output listed all 17 lab programs in the catalog |
| Working tree | `git status --short` showed only a modified `flake.lock` |
| ARM compiler | Arm GNU Toolchain 14.2.Rel1, GCC `14.2.1 20241119` |
| CMake | `3.31.6` |
| Nix input | `nixos-25.05`, revision `ac62194c3917d5f474c1a844b6fd6da2db95077d` |
| Lockfile follow-up | The tested local lockfile was committed and pushed as `0c82ea2114d4dd229594579c2f59024d3529ee8b`; the owner then reported a clean working tree |

This records a successful local compilation based on the owner's terminal output. The lockfile diff was reviewed and the exact file used for the build is now committed, aligning it with the existing `nixos-25.05` input in `flake.nix`. The compilation preceded the lockfile commit; no LF source was changed by that commit. An independent fresh-checkout build has not been performed. Compilation does not establish runtime or physical robot correctness.

Firmware compilation has not been performed on the remote review host because LF, Nix, CMake, and the ARM cross-compiler are unavailable there.

## Inherited emulator

The TypeScript harness under `test/` executes Pico `.hex` files and captures UART output. It does not simulate the complete Pololu robot.

```bash
make test-emulator
```

This target rejects an empty fixture directory. The inherited runner considers termination before 10 seconds a success, does not assert UART content, and does not reliably propagate all failures as a process error. It is not a comprehensive correctness test.

## Hardware evidence

| Area | Check | New evidence |
| --- | --- | --- |
| Timers/GPIO | LED behavior and serial output | Pending |
| Interrupts | Callback/action behavior, debounce, mode changes | Pending |
| Tilt | Display values and sign on a stationary tilted robot | Pending |
| Motion | Encoder distance, turns, and bump response | Pending |
| Hill climb | Calibration, ascent, edges, turnaround, descent, stop | Pending recording; owner previously reported a successful physical run |

This is an evidence checklist, not a claim of completed new hardware tests.

## Demo recording

Show the robot and display clearly. Capture calibration, climbing, turnaround, descent, and `FINISHED` if those states actually occur in the run. Demonstrate edge recovery only if it occurs or is deliberately tested.

Record the commit and tuning constants with the video. The current turnaround threshold is 160 degrees; describe observed behavior rather than claiming exact measured 180-degree rotation.

Add the real video URL after recording. No placeholder footage or simulated hardware result is included.
