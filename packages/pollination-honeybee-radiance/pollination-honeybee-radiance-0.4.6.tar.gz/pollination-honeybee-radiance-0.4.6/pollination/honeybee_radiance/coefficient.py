from dataclasses import dataclass
from pollination_dsl.function import Function, command, Inputs, Outputs


@dataclass
class DaylightCoefficient(Function):
    """Calculate daylight coefficient for a grid of sensors from a sky matrix."""

    radiance_parameters = Inputs.str(
        description='Radiance parameters. -I, -c 1 and -aa 0 are already included in '
        'the command.', default=''
    )

    fixed_radiance_parameters = Inputs.str(
        description='Radiance parameters. -I, -c 1 and -aa 0 are already included in '
        'the command.', default='-aa 0'
    )

    sensor_count = Inputs.int(
        description='Number of maximum sensors in each generated grid.',
        spec={'type': 'integer', 'minimum': 1}
    )

    sky_matrix = Inputs.file(
        description='Path to a sky matrix.', path='sky.mtx',
        extensions=['mtx', 'smx']
    )

    sky_dome = Inputs.file(
        description='Path to a sky dome.', path='sky.dome'
    )

    sensor_grid = Inputs.file(
        description='Path to sensor grid files.', path='grid.pts',
        extensions=['pts']
    )

    scene_file = Inputs.file(
        description='Path to an octree file to describe the scene.', path='scene.oct',
        extensions=['oct']
    )

    @command
    def run_daylight_coeff(self):
        return 'honeybee-radiance dc scoeff scene.oct grid.pts sky.dome sky.mtx ' \
            '--sensor-count {{self.sensor_count}} --output results.ill --rad-params ' \
            '"{{self.radiance_parameters}}" --rad-params-locked '\
            '"{{self.fixed_radiance_parameters}}"'

    result_file = Outputs.file(description='Output result file.', path='results.ill')
