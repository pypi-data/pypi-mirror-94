from dataclasses import dataclass
from pollination_dsl.function import Function, command, Inputs, Outputs


@dataclass
class CreateRadianceFolder(Function):
    """Create a Radiance folder from a HBJSON input file."""

    input_model = Inputs.file(
        description='Path to input HBJSON file.',
        path='model.hbjson'
    )

    @command
    def hbjson_to_rad_folder(self):
        return 'honeybee-radiance translate model-to-rad-folder model.hbjson'

    model_folder = Outputs.folder(description='Radiance folder.', path='model')

    sensor_grids = Outputs.list(
        description='Sensor grids information.', path='model/grid/_info.json'
    )
