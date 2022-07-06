import asyncio
import time
from collections.abc import AsyncGenerator

from web3.eth import AsyncEth

from wherenfts.ethereum.types import Block, Receipt, Transaction
from wherenfts.misc.logging import logger


async def ethereum_transactions(
    eth: AsyncEth,
    blocks_source: AsyncGenerator[Block],
    batch_size: int = 100,
) -> AsyncGenerator[Transaction]:
    """Ethereum transactions asyncronous generator.

    Parameters
    ----------
    eth : AsyncEth
        Instantiated Ethereum RPC adapter.
    blocks_source : AsyncGenerator[Block]
        Ethereum blocks producer.
    batch_size : int, optional
        Limit on numbers of transactions to request from RPC node at the same time, by
        default 100.

    Yields
    ------
    Iterator[AsyncGenerator[Transaction]]
    """

    async for block in blocks_source:
        for idx in range(0, len(block.transactions), batch_size):
            receipts = await asyncio.gather(
                *[
                    eth.get_transaction_receipt(tx_hash)
                    for tx_hash in block.transactions[idx : idx + batch_size]
                ]
            )
            txs = [
                Transaction(receipt=Receipt.from_rpc(receipt)) for receipt in receipts
            ]
            for tx in txs:
                yield tx


async def ethereum_blocks(
    eth: AsyncEth,
    from_block: int,
    finality_delay: int,
    polling_period: int = 3,
) -> AsyncGenerator[Block]:
    """Continuous Ethereum blocks asyncronous generator.

    Parameters
    ----------
    eth : AsyncEth
        Instantiated Ethereum RPC adapter.
    from_block : int
        Block number to start with.
    finality_delay : int
        Depth of the block to consider it immutable and ready for producing. Recommended
        value is 6. Check more at
        https://ethereum.org/en/developers/docs/consensus-mechanisms/pow/#finality.
    polling_period : int, optional
        How many seconds to wait before querying RPC node for a new block, by default 3
        seconds.

    Yields
    ------
    Iterator[AsyncGenerator[Block]]
    """

    current = from_block
    logger.info(f"starting blocks producer, {from_block=}, {finality_delay=}")
    while True:
        t1 = time.time()
        latest = await eth.get_block_number()
        logger.info(f"{latest=}, {current=}")
        if latest - current >= finality_delay:
            block = await eth.get_block(current)
            current = block["number"] + 1
            yield Block.from_rpc(block)
        dt = time.time() - t1
        await asyncio.sleep(polling_period - dt)
