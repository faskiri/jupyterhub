FROM jupyterhub/jupyterhub:0.8.1
  
EXPOSE 8000

RUN /opt/conda/bin/pip install oauthenticator swarmspawner
ADD run.sh run.sh
ADD env env
ADD jupyterhub_config.py jupyterhub_config.py
ADD userlist userlist
CMD ./run.sh
