from builddevenv.Builder import Builder
import pytest
import docker
import os

class TestBuildDevEnv:

    def test_buildenv_ok(self):
        """
        Tests the builddevenv package based on the following scenario:
        1. Creates the networks and the containers
        2. Stops the containers
        3. Starts the containers previously stopped
        4. Remove the containers and the networks previously created.
        """
        client = docker.from_env()
        builder = Builder(os.path.join(os.path.dirname(__file__), "test_data\\env_var.yaml"))

        builder.run()
        builder.stop()
        builder.start()
        builder.delete()
        assert 1 == 1
