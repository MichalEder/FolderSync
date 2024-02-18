import os
import shutil
import hashlib
import time
import argparse
from typing import List, Set


class ItemHandler:
    """Represents a single file or directory within the synchronization process."""

    def __init__(self, item_rel_path: str, item_full_path: str) -> None:
        """
        Initializes an ItemHandler object.

        Args:
            item_rel_path: The relative path of the item within its folder.
            item_full_path: The absolute path to the item.
        """
        self.item_name = (os.path.basename(item_rel_path))
        self.item_rel_path = item_rel_path
        self.item_full_path = item_full_path

    def calculate_hash(self) -> str:
        """
        Calculates the MD5 hash of the file represented by this item.

        Returns:
            The MD5 hash as a hexadecimal string, or an empty string if an error occurs.
        """
        try:
            # Calculate hash of file
            md5_hash = hashlib.md5()
            with open(self.item_full_path, 'rb') as f:
                for chunk in iter(lambda: f.read(4096), b''):
                    md5_hash.update(chunk)

            return md5_hash.hexdigest()

        except (IOError, OSError) as e:
            print(f"Error calculating hash for {self.item_full_path}: {e}")
            return ''

    def copy_file(self, destination: str) -> None:
        """
        Copies the file to the specified destination.

        Args:
            destination: The path to copy the file to.
        """
        try:
            shutil.copy2(self.item_full_path, destination)
        except (IOError, OSError) as e:
            print(f"Error copying file {self.item_full_path}: {e}")

    def copy_dir(self, destination: str) -> None:
        """
        Copies the directory to the specified destination. Creates a necessary directories along the way.

        Args:
            destination: The path to copy the directory to.
        """
        try:
            os.makedirs(destination)
        except (IOError, OSError) as e:
            print(f"Error copying directory {self.item_full_path}: {e}")

    def delete_file(self) -> None:
        """
        Deletes the file represented by this item.
        """
        try:
            os.remove(self.item_full_path)
        except (IOError, OSError) as e:
            print(f"Error deleting file {self.item_full_path}: {e}")

    def delete_dir(self) -> None:
        """
        Deletes the directory represented by this item.
        """
        try:
            shutil.rmtree(self.item_full_path)
        except (IOError, OSError) as e:
            print(f"Error deleting directory {self.item_full_path}: {e}")


class ItemSynchronizer:
    """
    Manages synchronization between a source folder and a replica folder.
    """
    def __init__(self, source_folder: str, replica_folder: str, log_file: str, interval: int) -> None:
        """
        Initializes the synchronizer.

        Args:
            source_folder: Path to the source folder.
            replica_folder: Path to the replica folder.
            log_file: Path to the log file.
            interval: Synchronization interval in seconds.
        """
        self.source_folder = source_folder
        self.replica_folder = replica_folder
        self.log_file = log_file
        self.interval = interval

    def synchronize(self) -> None:
        """
        Performs a synchronization between the source and replica folders.
        """
        # Define source and replica files with file list of replica and source folder
        source_items: List[ItemHandler] = self.get_item_list(self.source_folder)
        replica_items: List[ItemHandler] = self.get_item_list(self.replica_folder)

        self.handle_new_items(source_items, replica_items)
        self.handle_deleted_items(source_items, replica_items)
        self.handle_modified_items(source_items)

    def get_item_list(self, folder: str) -> List[ItemHandler]:
        """
        Creates a list of ItemHandler objects representing the files and directories within a folder.

        Args:
           folder: The path to the folder.

        Returns:
           A list of ItemHandler objects.
        """
        items: List[ItemHandler] = []
        for root, dirs, files in os.walk(folder, topdown=False):
            for name in dirs:
                dir_path = os.path.join(root, name)
                rel_path = os.path.relpath(dir_path, folder)
                items.append(ItemHandler(rel_path, dir_path))

            for name in files:
                file_path = os.path.join(root, name)
                rel_path = os.path.relpath(file_path, folder)
                items.append(ItemHandler(rel_path, file_path))

        return items

    def handle_new_items(self, source_items: List[ItemHandler], replica_items: List[ItemHandler]) -> None:
        """
        Handles new items in the source folder by copying them to the replica folder.

        Args:
            source_items: A list of ItemHandler objects from the source folder.
            replica_items: A list of ItemHandler objects from the replica folder.
        """
        replica_item_names: Set[str] = {item.item_rel_path for item in replica_items}

        for item in source_items:
            if item.item_rel_path not in replica_item_names:
                if os.path.isfile(item.item_full_path):
                    replica_destination = os.path.join(self.replica_folder, item.item_rel_path)
                    item.copy_file(replica_destination)
                    self.log(f'Copied: {item.item_name} to {replica_destination}')
                elif os.path.isdir(item.item_full_path):
                    replica_destination = os.path.join(self.replica_folder, item.item_rel_path)
                    item.copy_dir(replica_destination)
                    self.log(f'Created directory: {item.item_name} in {replica_destination}')

    def handle_deleted_items(self, source_items: List[ItemHandler], replica_items: List[ItemHandler]) -> None:
        """
        Handles deleted items in the replica folder by removing them.

        Args:
            source_items: A list of ItemHandler objects from the source folder.
            replica_items: A list of ItemHandler objects from the replica folder.
        """
        source_items_paths: Set[str] = {item.item_rel_path for item in source_items}
        for item in replica_items:
            if item.item_rel_path not in source_items_paths:
                replica_destination = os.path.join(self.replica_folder, item.item_rel_path)
                if os.path.isfile(item.item_full_path):
                    item.delete_file()
                    self.log(f'Deleted: {item.item_name} from {replica_destination}')
                elif os.path.isdir(item.item_full_path):
                    item.delete_dir()
                    self.log(f'Deleted directory: {item.item_name} from {replica_destination}')

    def handle_modified_items(self, source_items: List[ItemHandler]) -> None:
        """
        Handles modified items in the source folder by overwriting them in the replica folder.

        Args:
            source_items: A list of ItemHandler objects from the source folder.
        """
        for item in source_items:
            replica_item_path: str = os.path.join(self.replica_folder, item.item_rel_path)
            if os.path.exists(replica_item_path):
                replica_file = ItemHandler(item.item_rel_path, replica_item_path)

                if os.path.isfile(replica_file.item_full_path):
                    if item.calculate_hash() != replica_file.calculate_hash():
                        item.copy_file(replica_item_path)
                        self.log(f'Updated: {replica_item_path}')

    def log(self, message: str):
        """
        Logs a message to the log file and prints it to the console.

        Args:
            message: The message to log.
        """
        timestamp: str = time.strftime('%Y-%m-%dT%H:%M:%S')
        log_entry: str = f'{timestamp}  {message}\n'
        with open(self.log_file, 'a') as f:
            f.write(log_entry)
        print(log_entry, end=' ')


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Folder Synchronization Utility")
    parser.add_argument("source", help="Path to the source folder")
    parser.add_argument("replica", help="Path to the replica folder")
    parser.add_argument("log_file", help="Path to the log file")
    parser.add_argument("-i", "--interval", type=int, default=60, help="Synchronization interval (seconds)")
    args = parser.parse_args()

    try:
        if not os.path.exists(args.source):
            raise ValueError("Source folder does not exist")
        if not os.path.exists(args.replica):
            raise ValueError("Replica folder does not exist")

    except ValueError as e:
        print(f"Error: {e}")
        exit(1)
    synchronizer = ItemSynchronizer(args.source, args.replica, args.log_file, args.interval)

    while True:
        synchronizer.synchronize()
        print("Synchronization is running..")
        os.system('cls')
        time.sleep(args.interval)
