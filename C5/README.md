This folder contains the artifact for the experiment C-5.

# Sources of experiement
The original 9 experiment result can be found at

- [20210411 exp](https://www.fuzzbench.com/reports/2021-04-11-7d-paper/index.html) [data](https://www.fuzzbench.com/reports/2021-04-11-7d-paper/data.csv.gz)
- [20210423 exp](https://www.fuzzbench.com/reports/2021-04-23-7d-paper/index.html) [data](https://www.fuzzbench.com/reports/2021-04-23-7d-paper/data.csv.gz)
- [20210423(2nd) exp](https://www.fuzzbench.com/reports/2021-04-23-paper/index.html) [data](https://www.fuzzbench.com/reports/2021-04-23-paper/data.csv.gz)
- [20210426 exp](https://www.fuzzbench.com/reports/2021-04-26-repro-paper/index.html) [data](https://www.fuzzbench.com/reports/2021-04-26-repro-paper/data.csv.gz)
- [20210502 exp](https://www.fuzzbench.com/reports/2021-05-02-repro-paper/index.html) [data](https://www.fuzzbench.com/reports/2021-05-02-repro-paper/data.csv.gz)
- [20210525 exp](https://www.fuzzbench.com/reports/experimental/2021-05-25-symccafl/index.html) [data](https://www.fuzzbench.com/reports/experimental/2021-05-25-symccafl/data.csv.gz)
- [20210529 exp](https://www.fuzzbench.com/reports/experimental/2021-05-29-symccafl/index.html) [data](https://www.fuzzbench.com/reports/experimental/2021-05-29-symccafl/data.csv.gz)
- [20210601 exp](https://www.fuzzbench.com/reports/experimental/2021-06-01-symccafl/index.html) [data](https://www.fuzzbench.com/reports/experimental/2021-06-01-symccafl/data.csv.gz)
- [20210602 exp](https://www.fuzzbench.com/reports/experimental/2021-06-02-symccafl-pp/index.html) [data](https://www.fuzzbench.com/reports/experimental/2021-06-02-symccafl-pp/data.csv.gz)

We could not put all the csv here, since the file is too large for github to host, but we pro

# (Optional) Downloading the data & Parsing the data.
For each of these experiments, you can download the corresponding `data.csv.gz` via the links above.
Since we are only interested in the coverage value after 23 hours, we need to cut the data at 23 hours (82800 seconds) by doing.
```
df = df[df['time'] == 82800]
```
In the provided `analysis.ipynb`, we did this for you and put the data in `df.csv` already in the __second__ code cell.

# Generating the graphs.
You can use our ipynb to generate all the graphs. 
Run this command inside this directory.
```
jupyter lab
```
Similarly, the data for the Table 4 is written into cv.csv