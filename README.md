# Cryptics-Learning

## Goal
Refresh my knowledgde of blockchain and crypto related projects. 

# Cryptics Learning: Bitcoin-Inspired Blockchain

This project is a full simulation of a Bitcoin-like blockchain based on the original whitepaper. It includes core blockchain mechanics, transactions, wallets, miners.

## Based on Bitcoin Whitepaper Sections
- Section 2: Transactions
- Section 3: Timestamp Server
- Section 4: Proof-of-Work
- Section 5: Network
- Section 6: Incentive
- Section 10: Privacy
- Section 11: Combining and Splitting Value

## Modules Overview

### Block
Defines a single block. Tracks index, timestamp, data, previous hash, nonce, and hash. Handles PoW mining.
- **Status**: Implemented

### Blockchain
Handles block creation, validation, chain growth, and chain integrity checks.
- **Status**: Implemented

### Transaction
Implements UTXO-style transactions. Contains inputs, outputs, digital signatures. Validates spendability.
- **Status**: Not implemented

### Wallet
Generates key pairs. Manages UTXOs. Signs transactions. Calculates balance.
- **Status**: Not implemented

### User
Owns wallets. Generates and sends transactions to others.
- **Status**: Not implemented

### Miner
Selects transactions from mempool. Mines new blocks. Earns block rewards and fees.
- **Status**: Not implemented

### Exchange
Matches orders between users. Simulate new funds flowing into the system. 
- **Status**: Not implemented

### Network / Node
Async P2P simulation of network. 
- **Status**: Not implemented
