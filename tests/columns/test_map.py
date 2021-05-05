from tests.testcase import BaseTestCase


class DecimalTestCase(BaseTestCase):
    # TODO: detect
    required_server_version = (18, 12, 13)
    stable_support_version = (22, 14, 9)

    def client_kwargs(self, version):
        if version < self.stable_support_version:
            return {'settings': {'allow_experimental_map_type': True}}

    def cli_client_kwargs(self):
        if self.stable_support_version > self.server_version:
            return {'allow_experimental_map_type': 1}

    def test_simple(self):
        with self.create_table('a Map(String, UInt64)'):
            data = [
                ({},),
                ({'key1': 1}, ),
                ({'key1': 2, 'key2': 20}, ),
                ({'key1': 3, 'key2': 30, 'key3': 50}, )
            ]
            self.client.execute('INSERT INTO test (a) VALUES', data)
            query = 'SELECT * FROM test'
            inserted = self.emit_cli(query)
            self.assertEqual(
                inserted,
                "{}\n"
                "{'key1':1}\n"
                "{'key1':2,'key2':20}\n"
                "{'key1':3,'key2':30,'key3':50}\n"
            )
            inserted = self.client.execute(query)
            self.assertEqual(inserted, data)

    def test_nullable(self):
        with self.create_table('a Map(Nullable(String), Nullable(UInt64))'):
            data = [
                ({None: None},),
                ({'key1': 1}, )
            ]
            self.client.execute('INSERT INTO test (a) VALUES', data)
            query = 'SELECT * FROM test'
            inserted = self.emit_cli(query)
            self.assertEqual(
                inserted,
                "{}\n"
                "{'key1':1}\n"
                "{'key1':2,'key2':20}\n"
                "{'key1':3,'key2':30,'key3':50}\n"
            )
            inserted = self.client.execute(query)
            self.assertEqual(inserted, data)
