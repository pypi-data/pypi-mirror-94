from dataclasses import dataclass
from pollination_dsl.function import Function, command, Inputs, Outputs


@dataclass
class AddRemoveSkyMatrix(Function):
    """Remove direct sky from total sky and add direct sun."""

    total_sky_matrix = Inputs.file(
        description='Path to matrix for total sky contribution.',
        path='sky.ill', extensions=['ill', 'dc']
    )

    direct_sky_matrix = Inputs.file(
        description='Path to matrix for direct sky contribution.',
        path='sky_dir.ill', extensions=['ill', 'dc']
    )

    sunlight_matrix = Inputs.file(
        description='Path to matrix for direct sunlight contribution.',
        path='sun.ill', extensions=['ill', 'dc']
    )

    @command
    def create_matrix(self):
        return 'rmtxop sky.ill + -s -1.0 sky_dir.ill + sun.ill > final.ill'

    results_file = Outputs.file(description='Radiance matrix file.', path='final.ill')


@dataclass
class AddRemoveSkyMatrixWithConversion(AddRemoveSkyMatrix):
    """Remove direct sky from total sky and add direct sun."""
    conversion = Inputs.str(
        description='conversion as a string which will be passed to -c',
        default='47.4 119.9 11.6'
    )

    output_format = Inputs.str(
        default='-fa',
        spec={'type': 'string', 'enum': ['-fa', '-fd']}
    )

    @command
    def create_matrix(self):
        return 'rmtxop {{self.output_format}} sky.ill + -s -1.0 sky_dir.ill + sun.ill ' \
            '-c {{self.conversion}} | getinfo - > final.ill'


@dataclass
class GenSkyWithCertainIllum(Function):
    """Generates a sky with certain illuminance level."""

    illuminance = Inputs.float(
        default=100000,
        description='Sky illuminance level.'
    )

    @command
    def gen_overcast_sky(self):
        return 'honeybee-radiance sky illuminance {{self.illuminance}} --name overcast.sky'

    sky = Outputs.file(description='Generated sky file.', path='overcast.sky')


@dataclass
class CreateSkyDome(Function):
    """Create a skydome for daylight coefficient studies."""

    @command
    def gen_sky_dome(self):
        return 'honeybee-radiance sky skydome --name rflux_sky.sky'

    sky_dome = Outputs.file(
        description='A sky hemisphere with ground.', path='rflux_sky.sky'
    )


@dataclass
class CreateSkyMatrix(Function):
    """Generate a sun-up sky matrix."""

    north = Inputs.int(
        description='An angle for north direction. Default is 0.',
        default=0, spec={'type': 'integer', 'maximum': 360, 'minimum': 0}
    )

    sky_component = Inputs.str(
        description='A switch for generating sun-only using -d or exclude sun '
        'contribution using -s. The default is an empty string for including both.',
        default=' ', spec={'type': 'string', 'enum': ['-s', '-d', ' ']}
    )

    wea = Inputs.file(
        description='Path to a wea file.', extensions=['wea'], path='sky.wea'
    )

    @command
    def generate_sky_matrix(self):
        return 'gendaymtx -u -O0 -r {{self.north}} -v {{self.sky_component}} sky.wea > sky.mtx'

    sky_matrix = Outputs.file(description='Output Sky matrix', path='sky.mtx')
