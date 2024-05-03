
# Bond Auction Simulation

This project utilizes Python, Solidity, Node.js, and Ganache CLI to simulate a bond auction where bonds are minted as NFTs. The application calculates the bond's payment dates, yield to maturity (YTM), dollar value of a 1 basis point move in rates (DV01), and convexity, then prompts the user to mint the bond as an NFT.

## Prerequisites

- Node.js and npm
- Python 3
- Ganache CLI for local blockchain simulation
- Solidity for smart contract development

## Installation

Clone this repository to your local machine and navigate to the project directory.

```bash
git clone <repository-url>
cd <repository-directory>
```

## Setting Up the Local Blockchain

Before interacting with the contracts, start the local blockchain using Ganache CLI.

```bash
ganache-cli
```

Open a new terminal window to proceed with the next steps.

## Compiling the Smart Contracts

Compile the smart contracts using the provided Python script.

```bash
python3 scripts/compile.py
```

## Deploying the Smart Contracts

Deploy the smart contracts to the local blockchain.

```bash
python3 scripts/deploy.py
```

## Running the Application

Run the application to simulate the bond auction. You will be prompted to input the coupon rate and maturity for the bond.

```bash
python3 interact.py
```

Follow the interactive prompts to simulate the auction and decide whether to mint the bond as an NFT.

## Bond Details

Each bond NFT includes the following metadata:
- Payment Schedule
- Generated Price
- Yield to Maturity (YTM)
- DV01
- Convexity

The image for the NFTs is sourced from IPFS at the following URL:
[IPFS Image](https://ipfs.io/ipfs/QmV7V5qYUQYNFvQDtz8xafrd2pSSsVP5xkPSCdMAsXbrBT)

## Contributing

Contributions are welcome. Please open an issue first to discuss what you would like to change.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.

## Acknowledgments

- Node.js community
- Python Software Foundation
- Ethereum development community
