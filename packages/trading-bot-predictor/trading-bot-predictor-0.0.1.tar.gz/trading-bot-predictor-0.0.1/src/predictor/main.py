from os.path import isfile
from typing import Final, List, Optional

from numpy import ndarray
from numpy.ma import zeros, MaskedArray
from pandas import DataFrame
from tensorflow.python.data.ops.dataset_ops import BatchDataset
from tensorflow.python.framework.ops import EagerTensor
from tensorflow.python.keras import Input, Model
from tensorflow.python.keras.callbacks import EarlyStopping, ModelCheckpoint, History
from tensorflow.python.keras.engine.functional import Functional
from tensorflow.python.keras.engine.keras_tensor import KerasTensor
from tensorflow.python.keras.layers import LSTM, Dense
from tensorflow.python.keras.optimizer_v2.adam import Adam
from tensorflow.python.keras.preprocessing.timeseries import timeseries_dataset_from_array

from predictor.converter.intraday_dto_converter import IntradayDTOConverter
from predictor.dto.intraday_dto import IntradayDTO
from predictor.dto.prediction_dto import PredictionDTO
from predictor.utils.intraday_utils import IntradayUtils
from predictor.utils.predictor_utils import PredictorUtils
from predictor.utils.utils import Utils


class Main:
    LEARNING_RATE: Final[float] = 0.001
    EPOCHS: Final[int] = 10

    @classmethod
    def fit(cls, frame: DataFrame, split_fraction: float = PredictorUtils.SPLIT_FRACTION,
            step: int = PredictorUtils.STEP, past: int = PredictorUtils.PAST, future: int = PredictorUtils.FUTURE,
            batch_size: int = PredictorUtils.BATCH_SIZE, sufficient_data: int = PredictorUtils.SUFFICIENT_DATA,
            show_visualization: bool = False) -> None:
        """
        There are between 29 and 32 data records per day
        """

        if len(frame) < sufficient_data:
            return

        # Raw Data Visualization

        if show_visualization:
            PredictorUtils.show_raw_visualization(frame)
            PredictorUtils.show_heatmap(frame)

        # Data Preprocessing

        print(
            'The selected parameters are:',
            ', '.join([PredictorUtils.TITLES[i] for i in PredictorUtils.SELECTED]),
        )

        train_split: int = int(split_fraction * int(frame.shape[0]))
        features: DataFrame = PredictorUtils.create_features(train_split, frame)

        train_data: DataFrame = features.loc[0: train_split - 1]
        val_data: DataFrame = features.loc[train_split:]

        # Training dataset

        start: int = past + future
        end: int = start + train_split

        x_train: ndarray = train_data[[i for i in range(len(PredictorUtils.SELECTED))]].values
        y_train: DataFrame = features.iloc[start:end][[PredictorUtils.CLOSE_COLUMN]]

        sequence_length: int = int(past / step)

        dataset_train: BatchDataset = timeseries_dataset_from_array(
            x_train,
            y_train,
            sequence_length=sequence_length,
            sampling_rate=step,
            batch_size=batch_size,
        )

        # Validation dataset

        x_end: int = len(val_data) - past - future

        label_start: int = train_split + past + future

        x_val: ndarray = val_data.iloc[:x_end][[i for i in range(len(PredictorUtils.SELECTED))]].values
        y_val: DataFrame = features.iloc[label_start:][[PredictorUtils.CLOSE_COLUMN]]

        dataset_val: BatchDataset = timeseries_dataset_from_array(
            x_val,
            y_val,
            sequence_length=sequence_length,
            sampling_rate=step,
            batch_size=batch_size,
        )

        inputs: Optional[EagerTensor] = None
        targets: Optional[EagerTensor] = None
        for batch in dataset_train.take(1):
            inputs, targets = batch

        print('Input shape:', inputs.numpy().shape)
        print('Target shape:', targets.numpy().shape)

        # Training

        inputs: KerasTensor = Input(shape=(inputs.shape[1], inputs.shape[2]))
        lstm_out: KerasTensor = LSTM(32)(inputs)
        outputs: KerasTensor = Dense(1)(lstm_out)

        model: Model = Model(inputs=inputs, outputs=outputs)
        model.compile(optimizer=Adam(learning_rate=cls.LEARNING_RATE), loss='mse')
        model.summary()

        es_callback: EarlyStopping = EarlyStopping(monitor='val_loss', min_delta=0, patience=5)

        checkpoint_callback: ModelCheckpoint = ModelCheckpoint(
            monitor='val_loss',
            filepath=PredictorUtils.PATH_CHECKPOINT_FILE,
            verbose=1,
            save_weights_only=True,
            save_best_only=True,
        )

        Utils.create_dir(PredictorUtils.PATH_MODEL_DIR)

        history: History = model.fit(
            dataset_train,
            epochs=cls.EPOCHS,
            validation_data=dataset_val,
            callbacks=[es_callback, checkpoint_callback],
        )
        model.save(PredictorUtils.PATH_MODEL_FILE)

        if show_visualization:
            PredictorUtils.visualize_loss(history, 'Training and Validation Loss')

    @staticmethod
    def plot_prediction(frame: DataFrame, split_fraction: float = PredictorUtils.SPLIT_FRACTION,
                        past: int = PredictorUtils.PAST, batch_size: int = PredictorUtils.BATCH_SIZE,
                        step: int = PredictorUtils.STEP, future: int = PredictorUtils.FUTURE) -> None:
        if len(frame) >= past and isfile(PredictorUtils.PATH_MODEL_FILE):
            train_split: int = int(split_fraction * int(frame.shape[0]))
            features: DataFrame = PredictorUtils.create_features(train_split, frame)

            start: int = past + future
            x_val: ndarray = features.iloc[-start:-future][[i for i in range(
                len(PredictorUtils.SELECTED))]].values
            y_val: MaskedArray = zeros(past)

            full_range: ndarray = features.iloc[-start:][[PredictorUtils.CLOSE_COLUMN]].values[::step]

            sequence_length: int = int(past / step)
            dataset_val: BatchDataset = timeseries_dataset_from_array(
                x_val,
                y_val,
                sequence_length=sequence_length,
                sampling_rate=step,
                batch_size=batch_size,
            )
            model: Functional = PredictorUtils.load_model()
            for x, y in dataset_val.take(5):
                predictions: ndarray = model.predict(x)[0]
                print(predictions)
                PredictorUtils.show_plot(
                    [full_range, predictions],
                    int(future / step),
                    'Single Step Prediction',
                    True
                )

    @staticmethod
    def predict(frame: DataFrame, split_fraction: float = PredictorUtils.SPLIT_FRACTION,
                past: int = PredictorUtils.PAST, batch_size: int = PredictorUtils.BATCH_SIZE,
                step: int = PredictorUtils.STEP, future: int = PredictorUtils.FUTURE,
                show_visualization: bool = False) -> Optional[PredictionDTO]:
        if len(frame) >= past and isfile(PredictorUtils.PATH_MODEL_FILE):
            train_split: int = int(split_fraction * int(frame.shape[0]))
            features: DataFrame = PredictorUtils.create_features(train_split, frame, False)

            x_val: ndarray = features.iloc[-past:][[i for i in range(len(PredictorUtils.SELECTED))]].values
            y_val: MaskedArray = zeros(past)

            sequence_length: int = int(past / step)
            dataset_val: BatchDataset = timeseries_dataset_from_array(
                x_val,
                y_val,
                sequence_length=sequence_length,
                sampling_rate=step,
                batch_size=batch_size,
            )
            model: Functional = PredictorUtils.load_model()
            for x, y in dataset_val.take(5):
                predictions: ndarray = model.predict(x)[0]
                print(predictions)
                if show_visualization:
                    PredictorUtils.show_plot(
                        [x[0][:, 1].numpy(), predictions],
                        int(future / step),
                        'Single Step Prediction',
                    )
                return PredictionDTO(predictions[0] - x_val[-1:][0][PredictorUtils.CLOSE_COLUMN])


if __name__ == '__main__':
    IntradayUtils.write_time_series_intraday_extended()
    intraday_list: List[IntradayDTO] = IntradayUtils.read_time_series_intraday_extended()
    intraday_list.sort(key=lambda intraday: intraday.date)
    intraday_frame: DataFrame = IntradayDTOConverter.to_dataframe(intraday_list)
    Main.fit(frame=intraday_frame, show_visualization=True)
    Main.predict(frame=intraday_frame, show_visualization=True)
    Main.plot_prediction(frame=intraday_frame)
