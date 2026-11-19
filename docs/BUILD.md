# Build and flash

Run commands from the repository root. Programs use **Lingua Franca with the C target**.

## Initialize dependencies

```bash
git submodule update --init
git submodule status
```

Keep the recorded submodule revisions when reproducing the project. The upstream lab guide recommends initializing top-level submodules without recursively cloning every Pico SDK dependency. The inherited Nix shell may initialize SDK dependencies it needs.

## Development environment

```bash
nix develop
```

The committed `shell.nix` sets `PICO_SDK_PATH`, initializes dependencies, and installs the inherited Node emulator packages. It supplies the ARM toolchain, CMake, and hardware tools.

**LF is installed separately:** its package entries are commented out in `shell.nix`. Follow the [official prerequisites](https://www.lf-lang.org/embedded-lab/Prerequisites.html), or use the working compiler from your course environment.

Record actual tool versions:

```bash
lfc --version
arm-none-eabi-gcc --version
cmake --version
make doctor
```

For an unsupported-system error on Apple Silicon, consult [upstream troubleshooting](https://www.lf-lang.org/embedded-lab/GettingStarted.html). Do not replace a working environment or update the lockfile just for this documentation change.

Host numerical tests also need Python 3 and a host C compiler. On macOS, the latter normally comes from Xcode Command Line Tools and is distinct from the ARM cross-compiler.

## Compile

```bash
make list
make build APP=ToolsBlinkSolution
make build APP=InterruptDebouncedSolution
make build APP=HillClimbSolution
make build-all
```

The direct equivalent is `lfc src/ToolsBlinkSolution.lf`. The compiler normally writes artifacts such as `bin/ToolsBlinkSolution.elf` and `.uf2`; confirm paths in its output. `build-all` stops on the first error.

## Flash deliberately

Enter Pololu BOOTSEL by holding **B**, pressing and releasing **RESET**, then releasing **B**. Verify the artifact exists, then load:

```bash
picotool load -x bin/ToolsBlinkSolution.elf
```

`-x` starts the loaded program. Alternatively, copy its `.uf2` to the `RPI-RP2` volume. Start with an LED example; position the robot appropriately before loading a motor program.

For serial output, identify the robot's current device path and connect with a terminal such as `screen` at 115200 baud. Device names vary.

## File handling

- Source and custom reactors belong in `src/` and `src/lib/`.
- `include/` is generated and removed by the existing cleanup target; do not place custom source there.
- Generated output, SDK downloads, emulator output, and local credentials should not be added as normal project files.
- Review any local `flake.lock` changes before claiming a matching reproducible environment. An uncommitted lockfile change on the owner's Mac was not part of the uploaded source commit.

## References

- [Getting started](https://www.lf-lang.org/embedded-lab/GettingStarted.html)
- [Compilation and hardware loading](https://www.lf-lang.org/embedded-lab/Tools.html)
- [Original template](https://github.com/lf-lang/lf-3pi-template)
