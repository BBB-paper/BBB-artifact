This folder contains the artifact for the experiment C-1 to C-4.

# Sources of experiement

The original experiment result can be found at

- C-1: The data is in c1.csv. This is a local experiment.
- C-2: The data is in c2.csv. It comes from fuzzbench experiment: [source](https://storage.googleapis.com/fuzzbench-data/index.html?prefix=2025-06-06-toka-2/)

- C-3: The data is in c3.csv. It comes from fuzzbench experiment: [source](https://storage.googleapis.com/fuzzbench-data/index.html?prefix=2025-06-29-toka/)
- C-4: The data is in c4.csv. It comes from fuzzbench experiment: [source](https://storage.googleapis.com/fuzzbench-data/index.html?prefix=2025-06-11-toka-normal/)

# (Optional) Downloading the data
We put the copies of the data in `c1.csv`, `c2.csv`, `c3.csv`, and `c4.csv` already.
If you want to download the data from fuzzbench yourself, continue on this section.

For C-2, C-3, C-4. You need to download the data first.
To do so, you need to list up all the trials that needs download first.
The 91th frame is the snapshot taken after 22hours and 45 minutes, and we look for this.
Therefore we use `gsutil ls` to list up everything and put them into `list.txt`

```
gsutil ls gs://fuzzbench-data/<replace the experiment name here>/**/corpus-archive-0091.tar.gz > list.txt
```

then you can run python3 download.py to actually download them after you put the correct `bucket_path`.
`bucket_path` is the experiment name
```
python3 downloader.py
```

After that you should run
```
python3 parser.py
```
to parse all the result into `result.csv`. Then you get the same result as our attached csvs.

# CV, QCD analysis.
To get the result of CV, and QCD presented in Table 1, 2, 3. You can run
```
python3 cv_qcd.py <campaign number>
```
For example, `python3 cv_qcd.py 1` to get campaign 1 result.