from qset_feature_store.featureset_engine.dataset_manager.local_dataset_manager import LocalDatasetManager
from qset_feature_store.featureset_engine.dataset_manager.engine_dataset_manager import EngineDatasetManager


dms = []
dms.append(LocalDatasetManager('data/'))
qdm = qset_dataset_manager = EngineDatasetManager(dms)


def test_calc():
    import sys
    sys.path.append(r'C:\Users\Mi\Desktop\master\code\git\2020.09-qset\qset-feature-store')
    from qset_feature_store import FeatureSet
    import pandas as pd
    class TrivialFeatureSet(FeatureSet):
        def calc(self):
            return pd.DataFrame([1, 2, 3], columns=['a'])

    import sys
    sys.path.append(r'C:\Users\Mi\Desktop\master\code\git\2020.09-qset\qset-feature-store')
    from qset_feature_store import FeatureSet
    import pandas as pd
    class FeatureSetUsingTimebars(FeatureSet):
        def calc(self):
            return self.get(self.inputs['timebars']) * 2

    from qset_feature_store.repository.client import QsetRepositoryClient
    cli = QsetRepositoryClient('akadaner', db='feature-store-test')

    # clean
    for key in ['featureset', 'dataset_schema', 'dataset']:
        for fs in cli.get_many(key):
            cli.delete(key, fs)

    # create timebars featureset
    fs = cli.create_featureset('timebars', 'external')
    fs = cli.push('featureset', fs)

    cfs = cli.create_dataset_schema('timebars_schema', fs, {'period': 600})
    cfs = cli.push('dataset_schema', cfs)

    df = pd.DataFrame([[1, 4], [2, 5], [3, 6]], columns=['a', 'b'])

    qdm.put(df, cfs, scope={'universe': 'binance'})

    print(qdm.get(cfs, scope={'universe': 'binance'}).head())
    print(qdm.calc(TrivialFeatureSet(), inputs={}, scope={'universe': 'binance'}, params={}))
    print(qdm.calc(FeatureSetUsingTimebars(), inputs={'timebars': cfs}, scope={'universe': 'binance'}, params={}))

    # create configured with pandas

    code = r'''
import sys
sys.path.append(r'C:\Users\Mi\Desktop\master\code\git\2020.09-qset\qset-feature-store')
from qset_feature_store import FeatureSet
import pandas as pd
class TrivialFeatureSet(FeatureSet):
    def calc(self):
        return pd.DataFrame([1, 2, 3], columns=['a'])
'''

    fs = cli.create_featureset('my_pandas_featureset', 'pandas/v1', {'code': code})
    fs = cli.push('featureset', fs)
    print(fs)

    # note: using get now - since it is a repository featureset
    print(qdm.get(fs, scope={'universe': 'binance'}, params={}))



if __name__ == '__main__':
    test_calc()