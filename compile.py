from solcx import compile_standard, install_solc
import json
import os

# Install a compatible version of the Solidity compiler
install_solc('0.8.1')

# Load the source code from file
with open('./contracts/BondNFT.sol', 'r') as file:
    source_code = file.read()

# Set the base directory for resolving node_modules path
base_path = os.getcwd()  # Gets the current working directory
node_modules_path = os.path.join(base_path, 'node_modules')

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
            "@openzeppelin=" + os.path.join(node_modules_path, '@openzeppelin/')
        ]
    }
}, solc_version='0.8.1', allow_paths=node_modules_path)

# Write the compiled contract to a JSON file
with open("compiled_code.json", "w") as file:
    file.write(json.dumps(compiled_sol))

print("Compilation successful, output saved to compiled_code.json.")
