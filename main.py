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
        self.tensorboard_cmd = '/tmp/tensorboard-projector/bazel-bin/tensorboard/tensorboard --logdir /tmp/tensorboard-projector/logs/POC --host 0.0.0.0 --port 3000 --load_fast true --path_prefix /tensorboard'
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
        logger.info('stream logs')
        self.stream_logs()
        logger.info('stream logs finished')

    def stream_logs(self):
        """ Stream stdout and stderr of both subprocesses using select for non-blocking reading. """
        streams = {
            self.tensorboard_process.stdout: "TensorBoard stdout",
            self.tensorboard_process.stderr: "TensorBoard stderr",
            self.delete_job_process.stdout: "DeleteOldFiles stdout",
            self.delete_job_process.stderr: "DeleteOldFiles stderr"
        }

        try:
            while streams:
                readable, _, _ = select.select(streams.keys(), [], [], 0.1)
                for stream in readable:
                    line = stream.readline()
                    if line:
                        logger.info(f"{streams[stream]}: {line.strip()}")
                    else:
                        # When EOF is reached, remove it from the dictionary
                        del streams[stream]

                # Check if processes have terminated and their streams are empty
                if not streams:
                    break

        finally:
            for stream in streams:
                stream.close()

    def run(self):
        logger.info('Runner run')
        self.stream_logs()


if __name__ == "__main__":
    runner = Runner()
    runner.run()
