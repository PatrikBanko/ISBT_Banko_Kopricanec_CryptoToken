// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;
contract IPToken {
    string public naziv = "Ivana Patrik Token";
    string public kratica = "IPT";
    uint256 public ukupanOpticaj;
    address public vlasnik;
    mapping(address => uint256) public Stanje;

    event Transfer(address indexed from, address indexed to, uint256 kolicina);

    constructor(uint256 pocetnoStanje) {
        vlasnik = msg.sender;
        ukupanOpticaj = pocetnoStanje;
        Stanje[msg.sender] = ukupanOpticaj;
    }

    function provjeriStanje(address account) public view returns (uint256) {
        return Stanje[account];
    }

    function transfer(address to, uint256 kolicina) public {
        require(kolicina <= Stanje[msg.sender]);
        Stanje[msg.sender] -= kolicina;
        Stanje[to] += kolicina;
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