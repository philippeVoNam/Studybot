# Studybot

## Requirements

Create a conda environment or virtual env and run the following command to install the requirements:
```
pip install -r requirements.txt
```

## Graph Generation

Run the `generate.py` file to generate the graph. The script accepts command-line arguments, to see them run:

```
python generate.py --help
```

Make sure to correctly specify the path to the local data directory.

NOTE: If different values are used for the base and schema options, then the provided queries may not function correctly.

## Queries

To run the queries:
```
python run_queries.py studyboy.n3 queries/*.txt
```

The results of the queries will be saved to the same directly as qX.out.txt
