import os
from dotenv import load_dotenv
from web3 import Web3, HTTPProvider
import solcx
load_dotenv()
solcx.install_solc('0.8.0')
solcx.set_solc_version('0.8.0')

print("Using Solc version:", solcx.get_solc_version())

def compile_standard_source(file_path):
    with open(file_path, 'r') as file:
        source = file.read()

    compiled_sol = solcx.compile_standard({
        "language": "Solidity",
        "sources": {
            "YourContract.sol": {
                "content": source
            }
        },
        "settings": {
            "outputSelection": {
                "*": {
                    "*": [
                        "abi",
                        "metadata",
                        "evm.bytecode",
                        "evm.sourceMap"
                    ]
                }
            }
        }
    })
    return compiled_sol

sol_file_path = 'C:\\Users\\inika\\assignment\\abc.sol'

compiled_sol = compile_standard_source(sol_file_path)
print("Compiled Solidity contract:", compiled_sol)

abi = compiled_sol['contracts']['YourContract.sol']['ERC20Basic']['abi']
bytecode = compiled_sol['contracts']['YourContract.sol']['ERC20Basic']['evm']['bytecode']['object']

INFURA_URL = os.getenv('INFURA_URL')
PRIVATE_KEY = os.getenv('PRIVATE_KEY')
ACCOUNT_ADDRESS = os.getenv('ACCOUNT_ADDRESS')


w3 = Web3(HTTPProvider(INFURA_URL))


def check_balance_for_gas():
    balance = w3.eth.get_balance(ACCOUNT_ADDRESS)
    print("Account Balance:", w3.from_wei(balance, 'ether'), "ETH")

    gas_price = w3.to_wei('21', 'gwei')
    gas_limit = 1728712
    estimated_gas_cost = gas_limit * gas_price
    print("Estimated Gas Cost:", w3.from_wei(estimated_gas_cost, 'ether'), "ETH")

    if balance < estimated_gas_cost:
        print("Insufficient funds for gas. Please fund your account.")
        return False
    return True
def deploy_contract():
    if not check_balance_for_gas():
        return

    contract = w3.eth.contract(abi=abi, bytecode=bytecode)

    construct_txn = contract.constructor().buildTransaction({
        'from': ACCOUNT_ADDRESS,
        'nonce': w3.eth.getTransactionCount(ACCOUNT_ADDRESS),
        'gas': gas_limit,
        'gasPrice': gas_price
    })

    signed = w3.eth.account.sign_transaction(construct_txn, PRIVATE_KEY)

    try:
        
        tx_hash = w3.eth.send_raw_transaction(signed.rawTransaction)
        print("Transaction Hash:", tx_hash.hex())

       
        tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        print("Contract Deployed:", tx_receipt.contractAddress)

        
        contract_address = tx_receipt.contractAddress
        deployed_contract = w3.eth.contract(address=contract_address, abi=abi)

        
        contract_balance = deployed_contract.functions.balanceOf(ACCOUNT_ADDRESS).call()
        print("Contract Balance:", contract_balance)

    except ValueError as ve:
        print(f"Transaction failed: {ve}")
        return

deploy_contract()
