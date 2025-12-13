.PHONY: run

RESOURCE_PATH := ./src/frontend/src/assets/resources.qrc
RESOURCE_OUTPUT := ./src/frontend/src/assets
PROGRAM_PATH := ./src/frontend/app.py
OS_NAME :=
PY_COMMAND  :=

# Check the operating system and set variables accordingly
ifeq ($(OS), Windows_NT)
    OS_NAME = Windows
    PY_COMMAND = py
else
 	UNAME_S := $(shell uname -s)
    ifeq ($(UNAME_S), Linux)
        PY_COMMAND = python3
    else ifeq ($(UNAME_S), Darwin)
		PY_COMMAND = python3
	else
		$(error Unsupported OS: $(UNAME_S))
	endif
endif

run:
	 pyside6-rcc .\assets\resources.qrc -o .\src\frontend\resources_rc.py
	$(PY_COMMAND) $(PROGRAM_PATH)
