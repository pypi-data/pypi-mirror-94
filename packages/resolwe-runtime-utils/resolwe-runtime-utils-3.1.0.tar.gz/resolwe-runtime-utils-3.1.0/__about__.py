# Copyright 2019 Genialis, Inc.
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

"""Central place for package metadata."""

from pkg_resources import DistributionNotFound, get_distribution

__name__ = "resolwe-runtime-utils"
__title__ = "Resolwe Runtime Utilities"
__summary__ = "Runtime utilities for Resolwe dataflow engine"
__url__ = "https://github.com/genialis/resolwe-runtime-utils"
__git_repo_url__ = __url__

try:
    __version__ = get_distribution(__name__).version
except DistributionNotFound:
    # Package is not (yet) installed.
    pass

__author__ = "Genialis, Inc."
__email__ = "dev-team@genialis.com"

__license__ = "Apache License (2.0)"
__copyright__ = "2015-2019, " + __author__
