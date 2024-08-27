# CPSL Label Studio

QuickStart guide for labeling data using [`label-studio`][label-studio].


## Labeling Existing Data

You're able to label data without installing anything via [`poetry`][poetry]. 

### Installation Requirements

- [`docker`][docker]: We run [`label-studio`][label-studio] through a docker container, so you must have docker installed.
- A data directory where you keep the data


### Running label studio

If docker is installed, we can run label studio via:
```
./run_label_studio.sh data_labelstudio
```
where `data_labelstudio` is the path where you want the data and login information to be stored. It's best just to keep it a local directory unless you have a reason not to.

This will run label studio in the docker container. The container posts to a localhost port that defaults at `localhost:8080`.

Open up a browser and navigate there. The first time you run this on a new machine, you will have to create an account. The account information is stored within the `data_labelstudio` directory you created and thus any other location will act as if your account doesn't exist. The accounts are not shared over the network. Make sure you remember your account information!

Once you sign up/log in, you'll see the project page. If it's your first time, then you'll need to create a new project. Add a project name and description. Also set the labeling configuration via the `Labeling Setup` tab.

After creating the project, you're able to import new data via `Go to import`. Use this to import data you have locally on your machine. Ensure that the data has already been prepared/massaged as you want it. It's difficult to go back after starting the labeling process!

## Training Models

Once you have a labeled dataset, you can also train a model using this repository. See the [model training readme][model-training-readme] for more information!


[poetry]: https://github.com/python-poetry/poetry
[docker]: https://www.docker.com/
[label-studio]: https://github.com/HumanSignal/label-studio
[model-training-readme]: model-training/README.md