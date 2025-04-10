"""Implement Block."""
import hashlib
from datetime import datetime, timezone

from helpers.log_config import setup_logger
from interfaces.base_block import BlockInterface

logger = setup_logger()


class Block(BlockInterface):
    """Implements BlockInterface."""

    def __init__(self, index: int, data: str, previous_hash: str) -> "Block":
        """Initialize the class instance.

        Args:
        ----
            index (int): The block's position in the chain.
            data (str): The data (transactions) associated with the block.
            previous_hash (str): The hash of the previous block.
        """
        self._index = index
        self._data = data
        self._previous_hash = previous_hash
        self._timestamp = datetime.now(timezone.utc).timestamp()
        self._nonce = 0
        self._hash = self.compute_hash()

    @property
    def index(self) -> int:
        """Return the block's position in the chain.

        Note:
        ----
            The index of the block represents its position in the blockchain and ensures
            proper linking to previous blocks. This is important for the chain structure,
            as mentioned in Section 3: Timestamp Server.
        """
        return self._index

    @property
    def data(self) -> str:
        """Return the block's data (transactions).

        Note:
        ----
            This will be transactions.
        """
        return self._data

    @property
    def previous_hash(self) -> str:
        """Return the hash of the previous block.

        Note:
        ----
            Each block includes the hash of the previous block to ensure the integrity and
            immutability of the chain. This is a key aspect of how blocks are linked
            together, as described in Section 3: Timestamp Server.
        """
        return self._previous_hash

    @property
    def block_hash(self) -> str:
        """Return the current block's hash.

        Note:
        ----
            The block's hash is computed from its content (transactions, timestamp, etc.).
            Section 4: Proof-of-Work discusses how this hash is generated and validated
            to demonstrate proof-of-work.
        """
        return self._hash

    @property
    def timestamp(self) -> float:
        """Return the block's creation timestamp.

        Note:
        ----
            The timestamp is critical for the chronological ordering of blocks and
            for calculating the block's hash. This is discussed in Section 3: Timestamp Server.
        """
        return self._timestamp

    def compute_hash(self) -> str:
        """Compute and return the SHA-256 hash of this block's contents.

        Returns:
        -------
            str: The computed SHA-256 hash of this block's contents.

        Note:
        ----
            This method calculates the hash of the block, which includes the Merkle root
            and other block information. Section 4: Proof-of-Work mentions that the hash
            must meet certain difficulty criteria, which is enforced during the mining process.
        """
        # Concatenate the relevant block properties into a string
        block_string = (
            f"{self.index}"
            f"{self.previous_hash}"
            f"{self.timestamp}"
            f"{self.data}"
            f"{self._nonce}"
        )

        # Create the SHA-256 hash of the string
        return hashlib.sha256(block_string.encode("utf-8")).hexdigest()

    def mine(self, difficulty: int, *, display: bool = True) -> None:
        """Perform the proof-of-work mining process to find a valid hash.

        Args:
        ----
            difficulty (int): Number of leading zeros required in the hash.

        Note:
        ----
            This implements proof-of-work by incrementing the nonce until the hash
            meets the specified difficulty.
        """
        leading_zeros = "0" * difficulty
        block_hash = self.compute_hash()

        while block_hash[:difficulty] != leading_zeros:
            self._nonce += 1
            block_hash = self.compute_hash()
            if display:
                logger.info(
                    "Leading Zero's: %s; Nonce: %d; Hash: %s;",
                    leading_zeros,
                    self._nonce,
                    block_hash,
                )

        self._hash = block_hash


if __name__ == "__main__":
    # Example usage:
    block = Block(1, "Nakamoto", "0")
    block.mine(difficulty=3)
