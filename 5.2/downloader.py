import subprocess
from pathlib import Path


# Define the file to search for
file_name = "corpus-archive-0091.tar.gz"
bucket_path = "gs://fuzzbench-data/2025-06-29-toka"
import re
import os

rg = list(range(1, 91, 4))# On

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
        # Because gsutil ls takes years if I run it from python3. dunno why. so i just put it into txt instead
        with open("list.txt") as to_download:
            all_lines = to_download.readlines()
            for line in all_lines:
                line = line.rstrip('\n')
                file_paths.append(line)
        # Step 2: Download the first matching file
        for file in file_paths:
            if "bloaty" in file or "lcms" in file:
                pass
            else:
                continue

            for numero in rg:
                print(f"Replacing it with: {numero}")
                fuzzer_type = file.split('/')[5].split('-')[-1]
                result_log = get_result_location(fuzzer_type)
                new = file.replace(file_name, f"corpus-archive-{numero:04d}.tar.gz")
                subprocess.run(["gsutil", "cp", "-r", new, "./{}".format(new[5:])], check=True)
                print(f"Downloaded {file} successfully!")
                tar_path = Path(os.getcwd()).joinpath(new[5:])
                tar_dir = tar_path.parent
                print(tar_path, tar_dir, result_log)
                os.system("tar -zxvf {} -C {} {}".format(tar_path, tar_dir, result_log))
                os.system("cd {} && mv {} default/fuzzer_stats_{}".format(tar_dir, result_log, numero))
                # then remove, cuz i don't have space
                os.system("rm -rf {}".format(tar_path))

    except subprocess.CalledProcessError:
        print(f"Error: Could not find '{file_name}' in {bucket_path}")

# Run the function
find_and_download(file_name, bucket_path)