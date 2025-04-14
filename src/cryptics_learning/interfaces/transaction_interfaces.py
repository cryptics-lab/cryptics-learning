# src/cryptics_learning/interfaces/base_transaction_input.py

from abc import ABC, abstractmethod


class TransactionInputInterface(ABC):
    """Abstract base class for a transaction input referencing a UTXO."""

    @property
    @abstractmethod
    def tx_id(self) -> str:
        """Return the transaction ID of the UTXO being referenced.

        Returns
        -------
            str: The transaction hash.
        """

    @property
    @abstractmethod
    def output_index(self) -> int:
        """Return the index of the output in the referenced transaction.

        Returns
        -------
            int: Index of the output.
        """

    @property
    @abstractmethod
    def signature(self) -> str:
        """Return the digital signature authorizing the spend.

        Returns
        -------
            str: Signature created with the owner's private key.
        """

    @abstractmethod
    def __str__(self) -> str:
        """Return a human-readable string representation of the object.

        Returns
        -------
            str: object in string format.
        """


class TransactionOutputInterface(ABC):
    """Abstract base class for a transaction output."""

    @property
    @abstractmethod
    def amount(self) -> float:
        """Return the amount to be transferred in this output.

        Returns
        -------
            float: Amount in the output.
        """

    @property
    @abstractmethod
    def recipient(self) -> str:
        """Return the public key/address that can spend this output.

        Returns
        -------
            str: Recipient's public key or address.
        """

    @abstractmethod
    def __str__(self) -> str:
        """Return a human-readable string representation of the object.

        Returns
        -------
            str: object in string format.
        """


class TransactionInterface(ABC):
    """Abstract base class for a UTXO-based transaction.

    Note: wallets are not part of Transaction because Bitcoin is designed
    to work without needing to know who "owns" what.
    """

    @property
    @abstractmethod
    def tx_id(self) -> str:
        """Return the transaction ID (hash of its contents).

        Returns
        -------
            str: Unique transaction hash.
        """

    @property
    @abstractmethod
    def inputs(self) -> list[TransactionInputInterface]:
        """Return the list of inputs for this transaction.

        Returns
        -------
            List[TransactionInputInterface]: Transaction inputs.
        """

    @property
    @abstractmethod
    def outputs(self) -> list[TransactionOutputInterface]:
        """Return the list of outputs for this transaction.

        Returns
        -------
            List[TransactionOutputInterface]: Transaction outputs.
        """

    @abstractmethod
    def compute_hash(self) -> str:
        """Compute the transaction ID from its contents.

        Returns
        -------
            str: The computed transaction hash.
        """

    @abstractmethod
    def sign(self, private_key: str) -> None:
        """Sign the transaction inputs using a private key.

        Args:
        ----
            private_key (str): The private key used to sign the inputs.
        """

    @abstractmethod
    def verify(self) -> bool:
        """Verify all input signatures and transaction validity.

        Returns
        -------
            bool: True if the transaction is valid, False otherwise.
        """

    @abstractmethod
    def get_total_input(self) -> float:
        """Return the total input value.

        Returns
        -------
            float: Total input value.
        """

    @abstractmethod
    def get_total_output(self) -> float:
        """Return the total output value.

        Returns
        -------
            float: Total output value.
        """

    @abstractmethod
    def __str__(self) -> str:
        """Return a human-readable string representation of the object.

        Returns
        -------
            str: object in string format.
        """
