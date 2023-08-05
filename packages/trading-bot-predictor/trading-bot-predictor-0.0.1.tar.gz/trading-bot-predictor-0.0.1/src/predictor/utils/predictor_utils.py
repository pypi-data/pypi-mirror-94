import os
from typing import Final, List, Iterable

import matplotlib.pyplot as plt
from matplotlib.colorbar import Colorbar
from numpy import ndarray, divide
from pandas import DataFrame, Series
from tensorflow.python.keras.callbacks import History
from tensorflow.python.keras.engine.functional import Functional
from tensorflow.python.keras.models import load_model

from predictor.exception.predictor_exception import PredictorException


class PredictorUtils:
    FEATURE_KEYS: Final[List[str]] = ['close', 'high', 'low', 'open', 'volume', ]
    COLORS: Final[List[str]] = ['blue', 'orange', 'green', 'red', 'purple', 'brown', 'pink', 'gray', 'olive', 'cyan', ]
    TITLES: Final[List[str]] = ['Close', 'High', 'Low', 'Open', 'Volume', ]
    DATE_TIME_KEY: Final[str] = 'date'
    PAST: Final[int] = 720
    FUTURE: Final[int] = 72
    STEP: Final[int] = 6
    SELECTED: Final[List[int]] = [0, 1, 2, 3, 4]
    SPLIT_FRACTION: Final[float] = 0.715
    BATCH_SIZE: Final[int] = 256
    CLOSE_COLUMN: Final[int] = 0
    SUFFICIENT_DATA: Final[int] = 20000
    PATH_CHECKPOINT_FILE: Final[str] = os.path.join('..', '..', 'model', 'model_checkpoint.h5')
    PATH_MODEL_FILE: Final[str] = os.path.join('..', '..', 'model', 'model.h5')
    PATH_MODEL_DIR: Final[str] = os.path.join('..', '..', 'model')

    @classmethod
    def show_raw_visualization(cls, data: DataFrame) -> None:
        time_data: Series = data[cls.DATE_TIME_KEY]
        fig, axes = plt.subplots(
            nrows=3, ncols=2, figsize=(15, 20), dpi=80, facecolor='w', edgecolor='k'
        )
        for i in range(len(cls.FEATURE_KEYS)):
            key: str = cls.FEATURE_KEYS[i]
            c: str = cls.COLORS[i % (len(cls.COLORS))]
            t_data: Series = data[key]
            t_data.index = time_data
            t_data.head()
            ax = t_data.plot(
                ax=axes[i // 2, i % 2],
                color=c,
                title='{} - {}'.format(cls.TITLES[i], key),
                rot=25,
            )
            ax.legend([cls.TITLES[i]])
        plt.tight_layout()

    @staticmethod
    def show_heatmap(data: DataFrame) -> None:
        plt.matshow(data.corr())
        plt.xticks(range(data.shape[1]), data.columns, fontsize=14, rotation=90)
        plt.gca().xaxis.tick_bottom()
        plt.yticks(range(data.shape[1]), data.columns, fontsize=14)
        cb: Colorbar = plt.colorbar()
        cb.ax.tick_params(labelsize=14)
        plt.title('Feature Correlation Heatmap', fontsize=14)
        plt.show()

    @staticmethod
    def normalize(data: ndarray, train_split: int, split: bool = True) -> ndarray:
        if split:
            data_mean: ndarray = data[:train_split].mean(axis=0)
            data_std: ndarray = data[:train_split].std(axis=0)
        else:
            data_mean: ndarray = data.mean(axis=0)
            data_std: ndarray = data.std(axis=0)
        return divide(data - data_mean, data_std)

    @staticmethod
    def visualize_loss(history: History, title: str) -> None:
        loss: List[float] = history.history['loss']
        val_loss: List[float] = history.history['val_loss']
        epochs: Iterable = range(len(loss))
        plt.figure()
        plt.plot(epochs, loss, 'b', label='Training loss')
        plt.plot(epochs, val_loss, 'r', label='Validation loss')
        plt.title(title)
        plt.xlabel('Epochs')
        plt.ylabel('Loss')
        plt.legend()
        plt.show()

    @staticmethod
    def show_plot(plot_data: List[ndarray], delta: int, title: str, full_range: bool = False) -> None:
        labels: List[str] = ['History', 'Model Prediction']
        marker: List[str] = ['.-', 'go']
        shift: int = delta if full_range else 0
        time_steps: List[int] = list(range(shift - (plot_data[0].shape[0]), shift))
        if delta:
            future: int = delta
        else:
            future: int = 0
        plt.title(title)
        for i, val in enumerate(plot_data):
            if i:
                plt.plot(future, plot_data[i], marker[i], markersize=10, label=labels[i])
            else:
                plt.plot(time_steps, plot_data[i].flatten(), marker[i], label=labels[i])
        plt.legend()
        plt.xlim([time_steps[0], (future + 5) * 2])
        plt.xlabel('Time-Step')
        plt.show()

    @classmethod
    def create_features(cls, train_split: int, frame: DataFrame, split: bool = True) -> DataFrame:
        selected_features: List[str] = [cls.FEATURE_KEYS[i] for i in cls.SELECTED]
        features: DataFrame = frame[selected_features]
        features.index = frame[cls.DATE_TIME_KEY]
        features.head()
        features: ndarray = cls.normalize(features.values, train_split, split)
        features: DataFrame = DataFrame(features)
        features.head()
        return features

    @classmethod
    def load_model(cls) -> Functional:
        if not os.path.isfile(cls.PATH_MODEL_FILE):
            raise PredictorException('No model available')
        return load_model(os.path.join(cls.PATH_MODEL_FILE))
