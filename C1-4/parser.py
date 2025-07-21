import os
from pathlib import Path
import pandas as pd
import re


records = []

def read_fuzzer_stats_afl(fuzzer_stats):
    with open(fuzzer_stats) as f:
        for line in f.readlines():
            if "start_time" in line:
                start_time = int(line.split(': ')[1])
            if "last_update" in line:
                last_update = int(line.split(': ')[1])
            if "execs_done" in line:
                execs_done = int(line.split(': ')[1])

    return last_update - start_time, execs_done


def read_fuzzer_stats_aflpp(fuzzer_stats):
    with open(fuzzer_stats) as f:
        for line in f.readlines():
            if "run_time" in line:
                run_time = int(line.split(': ')[1])
            if "execs_done" in line:
                execs_done = int(line.split(': ')[1])

    return run_time, execs_done

def read_fuzzer_stats_libfuzzer(fuzzer_stats):
    pattern = r"#(\d+).*time: (\d+)s"
    with open(fuzzer_stats) as f:
        last_100 = f.readlines()[:-100]
        for line in last_100:
            if "dft_time" in line:
                match = re.search(pattern, line)

                if match:
                    execs_done = int(match.group(1))
                    run_time = int(match.group(2))
    return run_time, execs_done

def result_path(fuzzer_type):
    if fuzzer_type == "lafintel" or fuzzer_type == "afl" or fuzzer_type == "aflfast" or fuzzer_type == "aflsmart" or fuzzer_type == "fairfuzz" or fuzzer_type == "mopt":
        return ("corpus/corpus/fuzzer_stats", "afl")
    elif fuzzer_type == 'eclipser':
        return ("corpus/corpus/afl-worker/fuzzer_stats", "afl")
    elif fuzzer_type == 'aflplusplus' or fuzzer_type.startswith('aflplusplus'):
        return ("corpus/default/fuzzer_stats", "aflpp")
    elif fuzzer_type == "libfuzzer" or fuzzer_type == "entropic":
        return ("results/fuzzer-log.txt", "libfuzzer")
    elif fuzzer_type == "honggfuzz":
        return ("404", "404")

def find_fuzzer_stats(root_dir):
    for dirpath, _, filenames in os.walk(root_dir):
        if "trial-" in dirpath.split('/')[-1]:
            # Split the path into directories
            trialroot = Path(dirpath)
            suffix, type = result_path(trialroot.parent.name.split('-')[-1])
            resultat = trialroot.joinpath(suffix)

            target = trialroot.parent.name.rsplit('-', 1)[0]
            config = trialroot.parent.name.rsplit('-', 1)[1]
            _, trial = trialroot.name.split("trial-")

            # if there's nothing then there's nothing
            if not os.path.exists(resultat):
                continue
            if type == "afl":
                run_time, execs_done = read_fuzzer_stats_afl(resultat)
            elif type == "aflpp":
                run_time, execs_done = read_fuzzer_stats_aflpp(resultat)
            elif type == "libfuzzer":
                run_time, execs_done = read_fuzzer_stats_libfuzzer(resultat)
            elif type == "404":
                print("hongg")
                continue
            else:
                print("error!!")
                exit(0)
            print(execs_done, run_time, trialroot)
            record = {"config": config, "target": target, "trial": trial, "core_number": 0, "execs_sec": execs_done/run_time, "execs_done": execs_done, "run_time": run_time}
            records.append(record)


if __name__ == "__main__":
    root_directory = os.getcwd()
    find_fuzzer_stats(root_directory)

    df = pd.DataFrame(records)
    df.to_csv("result.csv", index=False)