# Ansible Callback Plugin default_hide_sensitive_data

Ce plugin permet de masquer des données sensibles (type password) dans la log d'exécution de vos playbooks.

<br>

## Matrice de compatibilité

| Ansible version | Python version |
|-----------------|----------------|
| 2.6.20          | 2.7.5          |
| 2.7.18          | 2.7.5          |
| 2.8.6           | 2.7.5          |
| 2.9.9           | 3.6.8          |

<br>

## Cas d'usage
Vous avez chiffré des fichiers de variables via l'outil ansible-vault.
Vous chargez ces fichiers dans votre playbook et utilisez ces variables dans votre play.

**Problème : Les valeurs de ces variables s'affichent dans la log d'exécution du playbook.**

<br>

## Configuration
Les plugins de callback permettent de contrôler ce qui est affiché dans la log d'exécution d'un playbook.

Pour configurer ce plugin de callback il faut :

<br>

### Mettre en place du script de callback

Télécharger le script de callback qui correspond à votre version d'Ansible.

Exemple pour la version 2.9
``` shell
wget --directory-prefix ./plugins/callback https://si-devops-gitlab.edf.fr/DVS/callback_plugin_default_hide_sensitive_data/-/raw/master/plugins/callback/2.9/default_hide_sensitive_data.py
```

<br>

### Configuration dans le fichier ansible.cfg

Dans la section **[defaults]** \
Renseigner l'entrée **stdout_callback** avec le plugin à utiliser : default_hide_sensitive_data.

Renseigner l'entrée **encrypted_vars_files_list** avec la liste des fichiers de variables chiffrées dont les valeurs doivent être masquées dans la log. (séparateur ',').

Soit on renseigne l'entrée **vault_password_file** avec le path du fichier contenant le mot de passe pour déchiffrer les fichiers de variables. \
Soit on utilise l'option **--vault-password-file** dans la ligne de commande.

Renseinger l'entrée **callback_plugins** vers le path du folder contenant le plugin de callback.

Exemple vault_password_file dans le fichier ansible.cfg :

``` ini
[defaults]
stdout_callback = default_hide_sensitive_data
encrypted_vars_files_list = vars_1_encrypted.yml, vars_2_encrypted.yml
vault_password_file = secret.txt
callback_plugins = ./plugins/callback
```

<br>

### Configuration via la command line et ansible.cfg

Exemple vault_password_file via la ligne de commande :

``` ini
[defaults]
stdout_callback = default_hide_sensitive_data
encrypted_vars_files_list = vars_1_encrypted.yml, vars_2_encrypted.yml
callback_plugins = ./plugins/callback
```

``` bash
export VAULT_PASSWORD="vault"
ansible-playbook playbook.yml --vault-password-file=.vault_pass.py -vvvv
```

<br>

## Test

Le but de ce test est de masquer les variables suivantes :

``` yaml
sensitive_var_1: hello
sensitive_var_2: pong
``` 

<br>

### Sans le plugin de callback

``` 
PLAY [localhost] *****************************************************************************************************************************************************************************************************************************

TASK [shell] *****************************************************************************************************************************************************************************************************************************
changed: [localhost] => {
    "changed": true,
    "cmd": "echo hello",
    "delta": "0:00:00.020415",
    "end": "2020-08-03 15:22:02.637153",
    "invocation": {
        "module_args": {
            "_raw_params": "echo hello",
            "_uses_shell": true,
            "argv": null,
            "chdir": null,
            "creates": null,
            "executable": null,
            "removes": null,
            "stdin": null,
            "stdin_add_newline": true,
            "strip_empty_ends": true,
            "warn": true
        }
    },
    "rc": 0,
    "start": "2020-08-03 15:22:02.616738",
    "stderr": "",
    "stderr_lines": [],
    "stdout": "hello",
    "stdout_lines": [
        "hello"
    ]
}

TASK [debug msg with only a sensitive var] ***************************************************************************************************************************************************************************************************
ok: [localhost] => {
    "msg": "hello"
}

TASK [debug msg with text and a sensitive var] ***********************************************************************************************************************************************************************************************
ok: [localhost] => {
    "msg": "this message contains a sensitive data hello"
}

TASK [fail task with a msg text and a sensitive var] *****************************************************************************************************************************************************************************************
fatal: [localhost]: FAILED! => {"changed": false, "msg": "The system may not be provisioned according to the CMDB pong status."}

PLAY RECAP ***********************************************************************************************************************************************************************************************************************************
localhost                  : ok=2    changed=0    unreachable=0    failed=1    skipped=0    rescued=0    ignored=0
``` 

### Avec le plugin de callback

``` 
PLAY [localhost] *****************************************************************************************************************************************************************************************************************************

TASK [shell] *****************************************************************************************************************************************************************************************************************************
changed: [localhost] => {
    "changed": true,
    "cmd": "echo ********",
    "delta": "0:00:00.019622",
    "end": "2020-08-03 14:38:05.689964",
    "invocation": {
        "module_args": {
            "_raw_params": "echo ********",
            "_uses_shell": true,
            "argv": null,
            "chdir": null,
            "creates": null,
            "executable": null,
            "removes": null,
            "stdin": null,
            "stdin_add_newline": true,
            "strip_empty_ends": true,
            "warn": true
        }
    },
    "rc": 0,
    "start": "2020-08-03 14:38:05.670342",
    "stderr": "",
    "stderr_lines": [],
    "stdout": "********",
    "stdout_lines": [
        "********"
    ]
}

TASK [debug msg with only a sensitive var] ***************************************************************************************************************************************************************************************************
ok: [localhost] => {
    "msg": "********"
}

TASK [debug msg with text and a sensitive var] ***********************************************************************************************************************************************************************************************
ok: [localhost] => {
    "msg": "this message contains a sensitive data ********"
}

TASK [fail task with a msg text and a sensitive var] *****************************************************************************************************************************************************************************************
fatal: [localhost]: FAILED! => {"changed": false, "msg": "The system may not be provisioned according to the CMDB ******** status."}

PLAY RECAP ***********************************************************************************************************************************************************************************************************************************
localhost                  : ok=2    changed=0    unreachable=0    failed=1    skipped=0    rescued=0    ignored=0
``` 