import subprocess
import logging
import os


os.chdir("/")
logger = logging.getLogger('tensorboard')

logger.info(f"Current working directory: {os.getcwd()}")


class Runner:
    def __init__(self):
        logger.info('Runner init')
        execution = subprocess.Popen('/tmp/tensorboard-projector/bazel-bin/tensorboard/tensorboard --logdir /tmp/tensorboard-projector/logs/POC --host 0.0.0.0 --port 3000 --path_prefix /tensorboard', shell=True)
        delete_job = subprocess.Popen('python3 /tmp/tensorboard-projector/deployments/delete_old_files.py /tmp/tensorboard-projector/logs/POC', shell=True)

    def run(self):
        pass


if __name__ == "__main__":
    run = Runner()
