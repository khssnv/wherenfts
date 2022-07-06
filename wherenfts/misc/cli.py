import argparse


def get_cli_args():
    cli = argparse.ArgumentParser(
        description="Prints addresses of newly created ERC721 smart contracts",
    )

    cli.add_argument(
        "--http",
        required=True,
        dest="eth_http_provider",
        help="HTTP endpoint of an Ethereum node RPC",
    )

    cli.add_argument(
        "--finality",
        dest="finality_delay",
        type=int,
        default=6,
        help=(
            "number of blocks to wait before retrieving a block for processing, 6 by"
            " default"
        ),
    )

    cli.add_argument(
        "--from-block",
        dest="from_block",
        type=int,
        default=None,
        help="block number to start from, most recent by refault",
    )

    return cli.parse_args()
