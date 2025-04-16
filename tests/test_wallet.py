import pytest
from cryptics_learning.utxo import UTXO
from cryptics_learning.wallet import Wallet

INITIAL_WALLET_VALUE: float = 50


@pytest.fixture()
def first_wallet() -> Wallet:
    """Create a first Wallet for testing."""
    return Wallet()


@pytest.fixture()
def first_utxo(first_wallet: Wallet) -> UTXO:
    """Create a first UTXO for testing."""
    return UTXO(
        tx_id="tx1",
        output_index=0,
        recipient=first_wallet.address,
        amount=INITIAL_WALLET_VALUE,
    )


def test_add_utxo_updates_balance(first_wallet: Wallet, first_utxo: UTXO) -> None:
    """Test add_utxo and balance."""
    first_wallet.add_utxo(first_utxo)
    assert first_wallet.balance == INITIAL_WALLET_VALUE
