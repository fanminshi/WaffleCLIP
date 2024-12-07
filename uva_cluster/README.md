# Scripts to run WaffleCLIP on the university of Amsterdam Cluster

## Setup
First you need to install environment.

```sh
$ cd WaffleCLIP
$ sbatch uva_cluster/install_env.job
```

Then you need to create a `.env` file in the /WaffleCLIP directory, containing the following variables:
- `USER`: Snellius username (e.g. dvdmast) (REQUIRED)
- `OPENAI_API_KEY`: OpenAI key (OPTIONAL: Needed from `generate_descriptors.py`)


## Evaluation
After that is done, we need to download the datasets, which will be done in your `scratch-shared` folder automatically using the `eval.job` script. Currently, I set them at `/scratch-shared/{username}/waffle-data`.
All datasets except imagenet will be downloaded automatically. 

Then we run the eval code.
```sh
$ sbatch uva_cluster/eval.job
```

## Generate_descriptors
To generate descriptors for a new dataset, you need to edit the generate_descriptors.py file to load the dataset you want descriptors for. Be sure to edit the .json path at the bottom of the file.
Then we run the generate_descriptors code.
```sh
$ sbatch generate_descriptors.job
```