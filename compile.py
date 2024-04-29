from solcx import compile_standard, install_solc

install_solc('0.8.0')

with open('Interaction.sol', 'r') as file:
    source_code = file.read()

compiled_sol = compile_standard({
    "language": "Solidity",
    "sources": {"Interaction.sol": {"content": source_code}},
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
