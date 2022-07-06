import asyncio
import signal
import sys
from collections.abc import AsyncGenerator

from web3 import AsyncHTTPProvider, Web3
from web3.eth import AsyncEth
from web3.net import AsyncNet

from wherenfts.ethereum.data import ethereum_blocks, ethereum_transactions
from wherenfts.ethereum.types import Transaction
from wherenfts.filters import (
    ContractAddressPrinter,
    ContractDeployment,
    DecompilingERC721Filter,
)
from wherenfts.filters.base import Filter
from wherenfts.misc.cli import get_cli_args
from wherenfts.misc.logging import logger

MAX_RECURSION = 10_000  # allow decompiler to use deeper recursion then default 1000


async def apply_filters(
    filtering: Filter,
    transactions_source: AsyncGenerator[Transaction],
) -> None:
    """Asyncronously schedules `filtering` filter on `transaction_source` generated
    transactions.

    Parameters
    ----------
    filtering : Filter
        A filter or a chain of filters.
    transactions_source : AsyncGenerator[Transaction]
    """

    async for tx in transactions_source:
        asyncio.create_task(filtering.handle(tx))


async def main():
    args = get_cli_args()

    logger.info("starting")

    w3 = Web3(
        AsyncHTTPProvider(args.eth_http_provider),
        modules={
            "eth": (AsyncEth,),
            "net": (AsyncNet,),
        },
        middlewares=[],
    )
    eth: AsyncEth = w3.eth

    # Create filtering chain
    logger.info("prepating filters data, it may take a minute")
    contract_deployment_filter = ContractDeployment()
    decompiling_erc721_filter = DecompilingERC721Filter(eth, MAX_RECURSION)
    contract_address_printer_filter = ContractAddressPrinter()
    contract_deployment_filter.set_next(decompiling_erc721_filter).set_next(
        contract_address_printer_filter
    )
    filters = contract_deployment_filter

    # Setup data producers
    start_from_block_number = (
        args.from_block if args.from_block is not None else await eth.get_block_number()
    )
    blocks_source = ethereum_blocks(eth, start_from_block_number, args.finality_delay)
    transactions_source = ethereum_transactions(eth, blocks_source)
    erc721_printer = apply_filters(filters, transactions_source)

    # Run processing
    task = asyncio.create_task(erc721_printer)
    await task


if __name__ == "__main__":
    # Suppress printing stacktrace
    signal.signal(signal.SIGINT, lambda a, b: sys.exit(0))

    asyncio.run(main())
