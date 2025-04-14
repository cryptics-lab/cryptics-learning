from abc import ABC, abstractmethod


class UTXOInterface(ABC):
    """Abstract base class for a UTXO (Unspent Transaction Output)."""

    @property
    @abstractmethod
    def tx_id(self) -> str:
        """Return the ID of the transaction that created this output.

        Returns
        -------
            str: Transaction hash.
        """

    @property
    @abstractmethod
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

    @property
    @abstractmethod
    def recipient(self) -> str:
        """Return the recipient's public key or address.

        Returns
        -------
            str: Address/public key hash that can spend this output.
        """

    @property
    @abstractmethod
    def amount(self) -> float:
        """Return the amount stored in this output.

        Returns
        -------
            float: Amount of value in the output.
        """

    @abstractmethod
    def is_owned_by(self, public_key: str) -> bool:
        """Check if the UTXO is owned by a given public key or address.

        Args:
        ----
            public_key (str): The public key to verify.

        Returns:
        -------
            bool: True if the recipient matches, False otherwise.
        """

    @abstractmethod
    def to_dict(self) -> dict:
        """Serialize the UTXO to a dictionary.

        Returns
        -------
            dict: Dictionary containing tx_id, output_index, recipient, and amount.
        """

    @abstractmethod
    def __str__(self) -> str:
        """Return a human-readable string representation of the object.

        Returns
        -------
            str: object in string format.
        """
