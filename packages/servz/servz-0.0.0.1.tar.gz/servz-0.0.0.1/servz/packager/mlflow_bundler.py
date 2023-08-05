# Copyright © 2020 Hashmap, Inc
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
import os
import subprocess
import traceback
import uuid
from jinja2 import Template

from servz.base.packager.packager import Packager
from servz.base.exceptions.packager_error import PackagerError
from servz.base.project_config import ProjectConfig
from servz.base.utilities.parser.config_parser import ConfigParser
from servz.base.utilities.parser.cmd_config_parser import CmdConfigParser


class MLFlowPackager(Packager):

    # ---------------------------------------- #
    # ------------- Construction ------------- #
    # ---------------------------------------- #

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.__root_path: str = os.path.abspath(kwargs.get('project_path'))
        self.__workflows_path: str = os.path.join(kwargs.get('project_path'), 'workflows')

        self._pipelines: list = list()
        self._pacified_tasks: list = list()

    def build_part(self, **kwargs):
        """
        Public API for packager.

        :param kwargs:
            **kwargs.
        :return:
            None.
        """
        try:
            if 'pipelines' not in kwargs.keys():
                error_message = f"In {__name__}.build_part 'pipelines' was not found in build_part. " \
                                f"The parameters passed were: {' - '.join(kwargs.keys()) }."

                self._error_handler(error_message)
                raise ValueError(error_message)

            self._build(pipelines=kwargs.get("pipelines"))
        except:
            self.__handle_exception(f'The following error has occurred{traceback.format_exc()}')

    def _build(self, pipelines: list) -> None:
        """
        Execution logic.

        :param pipelines:
            list of pipelines.
        :return:
            None.
        """
        self._workflows = []
        for pipeline in pipelines:
            updated_pipes: list = list()
            while len(pipeline['workflow']) > 0:
                for pipe in pipeline['workflow']:
                    _res = self.__build_server(pipe=pipe)

                    if _res['successful']:
                        # Update dependencies pacified
                        self._pacified_tasks.append(pipe['stage_name'])
                        # Make a copy of the new pipes
                        updated_pipes.append(pipe)
                        # Remove old pipe
                        pipeline['workflow'].remove(pipe)

            self._build_flows.append(
                {
                    'name': pipeline['name'],
                    'workflow': updated_pipes
                }
            )

    def __build_server(self, pipe: dict) -> dict:

        if pipe.get('dependencies') and not self.__are_dependencies_pacified(pipe.get('dependencies')):
            return dict(successful=False)

        try:
            #  TOCDO:  template this out later

        except:
            self.__handle_exception(f'The following error has occurred{traceback.format_exc()}')
        self._logger.info('Server file created.')



# Copyright © 2020 Hashmap, Inc
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
import os
import traceback
import uuid
from servz.packager.asset_bundler import AssetBundler


class MLFlowBundler(AssetBundler):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.__root_path: str = os.path.abspath(kwargs.get('project_path'))

    def build_runner_script(self, pipe):

        try:
            #  TODO:  template this out later
            server_file = os.path.abspath(os.path.join(self.__root_path, 'Server_' + uuid.uuid4().hex) + '.sh')
            requirements = 'pip install -r requirements_txt'
            executable_app = f'mlflow  models serve -m ~/mlruns/0/{prediction}/artifacts/model -h 0.0.0.0 -p 8001'

            # Save Serverfile to disk
            with open(server_file, 'w') as fh:
                fh.write(requirements)
                fh.write(executable_app)
        except:
            self.__handle_exception(f'The following error has occurred{traceback.format_exc()}')

    def build_artifact_bundle(self, pipe):

        pass

    def build_endpoint(self, pipe):

        pass
