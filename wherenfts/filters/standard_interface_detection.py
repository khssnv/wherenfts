import os
from pathlib import Path

from web3.contract import AsyncContract
from web3.eth import AsyncEth
from web3.exceptions import BadFunctionCallOutput, ContractLogicError

from wherenfts.ethereum import abi
from wherenfts.ethereum.types import Transaction
from wherenfts.filters.base import Filter
from wherenfts.misc.logging import logger

ERC165_IDS = {
    "ERC721": "0x80ac58cd",
}


class StandardInterfaceDetection(Filter):
    """Utilizes ERC-165 standard interface detection to pass contracts that explicitly
    unveil standard interface they implement. See
    https://eips.ethereum.org/EIPS/eip-165 for more details.
    """

    def __init__(
        self,
        eth: AsyncEth,
        interface_id: str,
    ):
        super().__init__()
        self._eth = eth
        self.interface_id = interface_id

        abi_path = Path(os.path.dirname(abi.__file__)) / Path("ERC165.json")
        with open(abi_path, "r") as fd:
            self._abi = fd.read()

    @classmethod
    def get_erc165_identifier_by_standard(cls, standard: str) -> str:
        return ERC165_IDS[standard]

    async def handle(self, tx: Transaction) -> Transaction | None:
        contract: AsyncContract = self._eth.contract(
            address=tx.receipt.contract_address,
            abi=self._abi,
        )

        try:
            is_target_contract = await contract.functions.supportsInterface(
                self.interface_id
            ).call()
        except (BadFunctionCallOutput, ContractLogicError):
            is_target_contract = False

        if not is_target_contract:
            logger.info(f"rejected, {tx.receipt.contract_address=}")
            return

        logger.info(f"passed, {tx.receipt.contract_address=}")
        if self._next:
            return await self._next.handle(tx)
        return tx
