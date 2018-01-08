import os
c = get_config()

# spawn with Docker
c.JupyterHub.spawner_class = 'cassinyspawner.SwarmSpawner'
c.JupyterHub.ip = '0.0.0.0'
c.JupyterHub.hub_ip = '0.0.0.0'
c.SwarmSpawner.jupyterhub_service_name = 'jupyterhubserver'
c.SwarmSpawner.networks = ["jupyterhubstack_overlay"]
notebook_dir = os.environ.get('NOTEBOOK_DIR') or '/home/jovyan/work'
c.SwarmSpawner.notebook_dir = notebook_dir
c.SwarmSpawner.container_spec = {
        # The command to run inside the service
        'args' : ['/usr/local/bin/start-singleuser.sh'],
        'Image' : 'jupyterhub/singleuser:0.8',
        'mounts' : [],
        }

# OAuth with GitHub
c.JupyterHub.authenticator_class = 'oauthenticator.GitHubOAuthenticator'
c.Authenticator.whitelist = whitelist = set()
c.Authenticator.admin_users = admin = set()

import os

join = os.path.join
here = os.path.dirname(__file__)
with open(join(here, 'userlist')) as f:
    for line in f:
        if not line:
            continue
        parts = line.split()
        name = parts[0]
        whitelist.add(name)
        if len(parts) > 1 and parts[1] == 'admin':
            admin.add(name)

c.GitHubOAuthenticator.oauth_callback_url = os.environ['OAUTH_CALLBACK_URL']

# ssl config
ssl = join(here, 'ssl')
keyfile = join(ssl, 'ssl.key')
certfile = join(ssl, 'ssl.cert')
if os.path.exists(keyfile):
    c.JupyterHub.ssl_key = keyfile
if os.path.exists(certfile):
    c.JupyterHub.ssl_cert = certfile
