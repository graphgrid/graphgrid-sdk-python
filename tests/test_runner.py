"""Define methods to run tests and configure test output"""
import os
import subprocess
from pathlib import Path
from clover.coverage2clover import Clover, Cobertura


def main():
    """Run the test suite"""
    top_level_dir = Path(__file__).parent.parent.absolute()
    test_dir = os.path.join(top_level_dir, "tests")
    pytest_path = os.path.join(test_dir, "pytest.xml")
    cov_path = os.path.join(test_dir, "cov.xml")
    clover_path = os.path.join(test_dir, "clover.xml")
    coveragerc_path = os.path.join(top_level_dir, ".coveragerc")
    subprocess.check_call("pytest"
                          " --junitxml=" + pytest_path +
                          " --cov-report xml:" + cov_path +
                          " --cov=" + str(top_level_dir) +
                          " --cov-config=" + coveragerc_path +
                          " " + test_dir, shell=True)
    cov = Cobertura()
    cov.open(cov_path)
    cl = Clover(cov)
    cl.export(clover_path)


if __name__ == '__main__':
    main()
