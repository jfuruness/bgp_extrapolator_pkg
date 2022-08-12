from pathlib import Path

import pytest

from bgp_simulator_pkg import Config001
from bgp_simulator_pkg import Config002
from bgp_simulator_pkg import Config003
from bgp_simulator_pkg import Config004
from bgp_simulator_pkg import Config005
from bgp_simulator_pkg import Config006
from bgp_simulator_pkg import Config007
from bgp_simulator_pkg import Config008
from bgp_simulator_pkg import Config009
from bgp_simulator_pkg import Config010
from bgp_simulator_pkg import Config011
from bgp_simulator_pkg import Config012
from bgp_simulator_pkg import Config013
from bgp_simulator_pkg import Config014
from bgp_simulator_pkg import Config015
from bgp_simulator_pkg import Config016
from bgp_simulator_pkg import Config017
from bgp_simulator_pkg import Config018
from bgp_simulator_pkg import Config019
from bgp_simulator_pkg import Config020
from bgp_simulator_pkg import Config021
from bgp_simulator_pkg import Config022
from bgp_simulator_pkg import Config023
from bgp_simulator_pkg import Config024
from bgp_simulator_pkg import Config025
from bgp_simulator_pkg import Config026
from bgp_simulator_pkg import Config027
from bgp_simulator_pkg import Config028
from bgp_simulator_pkg import Config029
from bgp_simulator_pkg import Config030
from bgp_simulator_pkg import Config031
from bgp_simulator_pkg import Config032
from bgp_simulator_pkg import Config033
from bgp_simulator_pkg import Config034
from bgp_simulator_pkg import EngineTestConfig


BGP_CONFIGS = [Config001,
               Config002,
               Config003,
               Config004,
               Config009,
               Config010,
               Config011,
               Config012,
               Config013,
               Config014,
               Config015,
               Config016,
               Config019,
               Config020,
               Config023,
               Config024,
               Config027,
               Config028]
ROV_CONFIGS = [Config005,
               Config006,
               Config007,
               Config008,
               Config017,
               Config018,
               Config021,
               Config022,
               Config025,
               Config026]
WONT_WORK_DONT_INCLUDE = [Config029,
                          Config030,
                          Config031,
                          Config032,
                          Config033,
                          Config034]


@pytest.mark.engine
class TestEngine:
    """Performs a system test on the engine

    See README of bgp_simulator_pkg for in depth details
    """

    @pytest.mark.parametrize("conf", BGP_CONFIGS)
    def test_engine(self,
                    conf: EngineTestConfig,
                    overwrite: bool,
                    # Engine tester that is patched with extrapolator
                    ExtrapolatorEngineTesterCls):
        """Performs a system test on the engine

        See README of bgp_simulator_pkg for in depth details
        """

        ExtrapolatorEngineTesterCls(base_dir=self.base_dir,
                                    conf=conf,
                                    overwrite=overwrite).test_engine()

    @property
    def base_dir(self) -> Path:
        """Returns test output dir"""

        return Path(__file__).parent / "engine_test_outputs"
