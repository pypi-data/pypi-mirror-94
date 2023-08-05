# coding:utf-8
# Copyright (c) 2019  PaddlePaddle Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"
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

from typing import List

import paddlehub as hub
from paddlehub.commands import register
from paddlehub.module.manager import LocalModuleManager
from paddlehub.utils import log, platform


@register(name='hub.list', description='Show help for commands.')
class ListCommand:
    def execute(self, argv: List) -> bool:
        manager = LocalModuleManager()

        widths = [20, 40] if platform.is_windows() else [25, 50]
        aligns = ['^', '<']
        table = log.Table(widths=widths, aligns=aligns)

        table.append('ModuleName', 'Path', colors=['green', 'green'])

        for module in manager.list():
            table.append(module.name, module.directory)

        print(table)
        return True
