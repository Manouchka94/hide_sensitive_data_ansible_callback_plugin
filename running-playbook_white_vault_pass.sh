export VAULT_PASSWORD="vault"

ansible-playbook playbook.yml --vault-password-file=.vault_pass.py -vvvv