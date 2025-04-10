from abc import ABC, abstractmethod


class BlockInterface(ABC):
    """Abstract base class for a block in a blockchain.

    Based on the Bitcoin whitepaper:
    - Section 2: Transactions
    - Section 3: Timestamp Server
    - Section 4: Proof-of-Work
    """

    @property
    @abstractmethod
    def index(self) -> int:
        """Return the block's position in the chain."""

    @property
    @abstractmethod
    def previous_hash(self) -> str:
        """Return the hash of the previous block."""

    @property
    @abstractmethod
    def block_hash(self) -> str:
        """Return the current block's hash."""

    @property
    @abstractmethod
    def timestamp(self) -> float:
        """Return the block's creation timestamp."""

    @abstractmethod
    def compute_hash(self) -> str:
        """Compute and return the SHA-256 hash of this block's contents.

        Returns
        -------
            str: The computed SHA-256 hash of this block's contents.
        """

    @abstractmethod
    def mine(self, difficulty: int) -> None:
        """Perform the proof-of-work mining process.

        Args:
        ----
            difficulty (int): Number of leading zeros required in the hash.

        Note:
        ----
            This implements proof-of-work by incrementing the nonce until the hash
            meets the specified difficulty.
        """
