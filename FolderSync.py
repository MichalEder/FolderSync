import os
import shutil
from typing import List, Set


class FileHandler:
    def __init__(self, filename: str) -> None:
        self.filename = filename

    def calculate_hash(self) -> str:
        # Calculate hash of file
        pass

    def copy(self, destination: str) -> None:
        shutil.copy2(self.filename, destination)

    def delete(self):
        os.remove(self.filename)


class FolderSynchronizer:
    def __init__(self, source_folder: str, replica_folder: str, log_file: str, interval: int):
        self.source_folder = source_folder
        self.replica_folder = replica_folder
        self.log_file = log_file
        self.interval = interval

    def synchronize(self) -> None:
        # Define source and replica files with file list of replica and source folder
        source_files: List[FileHandler] = self.get_file_list(self.source_folder)
        replica_files: List[FileHandler] = self.get_file_list(self.replica_folder)

        # Handle new/modified/deleted files
        self.handle_new_files(source_files, replica_files)
        self.handle_deleted_files(source_files, replica_files)
        self.handle_modified_files(source_files, replica_files)


    def get_file_list(self, folder: str) -> List[FileHandler]:
        # return list of files in folder
        files: List[FileHandler] = []
        for filename in os.listdir(folder):
            full_path = os.path.join(folder, filename)
            if os.path.isfile(full_path):
                files.append(FileHandler(full_path))
        return files


    def handle_new_files(self, source_files: List[FileHandler], replica_files: List[FileHandler]) -> None:
        # check existence of file from source in replica
        # source_filenames: Set[str] = {file_obj.filename for file_obj in source_files}
        replica_filenames: Set[str] = {file_obj.filename for file_obj in replica_files}

        for file in source_files:
            if file.filename not in replica_filenames:
                replica_destination = os.path.join(self.replica_folder, os.path.basename(file.filename))
                file.copy(replica_destination)
                self.log(f'Copied: {file.filename} to {replica_destination}')

    def handle_deleted_files(self, source_files: List[FileHandler], replica_files: List[FileHandler]) -> None:
        # check existence of file in replica
        source_filenames: Set[str] = {file_obj.filename for file_obj in source_files}
        # replica_filenames: Set[str] = {file_obj.filename for file_obj in replica_files}

    def handle_modified_files(self, source_files, replica_files):
        for file in replica_files:
            if file.filename not in source_filenames:
                file.delete()
                self.log(f'Deleted: {file.filename} from {self.replica_folder}')

    def handle_modified_files(self, source_files: List[FileHandler]) -> None:
        # compare hash of files, if not same overwrite file in replica
        pass
        for source_file in source_files:

    def log(self, message):
                if source_file.calculate_hash() != replica_file.calculate_hash():
                    source_file.copy(replica_file_path)
                    self.log(f'Updated: {replica_file_path}')

        # log changes in logfile
        pass
