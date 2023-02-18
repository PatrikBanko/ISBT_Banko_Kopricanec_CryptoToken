import solcx
from solcx import compile_standard, install_solc

import json

import web3
from web3 import Web3
from eth_account import Account

with open("./IPToken.sol", "r") as file:
    IPT_file = file.read()

# print(IPT_file)

solcx.install_solc("0.8.0")
compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"IPToken.sol": {"content": IPT_file}},
        "settings": {"outputSelection": {"*": {"*": ["abi", "metadata", "evm.bytecode", "evm.bytecode.sourceMap"]}}},
    },
    solc_version="0.8.0",
)

# Spremanje kompajliranog solidity koda u json datoteku
with open("compiled_sol.json", "w") as file:
    json.dump(compiled_sol, file)

# dohvacanje bytecode i abi
bytecode = compiled_sol["contracts"]["IPToken.sol"]["IPToken"]["evm"]["bytecode"]["object"]
abi = json.loads(compiled_sol["contracts"]["IPToken.sol"]["IPToken"]["metadata"])["output"]["abi"]

# Spajanje na Ganache testnu mrezu
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))
chain_id = 1337
address_owner = "0xa1b561eaa185c747e601E5A032DD46fcA1AC2A44"
private_key = "0x92d3a1e43adda3618918ba7980ed691789ac0fb9f7663a7d02d9a57e6ed7f60f"

acc = Account.from_key(private_key)
print("racun: ", acc.address)

# Kreiranje ugovora
IPToken = w3.eth.contract(abi=abi, bytecode=bytecode)
# Generiranje nonce
nonce = w3.eth.getTransactionCount(address_owner)

# Kreiranje transakcije
naziv = "Ivana Patrik Token"
kratica = "IPT"
ukupanOpticaj = 500000


transaction = IPToken.constructor(ukupanOpticaj).buildTransaction(
    {
        "chainId": chain_id,
        # "gasPrice": w3.eth.gas_price,
        "from": address_owner,
        "nonce": nonce,
    }
)

# Potpisivanje transakcije
sign_transaction = w3.eth.account.sign_transaction(transaction, private_key=private_key)
print("\n\nPostavljanje pametnog ugovora!")

# Slanje transakcije
transaction_hash = w3.eth.send_raw_transaction(sign_transaction.rawTransaction)

# Cekanje na dovrsetak transakcije i dohvacanje racuna
print("Čekanje na završetak transakcije...")
transaction_receipt = w3.eth.wait_for_transaction_receipt(transaction_hash)
print(f"Token uspješno kreiran! Pametni ugovor postavljen na adresu -> {transaction_receipt.contractAddress}")

iptoken = w3.eth.contract(address=transaction_receipt.contractAddress, abi=abi)

# Pregled ukupnog opticaja, stanja na racunu vlasnika, imena tokena, kratice tokena, stanja na drugom racunu
print("\n\nNaziv tokena: ", naziv)
print("Kratica tokena: ", kratica)
print("Ukupan opticaj: {} tokena".format(ukupanOpticaj))
print("Stanje racuna vlasnika: ", iptoken.functions.provjeriStanje(address_owner).call())
# print("Stanje racuna vlasnika: ", web3.eth.get_balance(address_owner))

# Testiranje funkcija mint i burn
kolicina_mint = 100000
kolicina_burn = 300000
