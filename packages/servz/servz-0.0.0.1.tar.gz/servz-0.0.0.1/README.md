<!---
# Modifications © 2020 Hashmap, Inc
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
-->

# Servz
##  Machine Learning Model Serving

This library is a pre-alpha right now

The intent of this package is to provide a machine learning deplpoyment layer for model predictions.

## Features
* pipeline driven  
*  deployment via task runner
*  deployment via flask or other endpoint
*  MLFlow based deployment
*  Seldon deployment (in progress)

## Model Serving Architectures

###  Model as Code
Model is written by some developer and relatively standard IT DevOps procedures used to bring model into production.

Frameworks using the MoC architecture include:
* MLFlow
* Seldon
* Clipper
* Tensorflow Serving

pros:
- easy development
- data scientist does not need to be an SRE or deal with deployment
- automation (of standardized parts, if any)
- model state included in production code

cons:
- ever increasing complexities with scale
- increased latency, becomes a bottleneck at scale
- different toolsets used
- difficult to update
- hard to rebuild
- overall lack of scale


### Model as Data
The model is implemented via a parameter file of some kind.

Data formats used in MaD architectures include:
* Tensorflow SavedModelks
* PMML
* PFA
* ONNX

Frameworks using MaD concepts include:
* Lightbend
* Akka Serving
* Spark Structured Streaming
* Flink
* Kafka Queryable State

pros:
- simple model management
- model standardization
- low latency
- easy to implement
- forces cross-silo communication

cons:
-  not all tools support model formats
- standardization still in early stages


### Other Model Serving Patterns
* TBA

## Current opinion
1.  For workloads at low scale use MaC
2.  For workloads at high scale (aka batch() use MaD

## structure
````
/base  - common library
/core - core files for servz
/orchestration_artifact_builder - artifact packager
/orchestration_artifact_deployer - deployment runner
/packager - manifest packager
/pipeline - loading and validation of serving pipeline
/server_templates - artifacts for artifact builder to construct endpoints
/tests - unit tests and e2e tests

```