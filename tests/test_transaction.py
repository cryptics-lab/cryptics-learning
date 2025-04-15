import json

from cryptics_learning.transaction import (
    Transaction,
    TransactionInput,
    TransactionOutput,
)
from ecdsa import SECP256k1, SigningKey, VerifyingKey

# Constants to avoid magic values
EXPECTED_TOTAL_INPUT = 1.0
EXPECTED_TOTAL_OUTPUT = 5.0
CORRUPT_BYTE = "00"


def test_transaction_sign_and_verify() -> None:
    """Test that a valid multi-signed transaction verifies successfully."""
    sk1: SigningKey = SigningKey.generate(curve=SECP256k1)
    pk1: VerifyingKey = sk1.verifying_key

    sk2: SigningKey = SigningKey.generate(curve=SECP256k1)
    pk2: VerifyingKey = sk2.verifying_key

    input1: TransactionInput = TransactionInput("tx123", 0)
    input2: TransactionInput = TransactionInput("tx456", 1)
    output: TransactionOutput = TransactionOutput(
        EXPECTED_TOTAL_OUTPUT,
        pk1.to_string().hex(),
    )

    tx: Transaction = Transaction([input1, input2], [output])
    message: bytes = json.dumps(
        tx.to_dict(include_signatures=False),
        sort_keys=True,
    ).encode()

    input1.sign(message, sk1)
    input2.sign(message, sk2)

    tx._tx_id = tx.compute_hash()  # noqa: SLF001

    assert tx.verify([pk1, pk2]) is True


def test_invalid_signature() -> None:
    """Test that transaction verification fails with a corrupted signature."""
    sk1: SigningKey = SigningKey.generate(curve=SECP256k1)
    pk1: VerifyingKey = sk1.verifying_key

    sk2: SigningKey = SigningKey.generate(curve=SECP256k1)
    pk2: VerifyingKey = sk2.verifying_key

    input1: TransactionInput = TransactionInput("tx123", 0)
    input2: TransactionInput = TransactionInput("tx456", 1)
    output: TransactionOutput = TransactionOutput(
        EXPECTED_TOTAL_OUTPUT,
        pk1.to_string().hex(),
    )
    tx: Transaction = Transaction([input1, input2], [output])

    message: bytes = json.dumps(
        tx.to_dict(include_signatures=False),
        sort_keys=True,
    ).encode()
    input1.sign(message, sk1)
    input2.sign(message, sk2)

    input1._signature = CORRUPT_BYTE * len(input1.signature)  # noqa: SLF001

    assert tx.verify([pk1, pk2]) is False


def test_total_input_and_output() -> None:
    """Test total input and output value computation."""
    sk1: SigningKey = SigningKey.generate(curve=SECP256k1)
    pk1: VerifyingKey = sk1.verifying_key

    input1: TransactionInput = TransactionInput("tx123", 0)
    output1: TransactionOutput = TransactionOutput(3.0, pk1.to_string().hex())
    output2: TransactionOutput = TransactionOutput(2.0, pk1.to_string().hex())

    tx: Transaction = Transaction([input1], [output1, output2])

    assert tx.get_total_input() == EXPECTED_TOTAL_INPUT
    assert tx.get_total_output() == EXPECTED_TOTAL_OUTPUT
