import pandas as pd
from qset_feature_store.repository import models
from qset_feature_store.reflexion import get_featureset_code_from_current_notebook
from utils_ak.naming import to_lower_name
from utils_ak.builtin import delistify
from mongoengine import connect

from utils_ak.mongoengine import cast_model, cast_dict


class QsetRepositoryClient:
    def __init__(self, account, db='feature-store', host='localhost'):
        self.account = account
        connect(db, host=host)

    def _cast_mongoengine_query(self, query):
        query = query or {}
        if '_id' in query:
            query['pk'] = query.pop('_id')
        return query

    def get(self, type, **query):
        res = self.get_many(type, **query)
        return delistify(res)

    def get_many(self, type, **query):
        cls = models.cast_model_class(type)
        return [cast_dict(model, cls) for model in cls.objects(**self._cast_mongoengine_query(query))]

    def get_catalog(self, type, **query):
        return pd.DataFrame(self.get_many(type, **query))

    def get_latest(self, type, **query):
        cls = models.cast_model_class(type)

        latest = cls.objects(**self._cast_mongoengine_query(query)).last()

        if not latest:
            return

        return cast_dict(latest, cls)

    def delete(self, type, object):
        cls = models.cast_model_class(type)
        return cls.objects(pk=object['_id']).delete()

    def create_from(self, type, object):
        cls = models.cast_model_class(type)
        return cast_dict(cast_model(object, cls).clone(), cls)

    def publish(self, type, object):
        cls = models.cast_model_class(type)

        if '_id' in object:
            raise Exception('Feature Set already exists')
        res = cast_model(object, cls).save()
        return cast_dict(res, cls)

    def update(self, type, object):
        if '_id' not in object:
            raise Exception('Feature Set not published yet')
        new_object = self.create_from(type, object)
        return self.publish(type, new_object)

    def is_published(self, object):
        return '_id' in object

    def push(self, type, object):
        if not self.is_published(object):
            return self.publish(type, object)
        else:
            return self.update(type, object)

    def create_featureset(self, name, engine, config=None, inputs=None, **kwargs):
        config = config or {}
        inputs = inputs or {}
        return cast_dict(models.FeatureSet(account=self.account, name=name, engine=engine, config=config, inputs=inputs, **kwargs), models.FeatureSet)

    def create_pandas_featureset(self, featureset_cls, inputs=None, name=None, **kwargs):
        name = name or to_lower_name(featureset_cls.__name__)
        return self.create_featureset(name=name,
                                      engine='pandas/v1',
                                      inputs=inputs,
                                      config={'code': get_featureset_code_from_current_notebook(featureset_cls)}, **kwargs)

    def create_dataset_schema(self, name, featureset, params, **kwargs):
        featureset = cast_model(featureset, models.FeatureSet)

        return cast_dict(models.DatasetSchema(account=self.account,
                                              name=name,
                                              featureset=featureset,
                                              params=params,
                                              **kwargs), models.DatasetSchema)

    def create_dataset(self, name, scope, dataset_schema, materialization, **kwargs):
        dataset_schema = cast_model(dataset_schema, models.DatasetSchema)
        return cast_dict(models.DataSet(account=self.account,
                                        name=name,
                                        scope=scope,
                                        dataset_schema=dataset_schema,
                                        materialization=materialization, **kwargs), models.DataSet)


def test_qset_repository_client():
    cli = QsetRepositoryClient('akadaner', db='feature-store-test')

    # clean
    for key in ['featureset', 'dataset_schema', 'dataset']:
        for fs in cli.get_many(key):
            cli.delete(key, fs)

    fs = cli.create_featureset('my_featureset1', engine='pandas/v1', config={'code': 'print("Hello World")'})
    fs = cli.push('featureset', fs)
    print(fs)
    print(cli.get_catalog('featureset', account='akadaner'))
    print(cli.get_catalog('dataset_schema', account='akadaner'))
    print(cli.get_catalog('dataset', account='akadaner'))
    print(cast_model(fs, models.FeatureSet))

    cfs = cli.create_dataset_schema('my_dataset_schema_1', fs, {'param': 'foo'})
    cfs = cli.push('dataset_schema', cfs)
    print(cfs)

    ds = cli.create_dataset('my_dataset1', {'universe': 'my_universe'}, cfs, {'materialization_param': 'bar'})
    ds = cli.push('dataset', ds)
    print(ds)

    # create featureset with inputs
    fs = cli.create_featureset('my_featureset2', engine='pandas/v1', config={'code': 'print(self.inputs["my_input"])'}, inputs={'my_input': {'_id': str(cfs['_id'])}})
    fs = cli.push('featureset', fs)
    print(fs)

    for key in ['featureset', 'dataset_schema', 'dataset']:
        print(cli.get_catalog(key))
        print(cli.get_latest(key, account='akadaner'))


if __name__ == '__main__':
    test_qset_repository_client()