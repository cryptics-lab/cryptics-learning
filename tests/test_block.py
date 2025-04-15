"""Unit tests for the Block class."""

import pytest
from cryptics_learning.block import Block

HASH_LENGTH = 64


@pytest.fixture()
def block() -> Block:
    """Return a test Block instance."""
    return Block(
        1,
        "Test Data",
        "0" * HASH_LENGTH,
    )


def test_block_initialization(block: Block) -> None:
    """Test Block initializes correctly."""
    assert block.index == 1
    assert block.data == "Test Data"
    assert block.previous_hash == "0" * HASH_LENGTH
    assert isinstance(block.timestamp, float)
    assert block.nonce == 0
    assert block.block_hash is not None


def test_compute_hash(block: Block) -> None:
    """Test compute_hash returns a valid SHA-256 hash."""
    expected_hash = block.compute_hash()
    assert isinstance(expected_hash, str)
    assert len(expected_hash) == HASH_LENGTH


def test_mine(block: Block) -> None:
    """Test mining works with display off."""
    block.mine(difficulty=2, display=False)
    assert block.block_hash.startswith("00")
    assert len(block.block_hash) == HASH_LENGTH
