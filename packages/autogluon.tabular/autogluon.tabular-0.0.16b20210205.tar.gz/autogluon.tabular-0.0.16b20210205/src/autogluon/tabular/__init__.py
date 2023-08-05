import logging

from autogluon.core.dataset import TabularDataset
from autogluon.core.features.feature_metadata import FeatureMetadata

from .task.tabular_prediction import TabularPrediction
from .predictor import TabularPredictor

logging.basicConfig(format='%(message)s')  # just print message in logs
