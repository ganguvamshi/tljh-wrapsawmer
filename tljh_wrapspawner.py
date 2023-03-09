from tljh.hooks import hookimpl
from tljh.user import ensure_user_group
import subprocess


@hookimpl
def tljh_config_post_install(config):
    """
    Set JupyterLab to default
    """
    user_environment = config.get('user_environmnet', {})
    user_environment['default_app'] = user_environment.get('default_app', 'jupyterlab')
    
    config['user_environment'] = user_environment




@hookimpl
def tljh_post_install():
    """
    Install DockerSpawner, WrapSpawner and setup the notebook0
    """
    def install_dockerspawner():
        subprocess.call("sudo /opt/tljh/hub/bin/python3 -m pip install dockerspawner jupyter_client", shell=True)


    def install_wrap_spawner():
        subprocess.call("sudo /opt/tljh/hub/bin/python3 -m pip install wrapspawner", shell=True)
        get_docker_image()
        get_docker_singlecell()
        tljh_use_wrapspawner()
    
    def tljh_use_wrapspawner():
        
        # create the wrapspawner config file
        f = open('/opt/tljh/config/jupyterhub_config.d/wrapspawner_tljh_config.py', 'w')

        # add the details to configure dockerspaner
        contents= [
            "c.JupyterHub.spawner_class = 'wrapspawner.ProfilesSpawner'",
            "c.Spawner.http_timeout = 120",
            "c.ProfilesSpawner.profiles = [",
                "\t('Host process','local','systemdspawner.SystemdSpawner' , {'ip':'0.0.0.0'} )," ,
                "\t('Docker (singlecell)' ,'singlecell', 'dockerspawner.SystemUserSpawner', dict(image=\"rnakato/singlecell_jupyter:latest\") ),",
                "\t('Docker (Renv)' ,'datascience', 'dockerspawner.SystemUserSpawner', dict(image=\"jupyter/datascience-notebook:r-4.0.3\") )",
            "]",
            "c.DockerSpawner.image_whitelist = ['rnakato/singlecell_jupyter:latest','jupyter/datascience-notebook:r-4.0.3']",
            "from jupyter_client.localinterfaces import public_ips",
            "c.JupyterHub.hub_ip = public_ips()[0]",
            "c.DockerSpawner.name_template = '{prefix}-{username}-{servername}'"
        ]

        # add to the config file
        for line in contents:
            f.write(line)
            f.write("\n")
        f.close()


    def get_docker_image():
        subprocess.call("sudo docker pull jupyter/datascience-notebook:r-4.0.3", shell=True)
        restart_tljh()
    
    def get_docker_singlecell():
        subprocess.call("sudo docker pull rnakato/singlecell_jupyter:latest",  shell=True)
        restart_tljh()
    
    # and the restart TLJH and rebuild jupyterlab
    def restart_tljh():
        subprocess.call("sudo tljh-config reload", shell=True)
    
    install_dockerspawner()
    install_wrap_spawner()
    

@hookimpl
def tljh_new_user_create(username):
    ensure_user_group(username, 'docker')