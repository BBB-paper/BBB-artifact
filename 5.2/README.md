This folder contains the artifact for section 5.2

# Sources of experiement
The data comes from the same experiment as [C-3](https://storage.googleapis.com/fuzzbench-data/index.html?prefix=2025-06-29-toka/experiment-folders/) experiment.
We downloaded the corpus data for 15 min, 1hour + 15 min, ... until 22 hour + 15 minute,
each of them are stored in fuzzbench-z-1.csv, fuzzbench-z-5.csv, ..., fuzzbench-z-89.csv respectively inside data folder.

# (Optional) Downloading the data
We put the copies of the data in `data/` folder already.

If you want to downlown the raw data from fuzzbench yourself, you need to first generate the list to download by using `gsutil ls` command

```
gsutil ls gs://fuzzbench-data/<replace the experiment name here>/**/corpus-archive-0091.tar.gz > list.txt
```
then run
```
python3 downloader.py
```
to download

After, run
```
python3 parser.py
```
to parse all the data. then you will have csv files.

# Graphs
To generate the graph, you can use 
```
python3 calculator.py
```
