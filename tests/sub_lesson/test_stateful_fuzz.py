from hypothesis.stateful import RuleBasedStateMachine, rule
from hypothesis import settings
from contracts.sub_lesson import stateful_fuzz_solvable
from boa.test.strategies import strategy


class StatefulFuzzer(RuleBasedStateMachine):
    def __init__(self):
        super().__init__()
        self.contract = stateful_fuzz_solvable.deploy()
        print(f"    Deployed contract")

    # "Rule" -> Actions and can have props/invariants
    # Invariants -> props that must be true
    @rule(new_number=strategy("uint256"))
    def change_number(self, new_number):
        self.contract.change_number(new_number)
        print(f"    Change number with {new_number}")

    @rule(input=strategy("uint256"))
    def input_number_returns_itself(self, input):
        response = self.contract.always_returns_input_number(input)
        assert response == input, f"Expected {input} but got {response}"


TestStatefulFuzzing = StatefulFuzzer.TestCase

TestStatefulFuzzing.settings = settings(max_examples=10000, stateful_step_count=50)
