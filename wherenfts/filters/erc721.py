import asyncio
import concurrent.futures
import logging
import sys
import time

from panoramix.decompiler import decompile_bytecode
from panoramix.utils.supplement import check_supplements
from web3.eth import AsyncEth

from wherenfts.ethereum.types import Transaction
from wherenfts.filters.base import Filter
from wherenfts.misc.logging import logger


class DecompilingERC721Filter(Filter):
    """Decompiles contract code and checks if it contains ERC721 markers."""

    _markers = [
        "erc721",
        "punk",
        "kitt",
    ]

    def __init__(
        self,
        eth: AsyncEth,
        recursion_limit: int = sys.getrecursionlimit(),
    ):
        super().__init__()
        self._eth = eth
        sys.setrecursionlimit(recursion_limit)
        self._executor = concurrent.futures.ProcessPoolExecutor()
        self._active_jobs = 0
        logging.getLogger("panoramix").setLevel(
            logging.CRITICAL
        )  # disable panoramix warnings
        check_supplements()  # decompress panoramix database in advance

    def __del__(self):
        self._executor.shutdown()

    def _check_contains_marker(self, text: str) -> bool:
        for marker in self._markers:
            if marker in text:
                return True
        return False

    async def handle(self, tx: Transaction) -> Transaction | None:
        contract = await self._eth.get_code(tx.receipt.contract_address)
        bytecode = contract.hex()
        loop = asyncio.get_running_loop()

        self._active_jobs += 1
        logger.debug(
            f"executor submit, {tx.receipt.contract_address=}, {self._active_jobs=}"
        )
        t1 = time.time()

        decompiled = await loop.run_in_executor(
            self._executor,
            decompile_bytecode,
            bytecode,
        )

        dt = time.time() - t1
        self._active_jobs -= 1
        logger.debug(
            f"executor complete, {tx.receipt.contract_address=}, {self._active_jobs=},"
            f" {dt=}"
        )

        if not self._check_contains_marker(decompiled.text.lower()):
            logger.info(f"rejected, {tx.receipt.contract_address=}")
            return
        logger.info(f"passed, {tx.receipt.contract_address=}")
        if self._next:
            return await self._next.handle(tx)
        return tx
