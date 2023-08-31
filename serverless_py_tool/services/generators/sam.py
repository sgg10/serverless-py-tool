from typing import List


class SAMGenerator:

    def _init_(self, python_runtime: str, lambda_packege: str, lambda_handler: str) -> None:
        self.runtime = python_runtime
        self.lambda_layers_names = {}
        self.output = {
            "AWSTemplateFormatVersion": '2010-09-09',
            "Transform": 'AWS::Serverless-2016-10-31',
            "Globals": {
                "Function": {
                    "Runtime": self.runtime,
                    "Handler": f"{lambda_packege}.{lambda_handler}",
                    "Architectures": ["x86_64"]
                }
            },
            "Resources": {},
            "Outputs": {}
        }

    def _create_resource_name(self, name: str, resource_name: str):
        return (
            name.translate({ ord("-"): " ", ord("_"): " " }).title() + resource_name
        ).translate({ ord(" "): "" })

    def add_layer(self, layer_name: str, layer_path: str, description: str = ""):
        resource_name = self._create_resource_name(layer_name, "Layer")
        self.lambda_layers_names[layer_name] = resource_name
        self.output["Resources"][resource_name] = {
            "Type": "AWS::Serverless::LayerVersion",
            "Properties": {
                "LayerName": layer_name,
                "Description": description,
                "ContentUri": layer_path,
                "CompatibleRuntimes": [self.runtime]
            }
        }
        self.output["Outputs"][f"{resource_name}ARN"] = {
            "Description": f"{layer_name} ARN",
            "Value": f"!Ref {resource_name}"
        }

    def add_lambda(self, lambda_name: str, lambda_path: str, envs: List[str] = [], layers: List[str] = []):
        resource_name = self._create_resource_name(lambda_name, "Function")
        resource = {
            "Type": "AWS::Serverless::Function",
            "Properties": {
                "FunctionName": lambda_name,
                "CodeUri": lambda_path
            }
        }

        if envs:
            resource["Properties"]["Environment"] = {
                "Variables": { env: "" for env in envs }
            }

        if layers:
            associated_layer = ( f"!Ref {self.lambda_layers_names.get(l)}" for l in layers )
            resource["Properties"]["Layers"] = list(filter(lambda x: x, associated_layer))

        self.output["Resources"][resource_name] = resource
        self.output["Outputs"][f"{resource_name}ARN"] = {
            "Description": f"{lambda_name} ARN",
            "Value": f"!Ref {resource_name}"
        }


    def get_content(self):
        return self.output
