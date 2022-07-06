from wherenfts.ethereum.types import Transaction
from wherenfts.filters.base import Filter
from wherenfts.misc.logging import logger


class ContractDeployment(Filter):
    """Passes transactions with smart contract deployment only."""

    def __init__(self):
        super().__init__()

    async def handle(self, tx: Transaction) -> Transaction | None:
        if not tx.receipt.contract_address:
            return None
        logger.info(f"passed, {tx.receipt.contract_address=}")
        if self._next:
            return await self._next.handle(tx)
        return tx
