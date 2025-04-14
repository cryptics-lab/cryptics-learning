import unittest

from cryptics_learning.blockchain import BlockChain

CHAIN_LENGTH_AFTER_GENESIS = (
    2  # Constant for the expected length of the chain after the genesis block
)


class TestBlockChain(unittest.TestCase):
    """Test suite for the BlockChain class.

    This class contains tests for methods in the BlockChain class, including
    adding blocks, validating the chain, and checking the integrity of the blockchain.
    """

    def setUp(self) -> None:
        """Set up a new blockchain instance for each test."""
        self.blockchain = BlockChain()

    def test_create_genesis_block(self) -> None:
        """Test if the genesis block is created correctly."""
        genesis_block = self.blockchain.create_genesis_block()
        assert genesis_block.index == 0
        assert not genesis_block.previous_hash
        assert genesis_block.data == "Nvm"

    def test_add_block(self) -> None:
        """Test if a new block is added to the blockchain."""
        self.blockchain.add_block("Block 1 data")
        assert self.blockchain.get_chain_length() == CHAIN_LENGTH_AFTER_GENESIS
        last_block = self.blockchain.get_last_block()
        assert last_block.data == "Block 1 data"
        assert (
            last_block.previous_hash
            == self.blockchain._chain[-2].block_hash  # noqa: SLF001
        )

    def test_get_last_block(self) -> None:
        """Test if the method returns the last block in the blockchain."""
        self.blockchain.add_block("Block 1 data")
        last_block = self.blockchain.get_last_block()
        assert last_block.data == "Block 1 data"

    def test_is_valid(self) -> None:
        """Test if the blockchain is valid after adding blocks."""
        assert self.blockchain.is_valid()
        self.blockchain.add_block("Block 1 data")
        assert self.blockchain.is_valid()

    def test_is_invalid_chain(self) -> None:
        """Test if the blockchain is invalid when blocks are tampered with."""
        self.blockchain.add_block("Block 1 data")
        self.blockchain.add_block("Block 2 data")
        self.blockchain._chain[1]._data = "Tampered data"  # noqa: SLF001
        assert not self.blockchain.is_valid()

    def test_get_chain_length(self) -> None:
        """Test if the chain length is correct."""
        assert self.blockchain.get_chain_length() == 1
        self.blockchain.add_block("Block 1 data")
        assert self.blockchain.get_chain_length() == CHAIN_LENGTH_AFTER_GENESIS


if __name__ == "__main__":
    unittest.main()
