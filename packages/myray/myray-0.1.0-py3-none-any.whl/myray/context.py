#
# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import atexit
from contextlib import ContextDecorator
from threading import RLock
from typing import Dict, Union, Optional

import ray



class _MyContext(ContextDecorator):
    def __init__(self,
                 app_name: str,
                 configs: Dict[str, str] = None):
        self._app_name = app_name



def init_sp(app_name: str,
            configs: Optional[Dict[str, str]] = None):

    if not ray.is_initialized():
        # ray has not initialized, init local
        ray.init()
