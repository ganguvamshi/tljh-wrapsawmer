# tljh-wrapsawmer
TJLH plugin to use [WrapSpawner](https://github.com/jupyterhub/wrapspawner) to spin up both [SystemdSpawner](https://github.com/jupyterhub/systemdspawner) and [DockerSpawner](https://jupyterhub-dockerspawner.readthedocs.io/en/latest/)


# Install

include `--plugin thljh-wrapspawner` in yout TLJH install script. For example, here user `juser` with passsword `hellojhub` installs TLJH with `tjlh-wrapspawner`:

```
#!/bin/bash 
curl https://raw.githubusercontent.com/jupyterhub/the-littlest-jupyterhub/master/bootstrap/bootstrap.py \
  | sudo python3 - \
    --admin juser:hellojhub --plugin git+https://github.com/pennchildlanglab/tljh-datascience
    
```

