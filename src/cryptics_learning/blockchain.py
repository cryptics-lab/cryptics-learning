from cryptics_learning.block import Block
from cryptics_learning.helpers.log_config import setup_logger
from cryptics_learning.interfaces.base_blockchain import BlockchainInterface

logger = setup_logger()


class BlockChain(BlockchainInterface):
    """Represents a simple blockchain with methods to add blocks, validate the chain, and log details.

    This class implements the basic functionality of a blockchain, including creating the genesis block,
    adding new blocks, validating the chain, and logging the blockchain's details. It models the behavior
    described in Sections 3 and 4 of the whitepaper, including timestamping, proof-of-work, and chain validation.

    Attributes
    ----------
        _chain (list[Block]): A list holding the blocks in the blockchain, starting with the genesis block.

    Methods
    -------
        create_genesis_block(): Creates and returns the genesis (first) block in the chain.
        add_block(data: str): Adds a new block with the given data to the blockchain.
        get_last_block(): Returns the last block in the blockchain.
        is_valid(): Checks whether the blockchain is valid, ensuring all hashes and links are correct.
        get_chain_length(): Returns the number of blocks in the blockchain.
        log_chain(): Logs details of the blockchain, including block data and validity.
    """

    def __init__(self) -> None:
        """Initialize class."""
        self._chain: list[Block] = []
        self._chain.append(self.create_genesis_block())
        self.DIFFICULTY = 3

    def create_genesis_block(self) -> Block:
        """Return the genesis (first) block in the chain.

        The genesis block is hardcoded and marks the beginning of the blockchain.
        Discussed in Section 3: Timestamp Server, where the first block is the root of the chain.
        """
        data = "Nvm"
        previous_hash: str = ""
        index: int = 0
        return Block(index, data, previous_hash)

    def add_block(self, data: str) -> None:
        """Add a new block to the chain.

        Args:
        ----
            data (Any): The payload for the new block (e.g., transactions).

        This triggers mining (PoW) and appends the block to the chain.
        Discussed in Section 4: Proof-of-Work, where miners compete to add a block with valid proof.

        Note: in this case there is only one miner and one user.
        """
        index: int = len(self._chain)
        previous_hash: str = self._chain[-1].block_hash
        new_block: Block = Block(index, data, previous_hash)
        new_block.mine(self.DIFFICULTY)
        self._chain.append(new_block)

    def get_last_block(self) -> Block:
        """Return the last block in the chain (i.e., the tip).

        This is used to build new blocks based on the previous hash.
        Section 3: Timestamp Server explains how each block references the previous one.
        """
        return self._chain[-1]

    def is_valid(self) -> bool:
        """Return whether the entire chain is valid (hashes + linkage + proof-of-work).

        Ensures each block's:
        - hash matches its computed contents,
        - previous_hash matches the previous block's hash,
        - hash satisfies the proof-of-work difficulty requirement.

        Inspired by Sections 3 and 4 of the Bitcoin whitepaper.
        """
        difficulty_prefix = "0" * self.DIFFICULTY
        previous_hash = self._chain[0].block_hash

        for i in range(1, len(self._chain)):
            block = self._chain[i]

            # Check if previous hash matches
            if block.previous_hash != previous_hash:
                return False

            # Check if hash matches block content
            if block.block_hash != block.compute_hash():
                return False

            # Check if hash satisfies proof-of-work
            if not block.block_hash.startswith(difficulty_prefix):
                return False

            previous_hash = block.block_hash

        return True

    def get_chain_length(self) -> int:
        """Return the number of blocks in the chain.

        Used in consensus to determine the longest valid chain.
        Section 11: Combining and Splitting Value mentions how the longest valid chain
        is chosen as the valid one during network forks.
        """
        return len(self._chain)

    def log_chain(self) -> None:
        """Log details about the blockchain, including its length, the details of each block, and its validity.

        This method prints out the following information:
        - The current length of the blockchain.
        - The index, data, previous hash, and block hash for each block in the blockchain.
        - Whether the blockchain is valid or invalid.

        Args:
        ----
            None

        Returns:
        -------
            None
        """
        # Print out the blockchain length
        logger.info("Blockchain Length: %d", self.get_chain_length())

        # Print details of each block
        for i, block in enumerate(self._chain):
            logger.info("Block %d:", i)
            logger.info("  Index: %d", block.index)
            logger.info("  Data: %s", str(block.data))
            logger.info("  Previous Hash: %s", block.previous_hash)


if __name__ == "__main__":
    # Initialize the blockchain
    blockchain = BlockChain()

    # Add some blocks with example data
    blockchain.add_block("Block 1 data")
    blockchain.add_block("Block 2 data")
    blockchain.add_block("Block 3 data")

    blockchain.log_chain()
