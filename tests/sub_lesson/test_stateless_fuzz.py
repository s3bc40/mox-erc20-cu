import pytest
from contracts.sub_lesson import stateless_fuzz_solvable
from hypothesis import given, settings, HealthCheck
from boa.test.strategies import strategy


@pytest.fixture(scope="session")
def contract():
    return stateless_fuzz_solvable.deploy()


# @dev if pass int then bounded from 0 to infinity
# @dev becareful with using decorator settings -> learning purpose
@settings(max_examples=1000, suppress_health_check=[HealthCheck.function_scoped_fixture])
@given(input=strategy("uint256"))  # 0, MaxUint256
def test_always_return_input(contract, input):
    print(input)
    assert contract.always_returns_input_number(input) == input
