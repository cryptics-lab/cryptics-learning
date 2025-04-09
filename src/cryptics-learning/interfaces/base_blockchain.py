from abc import ABC, abstractmethod
from typing import Any

class BlockchainInterface(ABC):
    """
    Abstract base class for a simple blockchain.
    
    Inspired by Bitcoin's whitepaper:
    - Section 3: Timestamp Server
    - Section 4: Proof-of-Work
    - Section 6: Incentive
    - Section 11: Combining and Splitting Value
    """

    @abstractmethod
    def create_genesis_block(self) -> Any:
        """
        Returns:
            Any: The genesis (first) block in the chain.
        
        Note:
            The genesis block is hardcoded and marks the beginning of the blockchain.
            Discussed in Section 3: Timestamp Server, where the first block is the root of the chain.
        """
        pass

    @abstractmethod
    def add_block(self, data: str) -> None:
        """
        Args:
            data (str): The payload for the new block (e.g., transactions).
        
        Note:
            This triggers mining (PoW) and appends the block to the chain.
            Discussed in Section 4: Proof-of-Work, where miners compete to add a block with valid proof.
        """
        pass

    @abstractmethod
    def get_last_block(self) -> Any:
        """
        Returns:
            Any: The last block in the chain (i.e., the tip).
        
        Note:
            This is used to build new blocks based on the previous hash.
            Section 3: Timestamp Server explains how each block references the previous one.
        """
        pass

    @abstractmethod
    def is_valid(self) -> bool:
        """
        Returns:
            bool: True if the entire chain is valid (hashes + linkage).
        
        Note:
            Ensures each block’s hash is valid and each block links correctly
            to its predecessor. Inspired by Sections 3 and 4 of the whitepaper, where each block's 
            hash is checked for validity and proper linkage.
        """
        pass

    @abstractmethod
    def get_chain_length(self) -> int:
        """
        Returns:
            int: The number of blocks in the chain.
        
        Note:
            Used in consensus to determine the longest valid chain.
            Section 11: Combining and Splitting Value mentions how the longest valid chain 
            is chosen as the valid one during network forks.
        """
        pass
