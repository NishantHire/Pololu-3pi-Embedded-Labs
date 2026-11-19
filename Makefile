.DEFAULT_GOAL := help
LFC ?= lfc
PYTHON ?= python3
APP ?= ToolsBlinkSolution
LAB_SOURCES := $(sort $(wildcard src/*Solution.lf))

.PHONY: help list doctor build build-all test test-emulator clean
help:
	@printf '%s\n' \
	  'make list                        List lab programs' \
	  'make test                        Run host tests of the actual C math' \
	  'make doctor                      Check firmware build prerequisites' \
	  'make build APP=ToolsBlinkSolution Compile one LF program' \
	  'make build-all                   Compile all lab programs' \
	  'make test-emulator               Run the inherited Pico emulator' \
	  'make clean                       Remove generated build directories'

list:
	@printf '%s\n' $(patsubst src/%.lf,%,$(LAB_SOURCES))

doctor:
	@set -eu; \
	for tool in "$(LFC)" java cmake arm-none-eabi-gcc; do \
	  command -v "$$tool" >/dev/null 2>&1 || { \
	    printf 'Missing build tool: %s. See docs/BUILD.md\n' "$$tool" >&2; exit 1; \
	  }; \
	done; \
	test -f pico-sdk/pico_sdk_init.cmake || { \
	  printf '%s\n' 'Run git submodule update --init to initialize the Pico SDK.' >&2; exit 1; \
	}; \
	test -e lf-packages/pololu-3pi-c/.git || { \
	  printf '%s\n' 'Run git submodule update --init to initialize the Pololu library.' >&2; exit 1; \
	}; \
	printenv PICO_SDK_PATH >/dev/null || { \
	  printf '%s\n' 'PICO_SDK_PATH is unset. Enter the development shell first.' >&2; exit 1; \
	}; \
	test -f "$$PICO_SDK_PATH/pico_sdk_init.cmake" || { \
	  printf '%s\n' 'PICO_SDK_PATH does not point to an initialized Pico SDK.' >&2; exit 1; \
	}; \
	printf '%s\n' 'Build prerequisites found. Compilation is checked separately.'

build: doctor
	@test -f "src/$(APP).lf" || { printf 'Unknown application: %s\n' "$(APP)" >&2; exit 1; }
	$(LFC) "src/$(APP).lf"

build-all: doctor
	@set -eu; for source in $(LAB_SOURCES); do \
	  printf 'Compiling %s\n' "$$source"; \
	  "$(LFC)" "$$source"; \
	done

test:
	$(PYTHON) scripts/test_numeric_kernels.py

test-emulator:
	@set -- test/*.hex; test -f "$$1" || { \
	  printf '%s\n' 'No test/*.hex fixtures found. See docs/VALIDATION.md.' >&2; exit 1; \
	}
	cd test && npm start

clean:
	rm -rf src-gen/ bin/ include/ build/ target/

