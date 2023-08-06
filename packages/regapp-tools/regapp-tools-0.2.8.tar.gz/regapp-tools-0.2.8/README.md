# regapp-tools

These is a collection of (python for the moment) tools for regapp.

Main goal of this package is to have them easily installable via:

```
    pip install regapp-tools
```

The initial tools are:

- subiss-to-unix that allows finding a user that was registered via OIDC
  in regapp. Examples:

  - `subiss-to-unix <sub>@<iss>`
  - `subiss-to-unix test-id`
  - `subiss-to-unix 6c611e2a-2c1c-487f-9948-c058a36c8f0e@https://login.helmholtz-data-federation.de/oauth2`

- ssh-key-retriever (there is a go version in an rpm package available
  elsewhere). This one is for retrieving ssh-keys that users have
  registered in reg-app. Examples:

  - `ssh-key-retriever <username>`

# Installation

```
pip install regapp-tools
```

# Configuration

Both tools read config files from 
    - ./regapp-tools.conf
    - $HOME/regapp-tools.conf
    - /etc/regapp-tools.conf
in that order

## Sample Config:

```
#vim: ft=conf

[backend.bwidm]
# The base URL of the BWIDM API
url = https://bwidm-test.scc.kit.edu/rest

# The ID of the organisation
org_id = hdf

[backend.bwidm.auth]
# HTTP basic auth to connect to BWIDM API
http_user = xxxx
http_pass = xxxx

[backend.bwidm.service]
# The name of the service the user should be added to on BWIDM:
name = sshtest
```

