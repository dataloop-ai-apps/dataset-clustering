import subprocess
import select
import logging
import os

# Configure logging
os.chdir("/")
logging.basicConfig(level=logging.INFO)
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

    def stream_logs(self, process, process_name):
        """ Stream stdout and stderr of a subprocess using select for non-blocking reading. """
        try:
            while True:
                # Wait for output from stdout or stderr
                readable, _, _ = select.select([process.stdout, process.stderr], [], [], 0.1)
                for f in readable:
                    line = f.readline()
                    if line:
                        if f is process.stdout:
                            logger.info(f"{process_name} stdout: {line.strip()}")
                        else:
                            logger.error(f"{process_name} stderr: {line.strip()}")

                # Check if the process has terminated
                if process.poll() is not None:
                    # Capture any remaining output after process termination
                    for line in process.stdout:
                        logger.info(f"{process_name} stdout: {line.strip()}")
                    for line in process.stderr:
                        logger.error(f"{process_name} stderr: {line.strip()}")
                    logger.info(f"{process_name} process finished.")
                    break
        finally:
            process.stdout.close()
            process.stderr.close()

    def run(self):
        self.stream_logs(self.tensorboard_process, "TensorBoard")
        self.stream_logs(self.delete_job_process, "DeleteOldFiles")


if __name__ == "__main__":
    runner = Runner()
    runner.run()
