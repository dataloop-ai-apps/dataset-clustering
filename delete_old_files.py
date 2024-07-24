import os
import time
import datetime
import shutil
import logging
import argparse


def cleanup_old_data(log_dir):
    logger = logging.getLogger('cleanup')
    logger.info("Starting cleanup of old data.")
    current_time = datetime.datetime.now()

    for folder in os.listdir(log_dir):
        folder_path = os.path.join(log_dir, folder)
        if folder == "datasets":
            logger.info(f"Skipping folder: {folder_path}")
            continue

        if os.path.isdir(folder_path):
            is_folder_empty = True
            for file in os.listdir(folder_path):
                file_path = os.path.join(folder_path, file)
                if os.path.isfile(file_path):
                    file_time = datetime.datetime.fromtimestamp(os.path.getmtime(file_path))
                    if (current_time - file_time).total_seconds() > 3600:  # older than 1 hour
                        logger.info(f"Deleting old file: {file_path}")
                        os.remove(file_path)
                    else:
                        is_folder_empty = False  # Folder is not empty as it has at least one file not old enough

            # Check if the folder is empty after file deletion
            if is_folder_empty:
                logger.info(f"Deleting empty folder: {folder_path}")
                # remove only if folder is older than 1 hour
                folder_time = datetime.datetime.fromtimestamp(os.path.getmtime(folder_path))
                if (current_time - folder_time).total_seconds() > 3600:
                    shutil.rmtree(folder_path)
                else:
                    logger.info(f"Folder {folder_path} is not old enough to delete.")


def main(log_dir):
    while True:
        cleanup_old_data(log_dir)
        time.sleep(600)  # Wait for one hour before next cleanup


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Cleanup old directories.')
    parser.add_argument('logdir', help='Directory to clean up')
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO)
    main(args.logdir)
