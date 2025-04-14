from collections.abc import Generator

import pytest
from cryptics_learning.utxo import UTXO


@pytest.fixture()
def sample_utxo() -> Generator[UTXO, None, None]:
    """Fixture providing a sample UTXO instance for testing."""
    return UTXO(
        tx_id="abc123",
        output_index=0,
        recipient="recipient_pubkey",
        amount=50.0,
    )


TX_ID = "abc123"
OUTPUT_INDEX = 0
RECIPIENT = "recipient_pubkey"
WRONG_RECIPIENT = "wrong_pubkey"
AMOUNT = 50.0


def test_utxo_fields(sample_utxo: UTXO) -> None:
    """Test that UTXO fields are set correctly."""
    assert sample_utxo.tx_id == TX_ID
    assert sample_utxo.output_index == OUTPUT_INDEX
    assert sample_utxo.recipient == RECIPIENT
    assert sample_utxo.amount == AMOUNT


def test_is_owned_by(sample_utxo: UTXO) -> None:
    """Test ownership verification via is_owned_by."""
    assert sample_utxo.is_owned_by(RECIPIENT) is True
    assert sample_utxo.is_owned_by(WRONG_RECIPIENT) is False


def test_to_dict(sample_utxo: UTXO) -> None:
    """Test dictionary serialization of a UTXO."""
    expected = {
        "tx_id": TX_ID,
        "output_index": OUTPUT_INDEX,
        "recipient": RECIPIENT,
        "amount": AMOUNT,
    }
    assert sample_utxo.to_dict() == expected


def test_str_representation(sample_utxo: UTXO) -> None:
    """Test human-readable string representation of UTXO."""
    string_output = str(sample_utxo)
    assert "UTXO(" in string_output
    assert f"tx_id={TX_ID}" in string_output
    assert f"output_index={OUTPUT_INDEX}" in string_output
    assert f"recipient={RECIPIENT}" in string_output
    assert f"amount={AMOUNT}" in string_output
