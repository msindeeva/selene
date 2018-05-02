"""
This class is the abstract base class for handling model predicions
"""
from abc import ABCMeta
from abc import abstractmethod


def write_to_file(feature_predictions, info_cols, column_names, filename):
    with open(filename, 'w+') as file_handle:
        file_handle.write("{columns}\n".format(
            columns='\t'.join(column_names)))
        for info, preds in zip(info_cols, feature_predictions):
            feature_cols = '\t'.join(
                probabilities_to_string(preds))
            info_cols = '\t'.join(info)
            file_handle.write(f"{info_cols}\t{feature_cols}\n")


def probabilities_to_string(probabilities):
    return ["{:.2e}".format(p) for p in probabilities]


class PredictionsHandler(metaclass=ABCMeta):
    """
    The base class for handling model predictions.
    """
    @abstractmethod
    def __init__(self):
        self.needs_base_pred = False
        self.results = []
        self.samples = []

    @abstractmethod
    def handle_NA(self, row_ids):
        """
        Handle rows without data that we still want to write to file.
        """
        self.results.append(row_ids)
        self.samples.append([] * len(row_ids))

    @abstractmethod
    def handle_batch_predictions(self, *args, **kwargs):
        """
        Must be able to handle a batch of model predictions.
        """
        raise NotImplementedError

    @abstractmethod
    def write_to_file(self, *args, **kwargs):
        """
        Writes accumulated handler results to file.
        """
        raise NotImplementedError