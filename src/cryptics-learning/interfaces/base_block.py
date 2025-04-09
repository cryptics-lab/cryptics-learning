from abc import ABC, abstractmethod
from typing import Any

class BlockInterface(ABC):
    """
    Abstract base class for a block in a blockchain.
    
    Based on Bitcoin whitepaper:
    - Section 2: Transactions
    - Section 3: Timestamp Server
    - Section 4: Proof-of-Work
    """

    @property
    @abstractmethod
    def index(self) -> int:
        """Returns the block's position in the chain.
        
        Note:
            The index of the block represents its position in the blockchain and ensures 
            proper linking to previous blocks. This is important for the chain structure, 
            as mentioned in Section 3: Timestamp Server.
        """
        pass

    @property
    @abstractmethod
    def previous_hash(self) -> str:
        """Returns the hash of the previous block.
        
        Note:
            Each block includes the hash of the previous block to ensure the integrity and 
            immutability of the chain. This is a key aspect of how blocks are linked 
            together, as described in Section 3: Timestamp Server.
        """
        pass

    @property
    @abstractmethod
    def hash(self) -> str:
        """Returns the current block's hash.
        
        Note:
            The block's hash is computed from its content (transactions, timestamp, etc.).
            Section 4: Proof-of-Work discusses how this hash is generated and validated 
            to demonstrate proof-of-work.
        """
        pass

    @property
    @abstractmethod
    def timestamp(self) -> float:
        """Returns the block's creation timestamp.
        
        Note:
            The timestamp is critical for the chronological ordering of blocks and 
            for calculating the block's hash. This is discussed in Section 3: Timestamp Server.
        """
        pass

    @abstractmethod
    def compute_hash(self) -> str:
        """
        Returns:
            str: The computed SHA-256 hash of this block's contents.
        
        Note:
            This method calculates the hash of the block, which includes the Merkle root 
            and other block information. Section 4: Proof-of-Work mentions that the hash 
            must meet certain difficulty criteria, which is enforced during the mining process.
        """
        pass

    @abstractmethod
    def mine(self, difficulty: int) -> None:
        """
        Args:
            difficulty (int): Number of leading zeros required in the hash.
        
        Note:
            This implements proof-of-work. The miner needs to find a valid hash that 
            satisfies the difficulty level by repeatedly hashing different nonce values.
            Section 4: Proof-of-Work describes this mining process.
        """
        pass
