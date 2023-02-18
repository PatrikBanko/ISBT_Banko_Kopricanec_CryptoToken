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
adresa_vlasnika = "0xa1b561eaa185c747e601E5A032DD46fcA1AC2A44"
private_key = "0x92d3a1e43adda3618918ba7980ed691789ac0fb9f7663a7d02d9a57e6ed7f60f"

acc = Account.from_key(private_key)
print("racun: ", acc.address)

# Kreiranje ugovora
IPToken = w3.eth.contract(abi=abi, bytecode=bytecode)
# Generiranje nonce
nonce = w3.eth.getTransactionCount(adresa_vlasnika)

# Definiranje detalja o tokenu i kreiranje transakcije
naziv = input("\n\nNaziv tokena: ")
kratica = input("Kratica: ")
ukupanOpticajPy = int(input("Ukupni opticaj: "))


transaction = IPToken.constructor(ukupanOpticajPy).buildTransaction(
    {
        "chainId": chain_id,
        "from": adresa_vlasnika,
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
print("Ukupan opticaj: {} tokena".format(iptoken.functions.ukupanOpticaj().call()))
print("Stanje racuna vlasnika: {}\n".format(iptoken.functions.provjeriStanje(adresa_vlasnika).call()))
# print("Stanje racuna vlasnika: ", web3.eth.get_balance(adresa_vlasnika))

# Testiranje funkcija mint i burn
# Mint
kolicina_mint = int(input("Unesite količinu za mint: "))

print("\n_______MINT_____________________________________")
print("Ukupan opticaj prije mint-anja: {}".format(iptoken.functions.ukupanOpticaj().call()))
print("Mint u iznosu od {} tokena u tijeku...".format(kolicina_mint))
iptoken.functions.mint(kolicina_mint).transact({"from": adresa_vlasnika})
print("Ukupan opticaj poslije mint-anja: {}".format(iptoken.functions.ukupanOpticaj().call()))
print("________________________________________________\n")

# Burn
kolicina_burn = int(input("Unesite količinu za burn: "))

print("\n_______BURN_____________________________________")
print("Ukupan opticaj prije burn-anja: {}".format(iptoken.functions.ukupanOpticaj().call()))
print("Mint u iznosu od {} tokena u tijeku...".format(kolicina_burn))
iptoken.functions.burn(kolicina_burn).transact({"from": adresa_vlasnika})
print("Ukupan opticaj poslije burn-anja: {}".format(iptoken.functions.ukupanOpticaj().call()))
print("________________________________________________\n")

# Testiranje izvršavanja transakcija
adresa_drugog_korisnika = "0x869381E27274Aa9A18E028fB74E98E12C052C08B"
private_key_2 = "0xf05e86e57eff25b29ec32ccf0d3cd86f349389337dfe0b4624c1079b18029883"

print("\n_______TRANSAKCIJA______________________________")
print("Stanje računa vlasnika prije transakcije: {}".format(iptoken.functions.provjeriStanje(adresa_vlasnika).call()))
print(
    "Stanje računa drugog korisnika prije transakcije: {}\n".format(
        iptoken.functions.provjeriStanje(adresa_drugog_korisnika).call()
    )
)
kolicina_transfer = int(input("Unesite kolićinu koja će se poslati: "))
print("\nTransakcija u tijeku...\n")
iptoken.functions.transferFrom(adresa_vlasnika, adresa_drugog_korisnika, kolicina_transfer).transact(
    {"from": adresa_vlasnika}
)
print("Stanje računa vlasnika nakon transakcije: {}".format(iptoken.functions.provjeriStanje(adresa_vlasnika).call()))
print(
    "Stanje računa drugog korisnika nakon transakcije: {}".format(
        iptoken.functions.provjeriStanje(adresa_drugog_korisnika).call()
    )
)
print("________________________________________________\n")
