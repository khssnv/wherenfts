from dataclasses import dataclass


@dataclass
class Receipt:
    contract_address: str

    @classmethod
    def from_rpc(cls, resp: dict) -> "Receipt":
        return cls(
            contract_address=resp["contractAddress"],
        )


@dataclass
class Transaction:
    receipt: Receipt | None = None


@dataclass
class Block:
    number: int
    transactions: list[str]

    @classmethod
    def from_rpc(cls, resp: dict) -> "Block":
        return cls(
            number=resp["number"],
            transactions=resp["transactions"],
        )
