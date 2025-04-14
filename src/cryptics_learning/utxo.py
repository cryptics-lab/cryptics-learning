from cryptics_learning.interfaces.base_utxo import UTXOInterface


class UTXO(UTXOInterface):
    """Abstract base class for a UTXO (Unspent Transaction Output)."""

    def __init__(
        self,
        tx_id: str,
        output_index: int,
        recipient: str,
        amount: float,
    ) -> None:
        """Return instance of UTXO class."""
        self._tx_id: str = tx_id
        self._output_index: str = output_index
        self._recipient: str = recipient
        self._amount: float = amount

    @property
    def tx_id(self) -> str:
        """Return the ID of the transaction that created this output.

        Returns
        -------
            str: Transaction hash.
        """
        return self._tx_id

    @property
    def output_index(self) -> int:
        """Return the index of the output within the transaction.

        Returns:
        -------
            int: Output index.

        Note:
        ----
            Bitcoin Paper, Section 2:
            “We define an electronic coin as a
            chain of digital signatures.
            Each owner transfers the coin to the next by
            digitally signing a hash of the previous transaction
            and the public key of the next owner.”

            So each transaction spends the previous outputs
            by referencing them, it then creates new outputs
            that in turn can be spend.

            UTXO is the way "spendable ouput is formalized
        """
        return self._output_index

    @property
    def recipient(self) -> str:
        """Return the recipient's public key or address.

        Returns
        -------
            str: Address/public key hash that can spend this output.
        """
        return self._recipient

    @property
    def amount(self) -> float:
        """Return the amount stored in this output.

        Returns
        -------
            float: Amount of value in the output.
        """
        return self._amount

    def is_owned_by(self, public_key: str) -> bool:
        """Check if the UTXO is owned by a given public key or address.

        Args:
        ----
            public_key (str): The public key to verify.

        Returns:
        -------
            bool: True if the recipient matches, False otherwise.
        """
        return self._recipient == public_key

    def to_dict(self) -> dict:
        """Serialize the UTXO to a dictionary.

        Returns
        -------
            dict: Dictionary containing tx_id, output_index, recipient, and amount.
        """
        return {
            "tx_id": self.tx_id,
            "output_index": self.output_index,
            "recipient": self.recipient,
            "amount": self.amount,
        }

    def __str__(self) -> str:
        """Return string representation of UTXO class instance."""
        return (
            f"UTXO("
            f"  tx_id={self.tx_id},"
            f"  output_index={self.output_index},"
            f"  recipient={self.recipient},"
            f"  amount={self.amount}"
            f")"
        )


if __name__ == "__main__":
    utxo1 = UTXO(2, 1, 3, 20.0)

    from cryptics_learning.helpers.log_config import setup_logger

    logger = setup_logger()
    logger.info(utxo1)
