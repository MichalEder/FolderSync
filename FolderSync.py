import os


class FileHandler:
    def __init__(self, filename):
        self.filename = filename

    def calculate_hash(self):
        # Calculate hash of file
        pass


class FolderSynchronizer:
    def __init__(self, source_folder, replica_folder, log_file, interval):
        self.source_folder = source_folder
        self.replica_folder = replica_folder
        self.log_file = log_file
        self.interval = interval

    def synchronize(self):
        # Define source and replica files with file list of replica and source folder
        # Handle new/modified/deleted files
        pass

    def get_file_list(self, folder):
        # return list of files in folder
        files = []
        for filename in os.listdir(folder):
            full_path = os.path.join(folder, filename)
            if os.path.isfile(full_path):
                files.append(FileHandler(full_path))
        return files


    def handle_new_files(self, source_files, replica_files):
        # check existence of file from source in replica if not present copy file
        pass

    def handle_deleted_files(self, source_files, replica_files):
        # check existence of file in replica
        pass

    def handle_modified_files(self, source_files, replica_files):
        # compare hash of files, if not same overwrite file in replica
        pass

    def log(self, message):
        # log changes in logfile
        pass
