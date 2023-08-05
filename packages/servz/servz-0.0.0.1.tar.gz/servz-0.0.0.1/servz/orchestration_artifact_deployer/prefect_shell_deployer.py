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
from prefect import task, Flow, Parameter
from prefect.tasks.shell import ShellTask


class PrefectShellDeployer(OrchestrationArtifactDeployer):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.__namespace = kwargs.get('namespace')
        if not self.__namespace:
            self.__namespace = 'shell'
        self.result = None

    @task(log_stdout=True)
    def run_shell(self, shell_script):
        try:
            cmd = 'source ' + shell_script
            ShellTask(cmd)
        except:
            error_message = traceback.format_exc()
            print(error_message)
            self._error_handler(error_message)

    def _run(self, artifact: str):

        try:
            print("running shell deployer... ")
            with Flow("Serving Flow") as flow:
                self.run_shell(artifact)
                flow.run()

        return True
