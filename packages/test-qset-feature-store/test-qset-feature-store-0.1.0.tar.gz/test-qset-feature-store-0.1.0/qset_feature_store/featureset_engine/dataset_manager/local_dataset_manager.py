from utils_ak.interactive_imports import *
from qset_feature_store.featureset_engine.dataset_manager.dataset_manager import DatasetManager


class LocalDatasetManager(DatasetManager):
    def __init__(self, data_path):
        self.data_path = data_path
        makedirs(self.data_path)

    def _fn(self, configured_featureset, scope=None):
        scope = scope or {}
        base_fn = str(configured_featureset['_id'])
        return os.path.join(self.data_path, 'local', scope.get('universe', 'default'), base_fn, base_fn + '.parquet')

    def get_from_dataset_schema(self, configured_featureset, scope):
        if not os.path.exists(self._fn(configured_featureset, scope=scope)):
            raise KeyError('Local configured featureset not found')
        # todo: make index properly
        df = pd_read(self._fn(configured_featureset, scope=scope))
        return df

    def put_to_dataset_schema(self, df, dataset_schema, scope, **kwargs):
        makedirs(self._fn(dataset_schema, scope=scope))
        pd_write(df, self._fn(dataset_schema, scope=scope))


def test_local_dataset_manager():
    from qset_feature_store.repository.client import QsetRepositoryClient
    cli = QsetRepositoryClient('akadaner', db='feature-store-test')

    for key in ['featureset', 'dataset_schema', 'dataset']:
        for fs in cli.get_many(key):
            cli.delete(key, fs)

    fs = cli.create_featureset('my_featureset', engine='pandas/v1', config={'code': 'print("Hello World")'})
    fs = cli.push('featureset', fs)

    cfs = cli.create_dataset_schema('my_dataset_schema', fs, params={'param': 'foo'})
    cfs = cli.push('dataset_schema', cfs)

    ldm = LocalDatasetManager('data/')

    df = pd.DataFrame([1, 2, 3], columns=['a'])

    ldm.put(df, cfs, {'universe': 'binance'})

    print(ldm.get(cfs, {'universe': 'binance'}))


if __name__ == '__main__':
    test_local_dataset_manager()
