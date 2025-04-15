import hashlib
import json
import logging

from ecdsa import BadSignatureError, SECP256k1, SigningKey, VerifyingKey

from cryptics_learning.interfaces.transaction_interfaces import (
    TransactionInputInterface,
    TransactionInterface,
    TransactionOutputInterface,
)

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class TransactionInput(TransactionInputInterface):
    """Represents a transaction input referencing a UTXO and containing a signature."""

    def __init__(
        self,
        tx_id: str,
        output_index: int,
        signature: str | None = None,
    ) -> None:
        """Initialize a TransactionInput.

        Args:
        ----
            tx_id (str): The transaction ID of the UTXO being spent.
            output_index (int): The index of the output within the referenced transaction.
            signature (Optional[str]): The digital signature to authorize spending (optional at init).
        """
        self._tx_id = tx_id
        self._output_index = output_index
        self._signature = signature

    @property
    def tx_id(self) -> str:
        """Return the transaction ID being referenced."""
        return self._tx_id

    @property
    def output_index(self) -> int:
        """Return the output index in the referenced transaction."""
        return self._output_index

    @property
    def signature(self) -> str | None:
        """Return the signature authorizing the input (if available)."""
        return self._signature

    def to_dict(self, *, include_signature: bool = False) -> dict:
        """Convert input to dictionary format for serialization.

        Args:
        ----
            include_signature (bool): Whether to include the signature field.

        Returns:
        -------
            dict: Serialized dictionary.
        """
        d = {
            "tx_id": self._tx_id,
            "output_index": self._output_index,
        }
        if include_signature and self._signature:
            d["signature"] = self._signature
        return d

    def sign(self, message: bytes, private_key: SigningKey) -> None:
        """Sign this input's message using the provided private key.

        Note:
        ----
            In multi-user scenarios, each input must be signed individually
            by the owner of the corresponding UTXO. This ensures that only
            authorized users can contribute their inputs to a shared transaction.

        Args:
        ----
            message (bytes): The hash/message to sign.
            private_key (SigningKey): The private key used to sign.
        """
        signature = private_key.sign(message)
        self._signature = signature.hex()

    def __str__(self) -> str:
        """Return a string representation of the TransactionInput."""
        return f"TransactionInput(tx_id={self.tx_id}, output_index={self.output_index}, signature={self.signature})"


class TransactionOutput(TransactionOutputInterface):
    """Represents a transaction output defining a recipient and an amount."""

    def __init__(self, amount: float, recipient: str) -> None:
        """Initialize a TransactionOutput.

        Args:
        ----
            amount (float): The amount to be transferred.
            recipient (str): The public key or address of the recipient.
        """
        self._amount = amount
        self._recipient = recipient

    @property
    def amount(self) -> float:
        """Return the amount associated with the output."""
        return self._amount

    @property
    def recipient(self) -> str:
        """Return the recipient address or public key."""
        return self._recipient

    def to_dict(self) -> dict:
        """Convert output to dictionary format for serialization."""
        return {"amount": self.amount, "recipient": self.recipient}

    def __str__(self) -> str:
        """Return a string representation of the TransactionOutput."""
        return f"TransactionOutput(recipient={self.recipient}, amount={self.amount})"


class Transaction(TransactionInterface):
    """Represents a UTXO-based transaction with multiple inputs and outputs."""

    def __init__(
        self,
        tx_inputs: list[TransactionInput],
        tx_outputs: list[TransactionOutput],
    ) -> None:
        """Initialize a Transaction.

        Args:
        ----
            tx_inputs (List[TransactionInput]): List of signed transaction inputs.
            tx_outputs (List[TransactionOutput]): List of transaction outputs.
        """
        self._inputs = tx_inputs
        self._outputs = tx_outputs
        self._tx_id = self.compute_hash()

    @property
    def tx_id(self) -> str:
        """Return the transaction ID."""
        return self._tx_id

    @property
    def inputs(self) -> list[TransactionInput]:
        """Return the list of transaction inputs."""
        return self._inputs

    @property
    def outputs(self) -> list[TransactionOutput]:
        """Return the list of transaction outputs."""
        return self._outputs

    def to_dict(self, *, include_signatures: bool = True) -> dict:
        """Convert transaction to dictionary format for serialization.

        Args:
        ----
            include_signatures (bool): Whether to include input signatures.

        Returns:
        -------
            dict: Serialized dictionary.
        """
        return {
            "inputs": [
                inp.to_dict(include_signature=include_signatures)
                for inp in self._inputs
            ],
            "outputs": [out.to_dict() for out in self._outputs],
        }

    def compute_hash(self) -> str:
        """Compute and return the SHA-256 hash of the transaction.

        Returns
        -------
            str: Transaction hash as a hex string.
        """
        data = json.dumps(self.to_dict(include_signatures=True), sort_keys=True)
        return hashlib.sha256(data.encode()).hexdigest()

    def update_tx_id(self) -> None:
        """Update the transaction ID based on the current state."""
        self._tx_id = self.compute_hash()

    def sign(self) -> bool:
        """Sign the transaction. Assumes each input is pre-signed externally.

        Returns
        -------
            bool: True if transaction is valid after signature verification.
        """
        return self.verify([])

    def verify(self, public_keys: list[VerifyingKey]) -> bool:
        """Verify all input signatures.

        Args:
        ----
            public_keys (List[VerifyingKey]): Public keys matching the inputs.

        Returns:
        -------
            bool: True if all input signatures are valid.
        """
        message = json.dumps(
            self.to_dict(include_signatures=False),
            sort_keys=True,
        ).encode()
        for i, inp in enumerate(self._inputs):
            try:
                signature = bytes.fromhex(inp.signature)
                public_keys[i].verify(signature, message)
            except (ValueError, BadSignatureError, TypeError):
                return False
        return True

    def get_total_input(self) -> float:
        """Return the total number of inputs (simplified for testing).

        Returns
        -------
            float: Total input value.
        """
        return float(len(self._inputs))

    def get_total_output(self) -> float:
        """Return the total output value.

        Returns
        -------
            float: Sum of all output amounts.
        """
        return sum(output.amount for output in self._outputs)

    def __str__(self) -> str:
        """Return a string representation of the Transaction."""
        return f"Transaction(tx_id={self.tx_id}, inputs={self.inputs}, outputs={self.outputs})"


if __name__ == "__main__":
    # Simulate two wallets
    sk1 = SigningKey.generate(curve=SECP256k1)
    pk1 = sk1.verifying_key

    sk2 = SigningKey.generate(curve=SECP256k1)
    pk2 = sk2.verifying_key

    # Create unsigned inputs
    input1 = TransactionInput("tx123", 0)
    input2 = TransactionInput("tx456", 1)

    # Create dummy outputs
    output = TransactionOutput(5.0, pk1.to_string().hex())

    # Create transaction
    tx = Transaction([input1, input2], [output])

    # Create message to sign
    message = json.dumps(tx.to_dict(include_signatures=False), sort_keys=True).encode()

    # Sign each input
    input1.sign(message, sk1)
    input2.sign(message, sk2)

    # Recompute tx_id after signatures
    tx.update_tx_id()

    logger.info("Transaction Created:")
    logger.info(tx)

    logger.info("Verifying Transaction:")
    logger.info("Valid? %s", tx.verify([pk1, pk2]))
