# Ansible Callback Plugin default_hide_sensitive_data

Ce plugin permet de masquer des données sensibles (type password) dans la log d'exécution de vos playbooks.

## Cas d'usage
Vous avez chiffré des fichiers de variables via l'outil ansible-vault.
Vous chargez ces fichiers dans votre playbook et utilisez ces variables dans votre play.

**Problème : Les valeurs de ces variables s'affichent dans la log d'exécution du playbook.**

## Configuration
Les plugins de callback permettent de contrôler ce qui est affiché dans la log d'exécution d'un playbook.

Pour configurer ce plugin de callback il faut :

#### Mise en place du script de callback

Créer les folders plugins/callback
``` shell
mkdir -p plugins/callback
```

Télécharger le script de callback
``` shell
wget --directory-prefix ./plugins/callback https://si-devops-gitlab.edf.fr/DVS/callback_plugin_default_hide_sensitive_data/-/raw/master/plugins/callback/default_hide_sensitive_data.py
```

#### Éditer le fichier ansible.cfg :

Dans la section **[defaults]**
Renseigner l'entrée **stdout_callback** avec le plugin à utiliser : default_hide_sensitive_data.

Renseigner l'entrée **encrypted_vars_files_list** avec la liste des fichiers de variables chiffrées dans les valeurs doivent être masquées dans la log. (séparateur ',').

Soit on renseigne l'entrée **vault_password_file** avec le path du fichier contenant le mot de passe pour déchiffrer les fichiers de variables.
Soit on utilise l'option **--vault-password-file** dans la ligne de commande.

Renseinger l'entrée **callback_plugins** vers le path du folder contenant le plugin de callback.

Exemple :
``` ini
[defaults]
stdout_callback = default_hide_sensitive_data
encrypted_vars_files_list = vars_1_encrypted.yml, vars_2_encrypted.yml
vault_password_file = secret.txt
callback_plugins   = ./plugins/callback
```

## Test

Le but de ce test est de masquer les variables suivantes :

``` yaml
sensitive_var_1: hello
sensitive_var_2: pong
``` 

### Sans le plugin de callback

``` 
PLAY [localhost] *****************************************************************************************************************************************************************************************************************************

TASK [debug msg with only a sensitive var] ***************************************************************************************************************************************************************************************************ok: [localhost] => {
    "msg": "hello"
}

TASK [debug msg with text and a sensitive var] ***********************************************************************************************************************************************************************************************ok: [localhost] => {
    "msg": "this message contains a sensitive data hello"
}

TASK [fail task with a msg text and a sensitive var] *****************************************************************************************************************************************************************************************fatal: [localhost]: FAILED! => {"changed": false, "msg": "The system may not be provisioned according to the CMDB pong status."}

PLAY RECAP ***********************************************************************************************************************************************************************************************************************************localhost                  : ok=2    changed=0    unreachable=0    failed=1    skipped=0    rescued=0    ignored=0
``` 

### Avec le plugin de callback

``` 
PLAY [localhost] *****************************************************************************************************************************************************************************************************************************

TASK [debug msg with only a sensitive var] ***************************************************************************************************************************************************************************************************ok: [localhost] => {
    "msg": "********"
}

TASK [debug msg with text and a sensitive var] ***********************************************************************************************************************************************************************************************ok: [localhost] => {
    "msg": "this message contains a sensitive data ********"
}

TASK [fail task with a msg text and a sensitive var] *****************************************************************************************************************************************************************************************fatal: [localhost]: FAILED! => {"changed": false, "msg": "The system may not be provisioned according to the CMDB ******** status."}

PLAY RECAP ***********************************************************************************************************************************************************************************************************************************localhost                  : ok=2    changed=0    unreachable=0    failed=1    skipped=0    rescued=0    ignored=0
``` 