import pytest
from cryptics_learning.transaction import (
    Transaction,
)
from cryptics_learning.utxo import UTXO
from cryptics_learning.wallet import Wallet

INITIAL_WALLET_VALUE: float = 50.0
RECIPIENT_ADDRESS: str = "recipient_dummy_address"
TRANSFER_AMOUNT: float = 30.0
EXPECTED_NUM_OUTPUTS = 2


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
    """Test add_utxo and balance update."""
    first_wallet.add_utxo(first_utxo)
    assert first_wallet.balance == INITIAL_WALLET_VALUE


def test_create_transaction_valid(first_wallet: Wallet, first_utxo: UTXO) -> None:
    """Test that a wallet can create a valid signed transaction."""
    first_wallet.add_utxo(first_utxo)
    tx: Transaction = first_wallet.create_transaction(
        RECIPIENT_ADDRESS,
        TRANSFER_AMOUNT,
    )

    # Basic checks
    assert isinstance(tx, Transaction)
    assert tx.verify() is True

    # Inputs reference correct UTXO
    input_ref = tx.inputs[0]
    assert input_ref.tx_id == first_utxo.tx_id
    assert input_ref.output_index == first_utxo.output_index

    # Outputs add up correctly
    output_total = sum(output.amount for output in tx.outputs)
    assert pytest.approx(output_total, 0.01) == INITIAL_WALLET_VALUE

    # UTXO should be removed
    first_wallet.remove_utxo(first_utxo)
    assert first_wallet.balance == 0


def test_create_transaction_insufficient_funds(first_wallet: Wallet) -> None:
    """Test that trying to send more than the wallet has raises an error."""
    with pytest.raises(ValueError, match="Not enough funds in wallet."):
        first_wallet.create_transaction(RECIPIENT_ADDRESS, amount=100.0)


def test_transaction_change_output(first_wallet: Wallet, first_utxo: UTXO) -> None:
    """Test that a change output is created when needed."""
    first_wallet.add_utxo(first_utxo)
    tx = first_wallet.create_transaction(RECIPIENT_ADDRESS, amount=TRANSFER_AMOUNT)

    # One output should go to the recipient, one back to the sender
    assert len(tx.outputs) == EXPECTED_NUM_OUTPUTS

    # Check presence of change output
    change_outputs = [
        out for out in tx.outputs if out.recipient == first_wallet.address
    ]
    assert len(change_outputs) == 1
    assert (
        pytest.approx(change_outputs[0].amount, 0.01)
        == INITIAL_WALLET_VALUE - TRANSFER_AMOUNT
    )
