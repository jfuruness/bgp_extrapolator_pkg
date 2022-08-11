import csv
from pathlib import Path
import subprocess
from tempfile import TemporaryDirectory
from typing import Any, Dict, List
from unittest.mock import patch

import pytest

from bgp_simulator_pkg import Announcement
from bgp_simulator_pkg import EngineTester
from bgp_simulator_pkg import Relationships
from bgp_simulator_pkg import SimulationEngine
from caida_collector_pkg import CaidaCollector

from ..enums import Tiebreaking
from ..enums import TimestampComparison
from ..extrapolator import Extrapolator


@pytest.fixture(scope="session", autouse=True)
def install_extrapolator():
    """Installs extrapolator before tests run"""

    Extrapolator().install()


#####################
# Engine test funcs #
#####################


# https://stackoverflow.com/a/40673918/8903959
@pytest.fixture(scope="session", autouse=True)
def open_pdf(view):
    """Runs at the end of all tests"""

    # Setup stuff
    yield
    # Teardown stuff (open PDF for viewing)
    if view:
        # https://stackoverflow.com/q/19453338/8903959
        dir_ = Path(__file__).parent / "engine_tests"
        path = dir_ / "engine_test_outputs" / "aggregated_diagrams.pdf"
        subprocess.call(["xdg-open", str(path)])


@pytest.fixture(scope="session")
def view(pytestconfig):
    return pytestconfig.getoption("view")


@pytest.fixture(scope="session")
def overwrite(pytestconfig):
    return pytestconfig.getoption("overwrite")


# https://stackoverflow.com/a/66597438/8903959
def pytest_addoption(parser):
    parser.addoption("--view", action="store_true", default=False)
    parser.addoption("--overwrite", action="store_true", default=False)


#################################
# Simulation Engine Patch funcs #
#################################

CAIDA_TSV_PATH = Path("/tmp/exr_caida.tsv")


def _caida_run_patch(*args, **kwargs):
    """Patches the caida collector run to always write to a specific TSV"""

    kwargs["tsv_path"] = CAIDA_TSV_PATH

    return CaidaCollector.run(*args, **kwargs)


def _get_ann_rows(self) -> List[Dict[str, Any]]:
    """Converts all announcements into exr input"""

    ann_rows = list()
    prefix_ids = dict()
    for as_obj in self:
        for prefix, ann in as_obj._local_rib.prefix_anns():

            # Convert roa validity to a number the exr will understand
            if ann.invalid_by_roa:
                roa_validity = 2
            elif ann.valid_by_roa:
                roa_validity = 0
            elif ann.unknown_by_roa:
                roa_validity = 1
            else:
                raise NotImplementedError

            # Get prefix_id
            prefix_ids[prefix] = prefix_ids.get(prefix, len(prefix_ids) + 0)

            ann_rows.append({"prefix": prefix,
                             "as_path": "{" + ",".join(
                                str(x) for x in ann.as_path) + "}",
                             "timestamp": ann.timestamp,
                             "origin": ann.origin,
                             # Valid = 0, unknown = 1, invalid = 2
                             "roa_validity": roa_validity,
                             "prefix_id": prefix_ids[prefix],
                             "block_id": 0,
                             "prefix_block_id": prefix_ids[prefix]})
    return ann_rows


def _write_ann_rows(ann_rows, ann_path):
    """Writes announcement rows to path"""

    with ann_path.open("w") as f:
        writer = csv.DictWriter(f,
                                fieldnames=list(ann_rows[0].keys()),
                                delimiter="\t")
        writer.writeheader()
        writer.writerows(ann_rows)


def _run_exr(ann_path: Path, out_path: Path):
    """Runs extrapolator for tests"""

    Extrapolator().run(install=False,
                       # Path to file of annoucements to seed engine with
                       announcements=ann_path,
                       # BGP Topology for engine. If blank, use Caida
                       bgp_topology=CAIDA_TSV_PATH,
                       # Output for results
                       output=out_path,
                       # Propagation configurations
                       stub_removal=False,
                       # Seed only at the origin
                       origin_only_seeding=True,
                       # What wins ties after AS Path length
                       tiebreaking=Tiebreaking.LOWEST_ASN_WINS.value,
                       # Unclear as to what this affects
                       timestamp_comp=TimestampComparison.NEWER_WINS.value,
                       # Empty to dump all ASNS
                       rib_dump_asns=())


def _populate_sim_engine_w_exr_results(self, out_path: Path):
    # Read the results back in
    with out_path.open() as f:
        for row in csv.DictReader(f, delimiter="\t"):
            # Determine AS path
            as_path_str = row["as_path"].replace("{", "").replace("}", "")
            as_path = tuple([int(x) for x in as_path_str.split(",")])
            # Set roa_valid_length to be roa_validity
            if row["roa_validity"] == 2:
                roa_valid_length = False
            else:
                roa_valid_length = True

            ann = Announcement(row["prefix"],
                               as_path=as_path,
                               timestamp=int(row["timestamp"]),
                               seed_asn=None,
                               roa_valid_length=roa_valid_length,
                               # Always set to True
                               roa_origin=int(row["origin"]),
                               # Always set this to be origin for testing
                               recv_relationship=Relationships.ORIGIN,
                               withdraw=False,
                               traceback_end=False,
                               communities=())
            self.as_dict[as_path[-1]]._local_rib.add_ann(ann)


def _propagate_patch(self, *args, **kwargs):
    """Propagation patch for SimulationEngine

    This will allow the extrapolator to be integrated into the
    bgp_simulation_pkg's system test suite, which is very useful
    for testing simulations and specifically propagation and data
    plane traceback

    We do this by, instead of propagating:
    1. Dump SimulationEngine's relationships and seeded announcements
    2. Run the extrapolator on input from step 1
    3. Read in the extrapolator output into the SimulationEngine
    4. Continue as normal, tests should work
    """

    ann_rows = _get_ann_rows(self)
    with TemporaryDirectory() as tmp_dir:
        # Write CSV
        ann_path = Path(tmp_dir) / "ann.tsv"
        _write_ann_rows(ann_rows, ann_path)
        # Run extrapolator
        out_path = Path(tmp_dir) / "exr_output.tsv"
        _run_exr(ann_path, out_path)
        # Put results from extrapolator back in simulator
        _populate_sim_engine_w_exr_results(self, out_path)


@pytest.fixture(scope="function")
def ExtrapolatorEngineTesterCls():
    """Returns an engine tester cls that uses the extrapolator to run sims"""

    with patch.object(SimulationEngine, "_propagate", _propagate_patch):
        yield EngineTester
