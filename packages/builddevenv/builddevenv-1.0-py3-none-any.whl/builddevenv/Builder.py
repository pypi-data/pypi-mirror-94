import docker
import yaml
import time
from typing import Dict, List

__VOLUME_SEP__ = "|"

class NetworkConfig:
    """
    Simple docker network configuration
    """
    def __init__(self, name : str):
        """
        Instanciate a docker network configuration

        Args:
            name (str): The name of the configuration.
        """
        self._name = name

    @property
    def get_name(self):
        """
        Get the network configuration name.

        Returns:
            (string): The name of the configuration.
        """
        return self._name

class ContainerConfig:
    """
    Simple Docker container configuration.
    """
    def __init__(self, name : str, image : str, network : str, expose : Dict, 
    volumes : List, env : List):
        """
        Instanciate a docker container configuration

        Args:
            name (str): The name of the configuration.
            image (str): The image name and the tag to use for the container creation. For example mysql:latest.
            network (str): The network name to use to make containers communicate.
            expose (Dict): A dictionnary to bind a container port on a host port.
            volumes (List): A list of dictionnary to mount a container volume on a host volume.
            env (List): A list of string containing the environment and its value.
        """
        self._name = name
        self._image = image
        self._env = env
        self._network = network
        self._expose = expose
        self._volumes = None if volumes is None else self._generate_volumes(volumes)
                
    def _generate_volumes(self, volumes : List):
        """
        Generates a list or a dictionnary to bind the volumes on the host

        Args:
            volumes (List): List of cuples to bind container volumes to host volumes

        Returns:
            (Dict): A dictionnary if there is only one mapping.
            (List): A list of dictionnary if there are multiple mappings.
        """
        if len(volumes) == 0:
            return None
        else:
            volume_list = []
            for elem in volumes:
                volume_list.append(elem.split(__VOLUME_SEP__)[1] + ":" + elem.split(__VOLUME_SEP__)[0]) 
            return volume_list

    @property
    def get_name(self) -> str:
        """
        Get the name of the container configuration

        Returns:
        (str): The name of the configuration
        """
        return self._name
    
    @property
    def get_image(self) -> str:
        """
        Get the name of the container image

        Returns:
        (str): The name of the container image
        """
        return self._image
    
    @property
    def get_volumes(self):
        """
        Get the volumes to bind

        Returns:
        (List): In the case several volumes are bind, it returns a list of dictionnary
        (Dict) : In the case one volume is bind, it returns a list of dictionnary
        """
        return self._volumes

    @property
    def get_env(self):
        """
        Get the list of the environment variables

        Returns:
        (List): Returns the list of the environment variables.
        """
        return self._env

    @property
    def get_network(self):
        """
        Get the name of the network.

        Returns:
        (str): Returns the network name to which the container is attached.
        """
        return self._network

    @property
    def get_expose(self):
        """
        Get the ports from the container to bind to the host

        Returns:
        (Dict): Returns a dictionnary specifying the binding of the container ports with the host ports.
        """
        return self._expose

class Builder:
    """
    Orchestrate the operations on the docker instance
    """
    def __init__(self, config_file : str) -> None:
        """
        Instanciate the builder with the YAML configuration file

        Args:
        (config_file): Path to the YAML configuration file.
        """
        self._client = docker.from_env()
        self._config_file = config_file
        self._container_config, self._network_config = self._read_yaml_file()

        

    def _read_yaml_file(self):
        """
        Read and analyze the YAML configuration file

        Returns:
        (List, List): Returns a list of ContainerConfig objects and a List of NetworkConfig objects.
        """
        config_file = open(self._config_file)
        config = yaml.load(config_file,  Loader=yaml.FullLoader)
        container_config = []
        network_config = []
        
        for elem in config["env"]:
            if "container" in elem:
                volumes = None if "volumes" not in elem else elem["volumes"]
                env = None if "env" not in elem else elem["env"]
                expose = None if "expose" not in elem else elem["expose"]
                network = None if "network" not in elem else elem["network"]

                obj = ContainerConfig(name = elem["name"], image = elem["image"], 
                 network=network, expose = expose, env = env, volumes = volumes)
                
                container_config.append(obj)
            elif "network" in elem:
                obj = NetworkConfig(name = elem["name"])
                network_config.append(obj)
        return container_config,network_config

    def run(self):
        """
        Based on the List of ContainerConfig objects and NetworkConfig objects, it creates the networks 
        and the containers in Docker.
        """
        for elem in self._network_config:
            self._client.networks.create(elem.get_name)
            time.sleep(2)

        for elem in self._container_config :
            container = self._client.containers.run(name = elem.get_name, image=elem.get_image, ports = elem.get_expose, 
            network = elem.get_network, volumes = elem.get_volumes, environment = elem.get_env, detach=True)
            count = 0
            while str(container.status).lower() != "running":
                if count == 5:
                    break
                else:
                    count += 1
                time.sleep(5)
            
    def start(self):
        """
        Starts containers which have been previously stopped, based on the configuration file.
        """
        container_list = self._client.containers.list(all=True)
        for elem in self._container_config :
            container = None
            for container_listed in container_list:
                if container_listed.name == elem.get_name:
                    container = container_listed
                    break
            container.start()
            time.sleep(5)

    def stop(self):
        """
        Stops the containers which have been created, based on the configuration file.
        """
        container_list = self._client.containers.list()
        for elem in self._container_config :
            container = None
            for container_listed in container_list:
                if container_listed.name == elem.get_name:
                    container = container_listed
                    break
            container.stop()
            time.sleep(3)
    
    def delete(self):
        """
        Stops and deletes the containers which have been created and the networks, based on the configuration file.
        """
        container_list = self._client.containers.list()
        for elem in self._container_config :
            container = None
            for container_listed in container_list:
                if container_listed.name == elem.get_name:
                    container = container_listed
                    break
            container.stop()
            container.remove()
            time.sleep(3)

        network_list = self._client.networks.list()
        for elem in self._network_config:
            network = None
            for network_listed in network_list:
                if network_listed.name == elem.get_name:
                    network = network_listed
                    break
            network.remove()
            time.sleep(1)


    def show_all(self):
        """
        Shows the containers which have been created based on the configuration file.
        """
        container_list = self._client.containers.list()
        for elem in container_list:
            container = self._client.containers.get(elem)
            print("id: %s, name: %s, image: %s, status: %s" % (container.id, container.name, container.image, container.status))
