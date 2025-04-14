from abc import ABC, abstractmethod

from cryptics_learning.interfaces.base_block import (
    BlockInterface,  # Assuming Block is imported from the correct module
)


class BlockchainInterface(ABC):
    """Abstract base class for a simple blockchain.

    Inspired by Bitcoin's whitepaper:
    - Section 3: Timestamp Server
    - Section 4: Proof-of-Work
    - Section 6: Incentive
    - Section 11: Combining and Splitting Value
    """

    @abstractmethod
    def create_genesis_block(self) -> BlockInterface:
        """Return the genesis (first) block in the chain.

        The genesis block is hardcoded and marks the beginning of the blockchain.
        Discussed in Section 3: Timestamp Server, where the first block is the root of the chain.
        """

    @abstractmethod
    def add_block(self, data: str) -> None:
        """Add a new block to the chain.

        Args:
        ----
            data (str): The payload for the new block (e.g., transactions).

        This triggers mining (PoW) and appends the block to the chain.
        Discussed in Section 4: Proof-of-Work, where miners compete to add a block with valid proof.
        """

    @abstractmethod
    def get_last_block(self) -> BlockInterface:
        """Return the last block in the chain (i.e., the tip).

        This is used to build new blocks based on the previous hash.
        Section 3: Timestamp Server explains how each block references the previous one.
        """

    @abstractmethod
    def is_valid(self) -> bool:
        """Return whether the entire chain is valid (hashes + linkage).

        Ensures each block's hash is valid and each block links correctly
        to its predecessor. Inspired by Sections 3 and 4 of the whitepaper, where each block's
        hash is checked for validity and proper linkage.
        """

    @abstractmethod
    def get_chain_length(self) -> int:
        """Return the number of blocks in the chain.

        Used in consensus to determine the longest valid chain.
        Section 11: Combining and Splitting Value mentions how the longest valid chain
        is chosen as the valid one during network forks.
        """
