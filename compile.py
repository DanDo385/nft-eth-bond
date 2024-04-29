from solcx import compile_standard, install_solc

install_solc('0.8.0')

with open('BondPriceGenerator.sol', 'r') as file:  # Ensure this file name matches your Solidity file name
    source_code = file.read()

compiled_sol = compile_standard({
    "language": "Solidity",
    "sources": {"BondPriceGenerator.sol": {"content": source_code}},  # Changed from "Interaction.sol"
    "settings": {
        "outputSelection": {
            "*": {
                "*": ["abi", "metadata", "evm.bytecode", "evm.bytecode.sourceMap"]
            }
        }
    },
}, solc_version='0.8.0')

with open("compiled_code.json", "w") as file:
    import json
    file.write(json.dumps(compiled_sol))
