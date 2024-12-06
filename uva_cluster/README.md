# Scripts to run WaffleCLIP on the university of Amsterdam Cluster

First you need to install environment.

```sh
$ cd WaffleCLIP
$ sbatch uva_cluster/install_env.job
```

After that is done, we need to download the datasets, We need to modify the hardcode in WaffleCLIP/waffle_tools.py with our datapath. Currently, I set them at /scratch-shared/fshi/waffle-data for everyone.
All datasets except imagenet will be downloaded automatically. 

```
IMAGENET_DIR = '/scratch-shared/fshi/waffle-data/ImageNet2012' # REPLACE THIS WITH YOUR OWN PATH
IMAGENETV2_DIR = '/scratch-shared/fshi/waffle-data/ImageNetV2' # REPLACE THIS WITH YOUR OWN PATH
CUB_DIR = '/scratch-shared/fshi/waffle-data/cub200' # REPLACE THIS WITH YOUR OWN PATH
EUROSAT_DIR = '/scratch-shared/fshi/waffle-data/eurosat' # REPLACE THIS WITH YOUR OWN PATH
PLACES365_DIR = '/scratch-shared/fshi/waffle-data/places365' # REPLACE THIS WITH YOUR OWN PATH
PETS_DIR = '/scratch-shared/fshi/waffle-data/pets' # REPLACE THIS WITH YOUR OWN PATH
FOOD101_DIR = '/scratch-shared/fshi/waffle-data/food101' # REPLACE THIS WITH YOUR OWN PATH
DTD_DIR = '/scratch-shared/fshi/waffle-data/dtd' # REPLACE THIS WITH YOUR OWN PATH
FLOWERS102_DIR = '/scratch-shared/fshi/waffle-data/flowers102' # REPLACE THIS WITH YOUR OWN PATH
FGVCAIRCRAFT_DIR = '/scratch-shared/fshi/waffle-data/fgvcaircraft' # REPLACE THIS WITH YOUR OWN PATH
CARS_DIR = '/scratch-shared/fshi/waffle-data/cars' # REPLACE THIS WITH YOUR OWN PATH

```

Then we run the eval code.
```sh
$ sbatch uva_cluster/eval.job
```