import pytest


@pytest.mark.skip(reason="Leaving for EXR team if they choose to do them")
class TestExtrapolator:
    def test_run(self):
        """Tests run func under various circumstances"""

        raise NotImplementedError

    def test_write_config(self):
        """Tests that a config gets written correctly"""

        raise NotImplementedError

    def test_run_engine(self):
        """Tests that the engine is run correctly"""

        raise NotImplementedError

    def test_install(self):
        """Ensure that the engine is installed properly"""

        raise NotImplementedError

    def test_install_deps(self, tmp_path):
        """Tests that repo gets cloned into proper dir"""

        raise NotImplementedError

    def test_switch_extrapolator_engine_branch(self):
        """Tests that extrapolator engine branch switches properly"""

        raise NotImplementedError

    def test_build_extrapolator_engine(self):
        """Tests extrapolator engine build"""

        raise NotImplementedError
