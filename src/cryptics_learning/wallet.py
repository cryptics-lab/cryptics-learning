import hashlib
from logging import Logger

import base58
from ecdsa import SECP256k1, SigningKey, VerifyingKey

from cryptics_learning.helpers.log_config import setup_logger
from cryptics_learning.interfaces.base_wallet import WalletInterface
from cryptics_learning.transaction import (
    Transaction,
)
from cryptics_learning.utxo import UTXO

logger: Logger = setup_logger()


class Wallet(WalletInterface):
    """Concrete implementation of a Bitcoin-style wallet.

    This wallet represents a user's identity on the blockchain and manages:
    - Generation of private/public keypairs using ECDSA and secp256k1 curve.
    - Derivation of a Bitcoin-style address by hashing the public key.
    - Storage and selection of UTXOs (unspent transaction outputs).
    - Creation of signed transactions to spend UTXOs.

    Key ideas:
    - Section 10 of the Bitcoin whitepaper outlines how digital signatures are used to prove ownership.
    - Section 6 describes how addresses are based on public keys and how transactions are signed.
    - UTXOs are the spendable outputs referenced in Section 5: "Combining and Splitting Value."

    Uses the `ecdsa` Python package for signing keys.
    Uses `hashlib` for SHA-256 and RIPEMD-160 hashing to generate addresses.
    """

    def __init__(self) -> None:
        """Create a new wallet.

        This initializes a new ECDSA private key using the secp256k1 curve (same as Bitcoin).
        The corresponding public key is derived, then hashed (SHA-256 + RIPEMD-160) to create
        the wallet address. This is the identity that receives UTXOs.

        The wallet also starts with an empty list of known UTXOs.
        """
        self._private_key: SigningKey = SigningKey.generate(curve=SECP256k1)
        self._public_key: str = self._private_key.verifying_key

        self._address = self._get_address(self._public_key)
        self._utxos: dict[(str, int), UTXO] = {}

    def _get_address(self, public_key: VerifyingKey) -> str:
        """Return a Bitcoin-style Base58Check encoded address from a public key.

        Steps:
        1. SHA-256 hash of public key
        2. RIPEMD-160 hash of that SHA-256
        3. Prepend version byte (0x00 for mainnet)
        4. Compute checksum (first 4 bytes of double SHA-256)
        5. Concatenate and Base58 encode
        """
        pubkey_bytes: bytes = public_key.to_string()
        sha256_result: bytes = hashlib.sha256(pubkey_bytes).digest()
        payload: bytes = hashlib.new("ripemd160", sha256_result).digest()

        version_byte: bytes = b"\x00"
        payload_mainnet: bytes = version_byte + payload

        h1: bytes = hashlib.sha256(payload_mainnet).digest()
        h2: bytes = hashlib.sha256(h1).digest()
        checksum: bytes = h2[:4]

        full_result: bytes = payload_mainnet + checksum
        return base58.b58encode(full_result).decode()

    @property
    def address(self) -> str:
        """Return the public address of the wallet.

        This is derived from the public key using the following steps:
        - SHA-256 of public key
        - RIPEMD-160 of that hash
        - Prepend version byte (0x00 for Bitcoin mainnet)
        - Append checksum (first 4 bytes of double SHA-256)
        - Base58Check encode the result

        This process is described in the implementation details of Bitcoin addresses.

        Returns
        -------
            str: Public address (Base58Check encoded string).
        """
        return self._address

    @property
    def balance(self) -> float:
        """Return the current balance of the wallet based on known UTXOs.

        The wallet sums the amounts of all UTXOs it currently owns.
        This value represents how much the wallet can spend.

        Returns
        -------
            float: Total balance.
        """
        balance: float = 0.0
        for _, utxo in self._utxos.items():
            balance += utxo.amount
        return balance

    def sign_message(self, message: bytes) -> str:
        """Sign a message using the wallet's private key.

        This is typically used to sign a transaction input, proving the wallet has
        control over the UTXO being spent.

        Uses ECDSA to produce a signature, encoded in hexadecimal.

        See Section 10 of the Bitcoin whitepaper for digital signatures.

        Args:
        ----
            message (bytes): The message to be signed.

        Returns:
        -------
            str: Hex-encoded signature.
        """

    def get_utxos(self) -> dict[tuple[str, int], UTXO]:
        """Return a dictionary of UTXOs currently owned by the wallet.

        This internal UTXO list is updated whenever the wallet receives or spends coins.
        It is used to track what the wallet can spend.

        Returns
        -------
            dict[Tuple[str, int], UTXO]: List of unspent transaction outputs belonging to this wallet.
        """
        return self._utxos

    def add_utxo(self, utxo: UTXO) -> None:
        """Add a UTXO to the wallet's list of spendable outputs.

        This is called when a new transaction output is created that sends coins to
        this wallet's address. The UTXO is stored so it can be spent later.

        UTXOs are identified by the originating transaction ID and output index.

        Args:
        ----
            utxo (UTXO): The new UTXO to add.
        """
        if utxo.is_owned_by(self.address):
            if (utxo.tx_id, utxo.output_index) not in self._utxos:
                self._utxos[(utxo.tx_id, utxo.output_index)] = utxo
            else:
                logger.warning(
                    "Trying to add duplicate UTXOs:%s to  wallet:%s",
                    utxo,
                    self,
                )

    def remove_utxo(self, utxo: UTXO) -> None:
        """Remove a UTXO after it's been spent.

        When a transaction is created that uses this UTXO as an input, the UTXO
        is removed from the wallet's list to prevent double-spending.

        Args:
        ----
            utxo (UTXO): The UTXO to remove.
        """
        del self._utxos[(utxo.tx_id, utxo.output_index)]

    def create_transaction(self, recipient: str, amount: float) -> Transaction:
        """Create a signed transaction using internal UTXOs.

        This constructs a new transaction with the following logic:
        1. Select UTXOs from internal list until amount is covered
        2. Create transaction inputs referencing selected UTXOs
        3. Create transaction outputs:
           - One for recipient
           - One for change back to self (if any)
        4. Sign each input using this wallet's private key
        5. Return the signed Transaction object

        This implements the behavior described in Section 5 and 10 of the Bitcoin whitepaper.

        Args:
        ----
            recipient (str): The address/public key of the recipient.
            amount (float): The amount to send.

        Returns:
        -------
            Transaction: A signed transaction object ready for broadcasting.
        """


if __name__ == "__main__":
    w = Wallet()
