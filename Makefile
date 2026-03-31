# Copyright 2017-2022 F4PGA Authors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# SPDX-License-Identifier: Apache-2.0

# Build/install
# ------------------------------------------------------------------------
build-clean:
	rm -rf dist fasm.egg-info

.PHONY: build-clean

build:
	make build-clean
	python -m build

.PHONY: build

install:
	pip install -e .

.PHONY: install

# Test, lint, auto-format.
# ------------------------------------------------------------------------

test:
	pytest -s tests

.PHONY: test

# Find Python files tracked by git, excluding third_party and hidden dirs.
PY_FILES := $(shell git ls-files | grep -ve '^third_party\|^\.|^env' | grep -e '\.py$$')

lint:
	flake8 $(PY_FILES)

.PHONY: lint

format-py:
	yapf -p -i $(PY_FILES)

.PHONY: format-py

format: format-py

.PHONY: format

# Checks
# ------------------------------------------------------------------------
check-license:
	@./.github/check_license.sh

.PHONY: check-license

check-python-scripts:
	@./.github/check_python_scripts.sh

.PHONY: check-python-scripts

# Upload to PyPI
# ------------------------------------------------------------------------
upload-check: build
	twine check dist/*

.PHONY: upload-check
