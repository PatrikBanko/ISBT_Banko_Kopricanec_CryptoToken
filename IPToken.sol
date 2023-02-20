// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;
contract IPToken {
    string public naziv;
    string public kratica;
    uint256 public ukupanOpticaj;
    address public vlasnik;
    mapping(address => uint256) public Stanje;

    constructor(uint256 pocetnoStanje) {
        vlasnik = msg.sender;
        ukupanOpticaj = pocetnoStanje;
        Stanje[msg.sender] = ukupanOpticaj;
    }

    function provjeriStanje(address account) public view returns (uint256) {
        return Stanje[account];
    }

    function transferFrom(address from, address to, uint256 kolicina) public {
        require(kolicina <= Stanje[from]);
        Stanje[from] -= kolicina;
        Stanje[to] += kolicina;
    }

    function mint(uint256 amount) public {
        Stanje[msg.sender] += amount;
        ukupanOpticaj += amount;
    }

    function burn(uint256 amount) public {
        require(amount <= Stanje[msg.sender]);
        Stanje[msg.sender] -= amount;
        ukupanOpticaj -= amount;
    }

}