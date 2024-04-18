import subprocess
import threading
import logging
import os

# Configure logging
os.chdir("/")
logger = logging.getLogger('tensorboard')

logger.info(f"Current working directory: {os.getcwd()}")


class Runner:
    def __init__(self):
        logger.info('Runner init')
        self.tensorboard_cmd = '/tmp/tensorboard-projector/bazel-bin/tensorboard/tensorboard --logdir /tmp/tensorboard-projector/logs/POC --host 0.0.0.0 --port 3000 --path_prefix /tensorboard'
        self.delete_job_cmd = 'python3 /tmp/tensorboard-projector/deployments/delete_old_files.py /tmp/tensorboard-projector/logs/POC'

        self.tensorboard_process = subprocess.Popen(
            self.tensorboard_cmd, shell=True,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            text=True, bufsize=1
        )
        self.delete_job_process = subprocess.Popen(
            self.delete_job_cmd, shell=True,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            text=True, bufsize=1
        )

        # Start threads to log output
        self.stream_logs(self.tensorboard_process, "TensorBoard")
        self.stream_logs(self.delete_job_process, "DeleteOldFiles")

    def stream_logs(self, process, process_name):
        """ Stream stdout and stderr of a subprocess in separate threads. """
        def log_stdout():
            for line in iter(process.stdout.readline, ''):
                logger.info(f"{process_name} stdout: {line.strip()}")
            process.stdout.close()

        def log_stderr():
            for line in iter(process.stderr.readline, ''):
                logger.error(f"{process_name} stderr: {line.strip()}")
            process.stderr.close()

        stdout_thread = threading.Thread(target=log_stdout)
        stderr_thread = threading.Thread(target=log_stderr)

        stdout_thread.start()
        stderr_thread.start()

    def run(self):
        pass


if __name__ == "__main__":
    runner = Runner()
