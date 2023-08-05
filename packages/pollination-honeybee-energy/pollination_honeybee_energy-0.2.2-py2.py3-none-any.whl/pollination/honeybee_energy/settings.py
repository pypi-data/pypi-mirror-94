from dataclasses import dataclass
from pollination_dsl.function import Inputs, Outputs, Function, command


@dataclass
class SimParDefault(Function):
    """Get a SimulationParameter JSON with default outputs for energy use only."""

    ddy = Inputs.file(
        description='A DDY file with design days to be included in the '
        'SimulationParameter', path='input.ddy', extensions=['ddy']
    )

    filter_des_days = Inputs.str(
        description='A switch for whether the ddy-file should be filtered to only '
        'include 99.6 and 0.4 design days', default='filter-des-days',
        spec={'type': 'string', 'enum': ['filter-des-days', 'all-des-days']}
    )

    @command
    def create_sim_param(self):
        return 'honeybee-energy settings default-sim-par input.ddy ' \
            '--{{self.filter_des_days}} --output-file sim_par.json'

    sim_par_json = Outputs.file(
        description='SimulationParameter JSON with default outputs for energy use',
        path='sim_par.json'
    )


@dataclass
class SimParLoadBalance(SimParDefault):
    """Get a SimulationParameter JSON with all outputs for constructing load balances."""

    load_type = Inputs.str(
        description='Text to indicate the type of load. Choose from (Total, Sensible, '
        'Latent, All)', default='Total',
        spec={'type': 'string', 'enum': ['Total', 'Sensible', 'Latent', 'All']}
    )

    @command
    def create_sim_param(self):
        return 'honeybee-energy settings load-balance-sim-par input.ddy --load-type ' \
            '{{self.load_type}} --{{self.filter_des_days}} --output-file sim_par.json'


@dataclass
class SimParComfort(SimParDefault):
    """Get a SimulationParameter JSON with all outputs for thermal comfort mapping."""

    @command
    def create_sim_param(self):
        return 'honeybee-energy settings comfort-sim-par input.ddy ' \
            '--{{self.filter_des_days}} --output-file sim_par.json'


@dataclass
class BaselineOrientationSimPars(Function):
    """Get SimulationParameters with different north angles for a baseline building sim.
    """

    ddy = Inputs.file(
        description='A DDY file with design days to be included in the '
        'SimulationParameter', path='input.ddy', extensions=['ddy']
    )

    filter_des_days = Inputs.str(
        description='A switch for whether the ddy-file should be filtered to only '
        'include 99.6 and 0.4 design days', default='filter-des-days',
        spec={'type': 'string', 'enum': ['filter-des-days', 'all-des-days']}
    )

    @command
    def baseline_orientation_sim_pars(self):
        return 'honeybee-energy settings orientation-sim-pars input.ddy ' \
            '0 90 180 270 --{{self.filter_des_days}} --folder output ' \
            '--log-file output/sim_par_info.json'

    sim_par_list = Outputs.dict(
        description='A JSON array that includes information about generated simulation '
        'parameters.', path='output/sim_par_info.json'
    )

    output_folder = Outputs.folder(
        description='Output folder with the simulation parameters.', path='output'
    )
