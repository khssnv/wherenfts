Where NFTs?
===========

A CLI tool to watch for ERC721 contracts deployments to Ethereum.

Usage
-----

Print new ERC721 contracts addresses only to stdout.

```console
$ docker run -it ghcr.io/khssnv/wherenfts:main --http "https://mainnet.infura.io/v3/bd4ed15ff9c24b37bd46e05230f13ab0"
0xDFd3921769EF776348139888c4f7C5373A554549
0x588715D043901028A2898539E02e38d2fca68C79
...
```

You can pass `LOGURU_LEVEL=INFO` environment variable to see how it queires each block and tries to find ERC721-like contract.

```console
$ docker run -e LOGURU_LEVEL=INFO -it ghcr.io/khssnv/wherenfts:main --http "https://mainnet.infura.io/v3/bd4ed15ff9c24b37bd46e05230f13ab0"
2022-07-06 15:38:06.256 | INFO     | __main__:main:42 - starting
2022-07-06 15:38:06.257 | INFO     | __main__:main:57 - prepating filter data, it may take a minute
2022-07-06 15:38:18.147 | INFO     | wherenfts.ethereum.data:ethereum_blocks:72 - starting blocks producer, from_block=15089797, finality_delay=6
2022-07-06 15:38:18.334 | INFO     | wherenfts.ethereum.data:ethereum_blocks:76 - latest=15089797, current=15089797
2022-07-06 15:38:21.353 | INFO     | wherenfts.ethereum.data:ethereum_blocks:76 - latest=15089797, current=15089797
2022-07-06 15:38:24.386 | INFO     | wherenfts.ethereum.data:ethereum_blocks:76 - latest=15089797, current=15089797
...
```

Other options are following.

```console
$ docker run -it ghcr.io/khssnv/wherenfts:main --help
usage: wherenfts --http ETH_HTTP_PROVIDER [--finality FINALITY_DELAY] [--from-block FROM_BLOCK]

Prints addresses of newly created ERC721 smart contracts.

options:
  -h, --help            show this help message and exit
  --http ETH_HTTP_PROVIDER
                        HTTP endpoint of an Ethereum node RPC.
  --finality FINALITY_DELAY
                        Number of blocks to wait before retrieving a block for processing.
  --from-block FROM_BLOCK
                        Block number to start from. Most recent by refault.
```
