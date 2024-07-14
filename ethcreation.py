from eth_account import Account
import os

# Generate a new Ethereum account
acct = Account.create('danish')
private_key = acct.key()
address = acct.address

# Write address and private key to .env file
env_file_path = '.env'

# Update or create .env file
with open(env_file_path, 'w') as env_file:
    env_file.write(f"ACCOUNT_ADDRESS={address}\n")
    env_file.write(f"PRIVATE_KEY={private_key}\n")

print(f'Ethereum address ({address}) and private key written to {env_file_path}')
