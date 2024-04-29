// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract Interaction {
    uint256 public myNumber;

    constructor() {
        myNumber = 0;
    }

    function setMyNumber(uint256 _myNumber) public {
        myNumber = _myNumber;
    }

    function getMyNumber() public view returns (uint256) {
        return myNumber;
    }
}
