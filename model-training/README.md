# Model training based on CPSL-label-studio

## Installation

This project is managed with `poetry`. After installing poetry, run `poetry install` (or `make install`) to install the project.

## Prepare a dataset for labeling

TODO

## Train Models

### Detection

TODO

### Field of View Estimation

Some test notebooks are located in the [notebooks][notebooks] folder. 

- [`test_fov_model.ipynb`][test-fov] is for tuning the fov algorithms. It relies on using AVstack to load the carla dataset and therefore must be run within a poetry environment (e.g., `poetry run jupyter notebook` from the `model-training` folder).

- [`test_polylidar.ipynb`][test-polylidar] is for integrating the [polylidar][polylidar] algorithm. It has minimal dependencies right now and can run without needed a poetry environment.

Model training is a work in progress!



[notebooks]: notebooks
[test-polylidar]: notebooks/test_polylidar.ipynb
[test-fov]: notebooks/test_fov_model.ipynb
[polylidar]: https://github.com/JeremyBYU/polylidar/tree/master/examples/python
[mmdet-modelzoo]: https://mmdetection.readthedocs.io/en/stable/model_zoo.html
[mmdet3d-modelzoo]: https://mmdetection3d.readthedocs.io/en/stable/model_zoo.html