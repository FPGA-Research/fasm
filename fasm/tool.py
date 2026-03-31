#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
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

import argparse

from fasm import fasm_tuple_to_string
from fasm.parser import parse_fasm_filename


def main():
    parser = argparse.ArgumentParser("FASM tool")
    parser.add_argument("file", help="Filename to process")
    parser.add_argument(
        "--canonical",
        action="store_true",
        help="Return canonical form of FASM.")

    args = parser.parse_args()

    fasm_tuples = parse_fasm_filename(args.file)
    print(fasm_tuple_to_string(fasm_tuples, args.canonical))


if __name__ == "__main__":
    main()
