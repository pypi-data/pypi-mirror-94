from typing import Dict

import attr

from terra_sdk.core import AccAddress, Coins, ValAddress

from ._base import BaseAPI


@attr.s
class Rewards:
    rewards: Dict[ValAddress, Coins] = attr.ib()
    total: Coins = attr.ib()


@attr.s
class ValidatorRewards:
    self_bond_rewards: Coins = attr.ib()
    val_commission: Coins = attr.ib()


class AsyncDistributionAPI(BaseAPI):
    async def rewards(self, delegator: AccAddress) -> Rewards:
        res = await self._c._get(f"/distribution/delegators/{delegator}/rewards")
        return Rewards(
            rewards={
                item["validator_address"]: Coins.from_data(item["reward"] or [])
                for item in res["rewards"]
            },
            total=Coins.from_data(res["total"]),
        )

    async def validator_rewards(self, validator: ValAddress) -> ValidatorRewards:
        res = await self._c._get(f"/distribution/validators/{validator}")
        return ValidatorRewards(
            self_bond_rewards=Coins.from_data(res["self_bond_rewards"]),
            val_commission=Coins.from_data(res["val_commission"]),
        )

    async def withdraw_address(self, delegator: AccAddress) -> AccAddress:
        return await self._c._get(
            f"/distribution/delegators/{delegator}/withdraw_address"
        )

    async def community_pool(self) -> Coins:
        res = await self._c._get("/distribution/community_pool")
        return Coins.from_data(res)

    async def parameters(self) -> dict:
        return await self._c._get("/distribution/parameters")


class DistributionAPI(BaseAPI):
    def rewards(self, delegator: AccAddress) -> Rewards:
        """Fetches the staking reward data for a delegator.

        Args:
            delegator (AccAddress): delegator account address

        Returns:
            Rewards: delegator rewards
        """
        res = self._c._get(f"/distribution/delegators/{delegator}/rewards")
        return Rewards(
            rewards={
                item["validator_address"]: Coins.from_data(item["reward"] or [])
                for item in res["rewards"]
            },
            total=Coins.from_data(res["total"]),
        )

    def validator_rewards(self, validator: ValAddress) -> ValidatorRewards:
        """Fetches the commission reward data for a validator.

        Args:
            validator (ValAddress): validator operator address

        Returns:
            ValidatorRewards: validator rewards
        """
        res = self._c._get(f"/distribution/validators/{validator}")
        return ValidatorRewards(
            self_bond_rewards=Coins.from_data(res["self_bond_rewards"]),
            val_commission=Coins.from_data(res["val_commission"]),
        )

    def withdraw_address(self, delegator: AccAddress) -> AccAddress:
        """Fetches the withdraw address associated with a delegator.

        Args:
            delegator (AccAddress): delegator account address

        Returns:
            AccAddress: withdraw address
        """
        return self._c._get(f"/distribution/delegators/{delegator}/withdraw_address")

    def community_pool(self) -> Coins:
        """Fetches the community pool.

        Returns:
            Coins: community pool
        """
        res = self._c._get("/distribution/community_pool")
        return Coins.from_data(res)

    def parameters(self) -> dict:
        """Fetches the Distribution module parameters.

        Returns:
            dict: Distribution module parameters
        """
        return self._c._get("/distribution/parameters")
