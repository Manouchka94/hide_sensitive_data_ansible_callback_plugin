# Ansible Callback Plugin default_hide_sensitive_data

This plugin allows you to hide sensitive data (example password) in the execution log of your playbooks even when you use verbose mode.

<br>

## Compatibility matrix

| Ansible version | Python version |
|-----------------|----------------|
| 2.6.20          | 2.7.5          |
| 2.7.18          | 2.7.5          |
| 2.8.6           | 2.7.5          |
| 2.9.9           | 3.6.8          |

<br>

## Use case
You encrypted variable files using the ansible-vault tool.
You load these files into your playbook and use these variables in your play.

**Issue : Values of these variables are displayed in the playbook runtime log.**

<br>

## Configuration
Callback plugins allow you to control what is displayed in the execution log of a playbook.

To configure this callback plugin you must:

<br>

### Set up the callback script

Download the callback script that matches your version of Ansible.

Example for version 2.9
``` shell
wget --directory-prefix ./plugins/callback https://<url>/plugins/callback/2.9/default_hide_sensitive_data.py
```

<br>

### Configuration in the ansible.cfg file

In the section **[defaults]** \
Renseigner l'entrée **stdout_callback** avec le plugin à utiliser : default_hide_sensitive_data.

Fill in the entry **encrypted_vars_files_list** with the list of encrypted variable files whose values must be hidden in the log. (separator ',').

Or we fill in the entry **vault_password_file** with the path of the file containing the password to decrypt the variable files. \
Either we use the option **--vault-password-file** in the command line.

Fill in the entry **callback_plugins** to the path of the folder containing the callback plugin.

Example of ansible.cfg file :

``` ini
[defaults]
stdout_callback = default_hide_sensitive_data
encrypted_vars_files_list = vars_1_encrypted.yml, vars_2_encrypted.yml
vault_password_file = secret.txt
callback_plugins = ./plugins/callback
```

<br>

### Configuration via the command line and ansible.cfg

Example of ansible.cfg file :

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

The purpose of this test is to hide the following variables:

``` yaml
sensitive_var_1: hello
sensitive_var_2: pong
``` 

<br>

### Without the callback plugin

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

### With the callback plugin

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