import pytest
from script import deploy
from moccasin.boa_tools import VyperContract


@pytest.fixture(scope="function")
def snek_contract() -> VyperContract:
    """
    @dev deploy snek contract fixture
    """
    return deploy.deploy()
