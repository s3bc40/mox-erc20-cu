"""
@notice Workshop invariant cu: the goal to assert that totalSupply
is always equal to the sum of all balances. And there is an intentional
mistake in super_mint function.
"""

from contracts import snek_token
from hypothesis import assume, settings
from hypothesis.stateful import (
    RuleBasedStateMachine,
    initialize,
    rule,
    invariant,
)
from hypothesis.strategies import integers
from boa.test.strategies import strategy
from script.deploy import INITIAL_SUPPLY
from eth.constants import UINT_256_MAX
import boa

NB_ADDRESSES = 10


class InvariantSnekToken(RuleBasedStateMachine):
    def __init__(self):
        super().__init__()

    # @dev tried to implement Bundle but not adapted here
    # addresses = Bundle("addresses")

    @initialize()
    def init_addresses(self):
        print("Deployed contract with addresses")
        self.contract = snek_token.deploy(INITIAL_SUPPLY)
        self.addresses = [boa.env.generate_address() for i in range(NB_ADDRESSES)]

    @rule(amount=strategy("uint256"), id_seed=integers(0, NB_ADDRESSES - 1))
    def mint(self, amount, id_seed):
        # like an assert as a bad example but does not trigger an error
        assume(self.contract.totalSupply() + amount < UINT_256_MAX)
        addr = self.addresses[id_seed]
        self.contract.mint(addr, amount)

    @rule(id_seed=integers(0, NB_ADDRESSES - 1))
    def super_mint(self, id_seed):
        addr = self.addresses[id_seed]
        with boa.env.prank(addr):
            self.contract.super_mint()

    @invariant()
    def user_balance_should_never_exceed_total_supply(self):
        total_supply = self.contract.totalSupply()
        for address in self.addresses:
            balance = self.contract.balanceOf(address)
            assert (
                balance <= total_supply
            ), f"Address {address} balance exceeds total supply"


invariant_snek_token = InvariantSnekToken.TestCase

invariant_snek_token.settings = settings(max_examples=10000, stateful_step_count=50)
