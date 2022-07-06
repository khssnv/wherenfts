from wherenfts.ethereum.types import Transaction
from wherenfts.filters.base import Filter


class ContractAddressPrinter(Filter):
    """Prints smart contract address transaction deployes and terminates filtering
    chain."""

    def __init__(self):
        super().__init__()

    async def handle(self, tx: Transaction) -> None:
        print(tx.receipt.contract_address)
