from pathlib import Path


def analyze_lambda_layers(lambda_layers_base_path: str):
    layers = {}
    path = Path(lambda_layers_base_path)
    for layer in (x for x in path.glob("*") if x.is_dir()):
        modules = [x.name for x in layer.joinpath("python").glob("*") if x.is_dir()]
        layers[layer.name] = {
            "modules": modules,
            "path": f"{lambda_layers_base_path}/{layer.name}"
        }
    return layers
