from abc import ABC, abstractmethod

from wherenfts.ethereum.types import Transaction
from wherenfts.misc.logging import logger


class Filter(ABC):
    """Ethereum transactions filter with chaining support."""

    def __init__(self):
        self._next: Filter | None = None

    def set_next(self, handler: "Filter") -> "Filter":
        """Set the next filter which will receive a transaction complies filtring conditions.

        Parameters
        ----------
        handler : Filter
            Another filter.

        Returns
        -------
        Filter
            The same handler argument to chain another one after it.
        """

        logger.debug(f"filter={type(self).__name__}, next={type(handler).__name__}")
        self._next = handler
        return handler

    @abstractmethod
    async def handle(self, candidate: Transaction) -> Transaction | None:
        """Transaction processing implementation. Child classes should implement
        processing logic and pass candidate to the next filter in the chain or drop
        the candidate.

        Parameters
        ----------
        candidate : Transaction
            Ethereum transaction to process. Can be skipped or passed to the next filter
            in the chain.

        Returns
        -------
        Transaction | None
            Candidate passed the filter.
        """

        raise NotImplementedError()
