import json
from multiprocessing import cpu_count
from pathlib import Path
from subprocess import check_call
from tempfile import TemporaryDirectory
from typing import Optional
from typing import Tuple

from caida_collector_pkg import CaidaCollector

from .enums import Tiebreaking
from .enums import TimestampComparison


class Extrapolator:
    """Extrapolator that uses Sam's extrapolator engine"""

    def __init__(self,
                 repo_name: str = "BGPExtrapolator",
                 install_dir: Optional[Path] = None,
                 branch: Optional[str] = None,
                 git_url: str = "git@github.com:Same4254/BGPExtrapolator.git",
                 executable_name: str = "BGPExtrapolator"):

        self._install_dir: Path = install_dir if install_dir else Path("/tmp/")

        # Repo info
        self._branch: Optional[str] = branch
        self._repo_name: str = repo_name
        self._git_url: str = git_url
        self._executable_name: str = executable_name

#############
# Run Funcs #
#############

    def run(self,
            install: bool = True,
            # config options
            # Path to file of annoucements to seed engine with
            announcements: Optional[Path] = None,
            # BGP Topology for engine. If blank, use Caida
            bgp_topology: Optional[Path] = None,
            # Output for results
            output: Path = Path("/tmp/extrapolator_results.tsv"),
            # Propagation configurations
            # If true, assume stubs local rib are the same as parents
            stub_removal: bool = False,
            # Seed only at the origin
            origin_only_seeding: bool = False,
            # What wins ties after AS Path length
            tiebreaking: str = Tiebreaking.LOWEST_ASN_WINS.value,
            # Unclear as to what this affects
            timestamp_comp: str = TimestampComparison.NEWER_WINS.value,
            # List of ASNs to dump the local RIB. Empty will dump everything
            rib_dump_asns: Tuple[int, ...] = tuple()
            ) -> None:
        """Runs the extrapolator engine"""

        # Install the extrapolator engine
        if install:
            self.install()

        # Default announcements file
        if not announcements:
            announcements = (self._repo_path / self._repo_name /
                             "TestCases" / "RealData-Announcements.tsv")

        # If there is no default relationship file, run the Caida collector
        if not bgp_topology:
            bgp_topology = Path("/tmp/caida_collector.tsv")
            CaidaCollector().run(tsv_path=bgp_topology)

        with TemporaryDirectory() as tmp_dir:
            config_path = Path(tmp_dir) / "extrapolator_config.json"
            # Writes config options to a JSON
            self._write_config(config_path,
                               Announcements=str(announcements),
                               Relationships=str(bgp_topology),
                               Output=str(output),
                               Stub_Removal=stub_removal,
                               Origin_Only=origin_only_seeding,
                               Tiebreaking_Method=tiebreaking,
                               Timestamp_Comparison_Method=timestamp_comp,
                               Control_Plane_Traceback_ASNs=list(rib_dump_asns)
                               )

            self._run_engine(config_path)

    def _write_config(self, config_path: Path, **config_kwargs):
        """Writes config to config path

        For explanations of args, see run func parameters
        """

        with config_path.open("w") as f:
            json.dump(config_kwargs, f, indent=4)

    def _run_engine(self, config_path: Path):
        """Runs the extrapolator engine"""

        # Run the BGP Extrapolator Engine
        check_call(f"{self._executable_path} --config {config_path}",
                   shell=True)

#################
# Install funcs #
#################

    def install(self):
        """Installs the extrapolator"""

        # Clone repo and install deps
        self._install_deps()
        # Switch to proper branch
        self._switch_extrapolator_engine_branch()
        # Build
        self._build_extrapolator_engine()

    def _install_deps(self):
        """Install dependencies"""

        # If the path to the repo doesn't exist, clone it
        if not self._repo_path.exists():
            # TODO: really shouldn't install cmake to the system
            check_call("pip3 install cmake", shell=True)

            cmd = (f"cd {self._install_dir} && "
                   f"git clone {self._git_url}")
            check_call(cmd, shell=True)

    def _switch_extrapolator_engine_branch(self):
        """Switches branch of extrapolator engine"""

        # Checkout the proper branch if desired
        if self._branch:
            check_call(f"cd {self._repo_path} && git checkout {self._branch}",
                       shell=True)

    def _build_extrapolator_engine(self):
        """Build extrapolator engine"""

        cmds = (f"cd {self._repo_path}",
                "mkdir -p build",
                "cd build",
                "cmake -D CMAKE_BUILD_TYPE=RelWithDebInfo ..",
                f"make -j {cpu_count()}")
        check_call(" && ".join(cmds), shell=True)

    @property
    def _repo_path(self) -> Path:
        """Returns the path to the repo"""

        return self._install_dir / self._repo_name

    @property
    def _executable_path(self) -> Path:
        """Returns the path to the executable"""

        return self._repo_path / "build" / self._executable_name
