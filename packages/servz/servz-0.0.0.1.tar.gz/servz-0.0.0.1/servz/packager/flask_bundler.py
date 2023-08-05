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


class FlaskBundler(AssetBundler):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.__root_path: str = os.path.abspath(kwargs.get('project_path'))
        self.__prediction_main = kwargs.get('predict')
        self.__predictor = ''

    def build_runner_script(self, pipe):

        try:
            #  TODO:  template this out later
            runner = os.path.abspath(os.path.join(self.__root_path, 'server_' + uuid.uuid4().hex) + '.sh')
            requirements = 'pip install -r requirements_txt'
            executable_app = f'python app.py'

            # Save runner file to disk
            with open(runner, 'w') as fh:
                fh.write(requirements)
                fh.write(executable_app)
            fh.close()
        except:
            self.__handle_exception(f'The following error has occurred{traceback.format_exc()}')

    def build_artifact_bundle(self, pipe):

        path = str(self.__prediction_main)
        path_list = path.split('/')
        self.__predictor = path_list[-1].replace('.py','')

    def build_endpoint(self, pipe):

        # read in template file
        flask_code = os.path.join(self.__root_path, 'server_templates', 'flask', 'app.py')
        with open(flask_code, 'r') as fh:
            code = fh.read()
        fh.close()

        # apply parameters
        template = str(code)
        endpoint = template.replace('{predict}', self.__predictor)

        # save out to local path
        server = os.path.abspath(os.path.join(self.__root_path, 'app.py'))
        with open(server, 'w') as fh:
            fh.write(endpoint)
        fh.close
