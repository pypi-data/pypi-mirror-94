# =============================================================================
#                ____                                       ____ _
#   _ __  _   _ / ___|___  _ __ ___  _ __ ___   ___  _ __  / ___| | __ _ ___ ___  ___  ___
#  | '_ \| | | | |   / _ \| '_ ` _ \| '_ ` _ \ / _ \| '_ \| |   | |/ _` / __/ __|/ _ \/ __|
#  | |_) | |_| | |__| (_) | | | | | | | | | | | (_) | | | | |___| | (_| \__ \__ \  __/\__ \
#  | .__/ \__, |\____\___/|_| |_| |_|_| |_| |_|\___/|_| |_|\____|_|\__,_|___/___/\___||___/
#  |_|    |___/
# =============================================================================
# Authors:            Patrick Lehmann
#
# Python package:     A collection of common classes for Python
#
# Description:
# ------------------------------------
#		TODO
#
# License:
# ============================================================================
# Copyright 2020-2021 Patrick Lehmann - Bötzingen, Germany
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# SPDX-License-Identifier: Apache-2.0
# ============================================================================
#
import setuptools

with open("README.md", "r") as file:
	long_description = file.read()

requirements = []
with open("requirements.txt") as file:
	for line in file.readlines():
		requirements.append(line)

projectName = "pyCommonClasses"

github_url =  "https://github.com/Paebbels/" + projectName
rtd_url =     "https://" + projectName + ".readthedocs.io/en/latest/"

setuptools.setup(
	name=projectName,
	version="0.2.1",

	author="Patrick Lehmann",
	author_email="Paebbels@gmail.com",
	# maintainer="Patrick Lehmann",
	# maintainer_email="Paebbels@gmail.com",

	description="A collection of common classes for Python.",
	long_description=long_description,
	long_description_content_type="text/markdown",

	url=github_url,
	project_urls={
		'Documentation': rtd_url,
		'Source Code':   github_url,
		'Issue Tracker': github_url + "/issues"
	},
	# download_url="",

	packages=setuptools.find_packages(),
	classifiers=[
		"License :: OSI Approved :: Apache Software License",
		"Operating System :: OS Independent",
		"Programming Language :: Python :: 3 :: Only",
		"Programming Language :: Python :: 3.6",
		"Programming Language :: Python :: 3.7",
		"Programming Language :: Python :: 3.8",
		"Programming Language :: Python :: 3.9",
		"Development Status :: 5 - Production/Stable",
		"Intended Audience :: Developers",
		"Topic :: Utilities"
	],
	keywords="Python3 Class Collection",

	python_requires='>=3.6',
	install_requires=requirements
)
