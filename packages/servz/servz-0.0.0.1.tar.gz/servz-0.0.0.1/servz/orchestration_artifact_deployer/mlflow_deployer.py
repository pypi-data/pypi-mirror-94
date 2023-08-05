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
import subprocess
import traceback
from servz.base.orhcestration_artifact_deployer.orchestration_artifact_deployer import OrchestrationArtifactDeployer


class MLFlowDeployer(OrchestrationArtifactDeployer):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.__namespace = kwargs.get('namespace')
        if not self.__namespace:
            self.__namespace = 'mlflow'
        self.result = None

    def _run(self, artifact: str):

        try:
            print("running mlflow deployer... ")
            self.result = subprocess.run(artifact, check=True, stderr=subprocess.STDOUT)

            if self.result.stderr:
                print('Standard Error: ', self.result.stderr)
            return True

        except Exception:
            error_message = traceback.format_exc()
            print(error_message)
            self._error_handler(error_message)

            return False
