from abc import ABC, abstractmethod

from cryptics_learning.interfaces.base_utxo import UTXOInterface
from cryptics_learning.interfaces.transaction_interfaces import TransactionInterface


class WalletInterface(ABC):
    """Abstract base class for a Bitcoin-style UTXO-managing wallet."""

    @property
    @abstractmethod
    def adress(self) -> str:
        """Return the public address of the wallet.

        Returns
        -------
            str: Public address (hex string or encoded).
        """

    @property
    @abstractmethod
    def balance(self) -> float:
        """Return the current balance of the wallet based on known UTXOs.

        Returns
        -------
            float: Total balance.
        """

    @abstractmethod
    def sign_message(self, message: bytes) -> str:
        """Sign a message using the wallet's private key.

        Args:
        ----
            message (bytes): The message to be signed.

        Returns:
        -------
            str: Hex-encoded signature.
        """

    @abstractmethod
    def get_utxos(self) -> list[UTXOInterface]:
        """Return a list of UTXOs currently owned by the wallet.

        Returns
        -------
            list[UTXOInterface]: Spendable outputs.
        """

    @abstractmethod
    def add_utxo(self, utxo: UTXOInterface) -> None:
        """Add a UTXO to the wallet's list of spendable outputs.

        Args:
        ----
            utxo (UTXOInterface): The UTXO to add.
        """

    @abstractmethod
    def remove_utxo(self, utxo: UTXOInterface) -> None:
        """Remove a UTXO after it's been spent.

        Args:
        ----
            utxo (UTXOInterface): The UTXO to remove.
        """

    @abstractmethod
    def create_transaction(self, recipient: str, amount: float) -> TransactionInterface:
        """Create a signed transaction using internal UTXOs.

        Args:
        ----
            recipient (str): The recipient's public key or address.
            amount (float): The amount to send.

        Returns:
        -------
            TransactionInterface: A fully signed transaction.
        """
