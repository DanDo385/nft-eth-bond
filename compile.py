from solcx import compile_standard, install_solc
import json

# Ensure the correct version of the Solidity compiler is installed
install_solc('0.8.0')

# Load the source code from file
with open('./contracts/BondNFT.sol', 'r') as file:
    source_code = file.read()

# Compile the contract using solc
compiled_sol = compile_standard({
    "language": "Solidity",
    "sources": {
        "BondNFT.sol": {"content": source_code}
    },
    "settings": {
        "outputSelection": {
            "*": {
                "*": ["abi", "metadata", "evm.bytecode", "evm.bytecode.sourceMap"]
            }
        },
        "remappings": [
            "@openzeppelin/=./node_modules/@openzeppelin/"
        ]
    }
}, solc_version='0.8.0', allow_paths="./")

# Write the compiled contract to a JSON file
with open("compiled_code.json", "w") as file:
    file.write(json.dumps(compiled_sol))

print("Compilation successful, output saved to compiled_code.json.")
