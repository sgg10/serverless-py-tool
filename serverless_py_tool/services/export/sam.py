class SAMExporter:

    def __init__(self, python_runtime: str) -> None:
        self.runtime = python_runtime
        self.output = {
            "AWSTemplateFormatVersion": '2010-09-09',
            "Transform": 'AWS::Serverless-2016-10-31',
            "Resources": {}
        }

    def _create_resource_name(self, name: str, resource_name: str):
        return (
            name.translate({ ord("-"): " ", ord("_"): " " }).title() + resource_name
        ).translate({ ord(" "): "" })

    def add_layer(self, layer_name: str, layer_path: str, description: str = ""):
        resource_name = layer_name.translate({})

