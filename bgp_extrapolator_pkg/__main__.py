from pathlib import Path
from bgp_simulator_pkg import Simulation


def main():
    """Runs the defaults"""

    raise NotImplementedError
    Simulation(output_path=Path("~/Desktop/graphs").expanduser()).run()


if __name__ == "__main__":
    main()
