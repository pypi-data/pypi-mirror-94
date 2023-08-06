from qset_feature_store.featureset_engine.dataset_manager.dataset_manager import DatasetManager
from qset_feature_store.featureset_engine.dataset_manager.local_dataset_manager import LocalDatasetManager
from qset_feature_store.repository import models
from qset_feature_store.reflexion import extract_feature_set
from qset_feature_store.featureset_engine.featureset import FeatureSet


class EngineDatasetManager(DatasetManager):
    def __init__(self, dataset_managers):
        self.dataset_managers = dataset_managers

    def get_dataset(self, dataset):
        raise Exception(f'Use get method to get dataset from dataset managers')

    def get_from_featureset(self, featureset, scope, params):
        # todo: make use of config properly
        featureset = models.cast_dict(featureset, models.FeatureSet)
        assert featureset['engine'] == 'pandas/v1'
        cls = extract_feature_set(featureset['config']['code'])
        featureset_instance = cls()
        return self.calc(featureset_instance, featureset['inputs'], scope, params)

    def calc(self, featureset_instance, inputs, scope, params):
        featureset_instance.inputs = inputs
        featureset_instance.params = params
        featureset_instance.scope = scope
        featureset_instance.dataset_provider = self
        return featureset_instance.calc()

    def get_from_dataset_schema(self, configured_featureset, scope):
        featureset = models.cast_dict(configured_featureset['featureset'], models.FeatureSet)
        return self.get_from_featureset(featureset, scope, configured_featureset['params'])

    def get(self, generic_featureset, scope=None, params=None):
        generic_featureset = super()._format_generic_featureset(generic_featureset)

        # try to get from data managers first
        for manager in self.dataset_managers:
            try:
                return manager.get(generic_featureset, scope, params)
            except:
                pass

        # try to calc otherwise
        return super().get(generic_featureset, scope, params)

    def put_to_dataset_schema(self, df, dataset_schema, scope, **kwargs):
        for manager in self.dataset_managers:
            if isinstance(manager, LocalDatasetManager):
                return manager.put_to_dataset_schema(df, dataset_schema, scope, **kwargs)
        raise Exception('Could not put configured featureset')
