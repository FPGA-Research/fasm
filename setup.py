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
#
# This file contains ONLY the custom CMake + Cython build-extension logic.
# All project metadata (name, version, dependencies, entry-points …) lives in
# pyproject.toml.  setuptools reads that file automatically via the PEP 517
# build backend before executing this hook.

import os
import re
import shutil
import subprocess
import sys
import traceback

from Cython.Build import cythonize
from packaging.version import Version
from setuptools import Extension, setup
from setuptools.command.build import build
from setuptools.command.build_ext import build_ext
from setuptools.command.develop import develop
from setuptools.command.install import install


# Based on: https://www.benjack.io/2018/02/02/python-cpp-revisited.html
class CMakeExtension(Extension):
    def __init__(self, name, sourcedir="", prefix=""):
        Extension.__init__(self, name, sources=[])
        self.sourcedir = os.path.abspath(sourcedir)
        self.prefix = prefix


# Used to share the --antlr-runtime option across build commands.
class SharedOptions:
    ANTLR_RUNTIMES = ["static", "shared"]
    options = [
        ("antlr-runtime=", None, "Whether to use a 'static' or 'shared' ANTLR runtime.")
    ]

    def __init__(self):
        self.antlr_runtime = "static"

    def initialize(self, other):
        other.antlr_runtime = None

    def load(self, other):
        if other.antlr_runtime is not None:
            self.antlr_runtime = other.antlr_runtime
            assert self.antlr_runtime in SharedOptions.ANTLR_RUNTIMES, (
                "Invalid antlr_runtime {}, expected one of {}".format(
                    self.antlr_runtime, SharedOptions.ANTLR_RUNTIMES
                )
            )


shared_options = SharedOptions()


class AntlrCMakeBuild(build_ext):
    user_options = SharedOptions.options

    def copy_extensions_to_source(self):
        original_extensions = list(self.extensions)
        self.extensions = [
            ext for ext in self.extensions if not isinstance(ext, CMakeExtension)
        ]
        super().copy_extensions_to_source()
        self.extensions = original_extensions

    def run(self):
        shared_options.load(self)
        try:
            super().run()

            try:
                out = subprocess.check_output(["cmake", "--version"])
            except OSError:
                raise RuntimeError(
                    "CMake must be installed to build "
                    "the following extensions: "
                    + ", ".join(e.name for e in self.extensions)
                )

            cmake_version = Version(
                re.search(r"version\s*([\d.]+)", out.decode()).group(1)
            )
            if cmake_version < Version("3.7.0"):
                raise RuntimeError("CMake >= 3.7.0 is required.")

            for ext in self.extensions:
                self.build_extension(ext)

        except BaseException as e:
            print(
                "Failed to build ANTLR parser, "
                "falling back on slower textX parser. Error:\n",
                e,
            )
            traceback.print_exc()

    # FIXME: Remove this function
    # see: https://github.com/chipsalliance/fasm/issues/50
    def add_flags(self):
        if sys.platform.startswith("win"):
            return

        for flag in ["CFLAGS", "CXXFLAGS"]:
            flags = [os.environ.get(flag, "")]
            if not flags[0]:
                flags.pop(0)

            if shared_options.antlr_runtime == "static":
                flags.append("-fPIC")

            # Disable excessive warnings in the ANTLR runtime.
            flags.append("-Wno-attributes")

            if flags:
                os.environ[flag] = " ".join(flags)

    def build_extension(self, ext):
        if isinstance(ext, CMakeExtension):
            extdir = os.path.join(
                os.path.abspath(os.path.dirname(self.get_ext_fullpath(ext.name))),
                ext.prefix,
            )
            cmake_args = [
                "-DCMAKE_INSTALL_PREFIX=" + extdir,
                "-DCMAKE_LIBRARY_OUTPUT_DIRECTORY=" + extdir,
                "-DPYTHON_EXECUTABLE=" + sys.executable,
                "-DANTLR_RUNTIME_TYPE=" + shared_options.antlr_runtime,
            ]

            cfg = "Debug" if self.debug else "Release"
            build_args = ["--config", cfg]
            cmake_args += ["-DCMAKE_BUILD_TYPE=" + cfg]
            if not sys.platform.startswith("win") and (
                os.environ.get("CMAKE_BUILD_PARALLEL_LEVEL") is None
            ):
                build_args += ["--", "-j"]

            env = os.environ.copy()
            env["CXXFLAGS"] = '{} -DVERSION_INFO=\\"{}\\"'.format(
                env.get("CXXFLAGS", ""), self.distribution.get_version()
            )

            if os.path.exists(self.build_temp):
                shutil.rmtree(self.build_temp, ignore_errors=True)
            os.makedirs(self.build_temp, exist_ok=True)

            self.add_flags()

            subprocess.check_call(
                ["cmake", ext.sourcedir] + cmake_args, cwd=self.build_temp, env=env
            )
            subprocess.check_call(
                ["cmake", "--build", "."] + build_args, cwd=self.build_temp
            )
            subprocess.check_call(["cmake", "--install", "."], cwd=self.build_temp)
            subprocess.check_call(["ctest"], cwd=self.build_temp)
            print()
        else:
            super().build_extension(ext)

    def initialize_options(self):
        super().initialize_options()
        shared_options.initialize(self)

    def finalize_options(self):
        super().finalize_options()
        shared_options.load(self)


class BuildCommand(build):
    user_options = build.user_options + SharedOptions.options

    def initialize_options(self):
        super().initialize_options()
        shared_options.initialize(self)

    def finalize_options(self):
        super().finalize_options()
        shared_options.load(self)

    def run(self):
        shared_options.load(self)
        super().run()


class InstallCommand(install):
    user_options = install.user_options + SharedOptions.options

    def initialize_options(self):
        super().initialize_options()
        shared_options.initialize(self)

    def finalize_options(self):
        super().finalize_options()
        shared_options.load(self)

    def run(self):
        shared_options.load(self)
        super().run()


class DevelopCommand(develop):
    user_options = develop.user_options + SharedOptions.options

    def initialize_options(self):
        super().initialize_options()
        shared_options.initialize(self)

    def finalize_options(self):
        super().finalize_options()
        shared_options.load(self)

    def run(self):
        shared_options.load(self)
        super().run()


setup(
    ext_modules=[
        CMakeExtension("parse_fasm", sourcedir="src", prefix="fasm/parser"),
    ]
    + cythonize("fasm/parser/antlr_to_tuple.pyx"),
    cmdclass={
        "build_ext": AntlrCMakeBuild,
        "build": BuildCommand,
        "develop": DevelopCommand,
        "install": InstallCommand,
    },
)
