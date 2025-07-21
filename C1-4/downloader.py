import subprocess
from pathlib import Path


file_name = "corpus-archive-0091.tar.gz"
bucket_path = "XXXXXXX" # Fill me please
import re
import os

def get_result(path: str) -> str:
    return re.sub(r'corpus/.*', 'results/fuzzer-log.txt', path)

def get_result_location(fuzzer_type):
    if fuzzer_type == "lafintel" or fuzzer_type == "afl" or fuzzer_type == "aflfast" or fuzzer_type == "aflsmart" or fuzzer_type == "fairfuzz" or fuzzer_type == "mopt":
        return "corpus/fuzzer_stats"
    elif fuzzer_type == 'eclipser':
        return "corpus/afl-worker/fuzzer_stats"
    elif fuzzer_type == 'aflplusplus' or fuzzer_type.startswith('aflplusplus'):
        return "default/fuzzer_stats"
    else:
        return "404"

def find_and_download(file_name, bucket_path):
    try:

        file_paths = []
        with open("list.txt") as to_download:
            all_lines = to_download.readlines()
            for line in all_lines:
                line = line.rstrip('\n')
                file_paths.append(line)
        for file in file_paths:
            print(f"Found file: {file}")
            fuzzer_type = file.split('/')[5].split('-')[-1]
            result_log = get_result_location(fuzzer_type)
            subprocess.run(["gsutil", "cp", "-r", file, "./{}".format(file[5:])], check=True)
            print(f"Downloaded {file} successfully!")
            tar_path = Path(os.getcwd()).joinpath(file[5:])
            tar_dir = tar_path.parent
            print(tar_path, tar_dir, result_log)
            os.system("tar -zxvf {} -C {} {}".format(tar_path, tar_dir, result_log))

            # then remove, cuz i don't have space
            os.system("rm -rf {}".format(tar_path))

    except subprocess.CalledProcessError:
        print(f"Error: Could not find '{file_name}' in {bucket_path}")

# Run the function
find_and_download(file_name, bucket_path)