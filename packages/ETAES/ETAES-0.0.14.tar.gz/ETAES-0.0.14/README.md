
# Quick Start

Env Configurations
```shell
wget https://repo.continuum.io/archive/Anaconda3-2018.12-Linux-x86_64.sh
bash Anaconda3-2018.12-Linux-x86_64.sh
conda create -n <your_env_name> python=3.6
conda activate <your_env_name>
pip install -r requirements.txt
```

Put training file to folder 'data/'
```shell
cd <your_file_root>
cp <your_file_root>/<your_file_name> .
```

Configuration your own config file(Default config.yaml), configs detail show below:
```shell
.
├── basic(Basic Configurations)
  ├── names(Some Configurations of 'names' in project)
    ├── file_name(Input File Name)
  ├── paths(Some Configurations of 'paths' in project)
    ├── file_path(Input File Path)
    ├── output_models_path(Output Path Of Models)
    ├── output_schemas_path(Output Schema Of Each Operation of Each Component)
    ├── statistic_figs_path(Store URL Of Output figs of 'StatisticsGen' Component)
    ├── statistic_schemas_pat(Store URL Of Output schemas of 'StatisticsGen' Component)
  ├── models(Configurations Of Models)
    ├── model_format(Output Format Of Models)
├── layers(Detail Configurations of Each Layer)
  ├── ExampleGen(Data Reading Component)
  ├── StatisticsGen(Data Statistic Component)
  ├── SchemaGen(Schema Generation Component)
  ├── ExampleValidator(Data Abnormal Situation Filter/Data Preprocessing Component)
  ├── Transform(Data reprocessing/Data Transform Component)
  ├── Trainer(Model Traning Component)
  ├── Evaluator(Model Evaluation Component)
  ├── Pusher(Model Publish/Model saved Component)
  ├── Predictor(Model Inference Component)
```

CONFIGURATION TIPS:
+ 1.Each component can be reused, separated by "_ + suffix" (the suffix only separates different components, does not specify the order, follow the order of the configuration file). For example, if two Transform components are used, the configuration should be configured as follows:

```python
layers:
  Transform:
    QuantileTransformer_1:
      cols:
        - quantity
        - votes
      params:
        random_state: 0
    QuantileTransformer_2:
      cols:
        - rating
      params:
        random_state: 0

```
+ 2.The target object of the component is a column, so the cols parameter needs to be passed in, distinguished by "-"
+ 3.After each stage, the corresponding generated schema should be written to /output/schemas/<component>.csv

Just Run models.py is ok~
```python
python models.py
```

The current overall code structure and calling relationship are as follows:
![callgraph](./callgraph/pycallgraph.png)

【中文版】[中文版](http://git.shopeefood-algo.i.toc-foody.shopee.io/algosenate/colosseum/-/blob/dev/dev/jiawei/README_CN.md)
