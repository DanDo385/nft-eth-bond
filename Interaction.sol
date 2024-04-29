// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract BondPriceGenerator {
    uint256 public randomPrice;
    address public owner;

    constructor() {
        owner = msg.sender;
    }

    /** 
     * Simulates receiving a random number (for local testing).
     * In a real environment, this would be replaced with Chainlink VRF calls.
     */
    function requestRandomPrice() public {
        require(msg.sender == owner, "Only owner can request random price");
        fulfillRandomness(generateRandomNumber());
    }

    function generateRandomNumber() private view returns (uint256) {
        // Simple pseudo-random number generator
        // DO NOT use in production
        return uint256(keccak256(abi.encodePacked(block.timestamp, block.difficulty, msg.sender))) % 21 + 9980;
    }

    /**
     * Simulated callback function that would be called by Chainlink VRF.
     */
    function fulfillRandomness(uint256 randomness) private {
        uint256 scale = 21; // Scale to get 21 possible results (9980 to 10000 inclusive)
        uint256 base = 9980; // Start range at 9980 (represents 99.80)
        randomPrice = (randomness % scale + base) / 100.0; // Ensures a result between 99.80 and 100.00
    }

    // Function to reset random price (for testing purposes)
    function resetRandomPrice() public {
        require(msg.sender == owner, "Only owner can reset random price");
        randomPrice = 0;
    }
}
