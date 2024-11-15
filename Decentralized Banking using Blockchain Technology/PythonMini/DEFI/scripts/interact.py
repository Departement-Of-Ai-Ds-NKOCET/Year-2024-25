import os
from brownie import Contract, accounts
from dotenv import load_dotenv
load_dotenv()

def main():
    account = accounts.add(os.getenv("PRIVATE_KEY"))
    usdc_contract = Contract("0x8d79Ff7CEf97037649eB2921d72a27D13BBC2CAc")
    defi_contract = Contract("0xA31C0e25409EC88fdBcFeb9A5E92E19aEcf4b5cC")

    print(f"Before Function call Current usdc token deposit balance is {defi_contract.depositBalance(account)}")

    usdc_contract.approve(defi_contract, 10000, {"from": account})
    defi_contract.depositToken(10000, {"from": account})

    print(f"After function call Current usdc token deposit balance is {defi_contract.depositBalance(account)}")

    defi_contract.withdraw(100, {"from": account})    

    print(f"Current balance after Withdraw usdc token deposit balance is {defi_contract.depositBalance(account)}")
