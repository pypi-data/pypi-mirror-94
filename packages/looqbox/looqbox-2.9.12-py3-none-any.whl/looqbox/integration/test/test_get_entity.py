import unittest
from looqbox.integration.integration_links import get_entity


class TestGetEntity(unittest.TestCase):

    def test_get_entity_new_json_one_entity(self):
        """
        Test get_entity function with one entity
        """
        par = {
            "question": {
                "residualWords": [
                    "meta",
                    "python"
                ],
                "original": "meta python $debug",
                "clean": "meta python",
                "residual": "meta python"
            },
            "user": {
                "id": 1101,
                "login": "matheus",
                "groupId": 1,
                "language": "pt-br"
            },
            "entities": {
                "$date": {
                    "content": [
                        {
                            "segment": "hoje",
                            "text": "hoje",
                            "value": [
                                [
                                    "2020-01-22",
                                    "2020-01-22"
                                ]
                            ]
                        }
                    ]
                }
            },
            "partitions": {

            },
            "companyId": 0,
            "apiVersion": 2,
            "keywords": [
                "meta",
                "python"
            ]
        }

        date_value = get_entity("entities", par, "$date")
        date_json = get_entity("entities", par, "$date", only_value=False)
        self.assertEqual([['2020-01-22', '2020-01-22']], date_value)
        self.assertEqual([
            {"segment": "hoje", "text": "hoje", "value": [['2020-01-22', '2020-01-22']]}
        ], date_json)

        store_value = get_entity("entities", par, "$store")
        store_json = get_entity("entities", par, "$store", only_value=False)
        self.assertEqual(None, store_value)
        self.assertEqual(None, store_json)

        default_value = get_entity("entities", par, "$undefined")
        self.assertIsNone(default_value)

    def test_get_entity_new_json(self):
        """
        Test get_entity function with multiple entities
        """
        par = {
            "question": {
                "residualWords": [
                    "venda"
                ],
                "original": "venda da loja São Paulo por dia essa semana $debug",
                "clean": "venda da loja sao paulo por dia essa semana",
                "residual": "venda "
            },
            "user": {
                "id": 41,
                "login": "gustavo",
                "groupId": 1,
                "language": "pt-br"
            },
            "entities": {
                "$store": {
                    "content": [
                        {
                            "segment": "da loja sao paulo",
                            "value": [
                                1
                            ]
                        }
                    ]
                },
                "$date": {
                    "content": [
                        {
                            "segment": "essa semana",
                            "text": "essa semana",
                            "value": [
                                [
                                    "2021-01-11",
                                    "2021-01-17"
                                ]
                            ]
                        }
                    ]
                },
                "$datepartition": {
                    "content": [
                        {
                            "segment": "por dia",
                            "text": "por dia",
                            "value": [
                                "byDay"
                            ]
                        }
                    ]
                }
            },
            "partitions": {
                "$date": {
                    "content": [
                        {
                            "segment": "por dia",
                            "text": "por dia",
                            "value": [
                                "byDay"
                            ]
                        }
                    ]
                }
            },
            "companyId": 140,
            "apiVersion": 2,
            "keywords": [
                "venda",
                "?$datetime",
                "_date",
                "_datetime",
                "_store",
                "_plu",
                "_section",
                "_dep",
                "pivot",
                "pivotado",
                "pivotada",
                "grafico"
            ],
            "$query": "false",
            "deviceType": "desktop"
        }

        date_value = get_entity("entities", par, "$date")
        self.assertEqual([['2021-01-11', '2021-01-17']], date_value)

        date_json = get_entity("entities", par, "$date", only_value=False)
        self.assertEqual([{"segment": "essa semana", "text": "essa semana", "value": [['2021-01-11', '2021-01-17']]}], date_json)

        date_value_mix_entities = get_entity("entities", par, ["$date", "$store"])
        self.assertEqual([['2021-01-11', '2021-01-17'], 1],
                         date_value_mix_entities)

        date_value_mix_entities_json = get_entity("entities", par, ["$date", "$store"], only_value=False)
        self.assertEqual([{"segment": "essa semana", "text": "essa semana", "value": [['2021-01-11', '2021-01-17']]},
                          {"segment": "da loja sao paulo", "value": [1]}], date_value_mix_entities_json)

    def test_get_entity_old_json(self):
        """
        Test get_entity function
        """

        par = {
            "originalQuestion": "teste",
            "cleanQuestion": "teste",
            "residualQuestion": "",
            "residualWords": [""],
            "entityDictionary": None,
            "userlogin": "user",
            "userId": 666,
            "companyId": 0,
            "userGroupId": 0,
            "language": "pt-br",
            "$date": [
                [
                    "2019-01-08",
                    "2019-01-08"
                ]
            ],
            "$datetime": [
                [
                    "2019-01-08 00:00:00",
                    "2019-01-08 00:00:00"
                ]
            ],
            "$store": [1, 2, 3, 4, 5, 6, 7, 8],
            "apiVersion": 1
        }

        date_value = get_entity("entities", par, "$date")
        self.assertEqual([['2019-01-08', '2019-01-08']], date_value)

        store_value = get_entity("entities", par, "$store")
        self.assertEqual([1, 2, 3, 4, 5, 6, 7, 8], store_value)

        default_value = get_entity("entities", par, "$undefined")
        self.assertIsNone(default_value)

        mix_value = get_entity("entities", par, ["$date", "$datetime"])
        self.assertEqual([['2019-01-08', '2019-01-08'], ['2019-01-08 00:00:00', '2019-01-08 00:00:00']], mix_value)

        date_value_only = get_entity("entities", par, "$date", only_value=False)
        self.assertEqual([['2019-01-08', '2019-01-08']], date_value_only)
