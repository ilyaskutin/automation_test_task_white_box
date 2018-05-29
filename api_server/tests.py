# -*- coding: utf-8 -*-
import unittest
from time import sleep

import requests
import random
from threading import Thread


class Test(unittest.TestCase):
    """
        Для классификации тестов по техникам тест-дизайна
        решил для каждой техники создать свой класс.
        А это базовый класс
    """

    def setUp(self):
        self.scheme = "http://"
        self.host = "127.0.0.1"
        self.port = "8888"
        self.path = "/temperature_check"
        self.url = "".join([self.scheme, "{}:{}".format(self.host, self.port), self.path])
        self.is_ping()

    def positive_request(self, **kwargs):
        if 'status_code' in kwargs:
            status_code = kwargs['status_code']
        else:
            status_code = 200
        if 'elapsed' in kwargs:
            elapsed = kwargs['elapsed']
        else:
            elapsed = 1
        if 'msg' in kwargs:
            msg = kwargs['msg']
        else:
            msg = ''
        response = requests.get(self.url, params={"temperature": kwargs['temperature']})

        self.assertEqual(response.status_code, status_code, msg=msg)
        self.assertLess(response.elapsed.total_seconds(), elapsed, msg=msg)
        self.assertEqual(response.text, (kwargs['expected_water_state']), msg=msg)

    def is_ping(self):
        try:
            requests.get(self.url, params={"temperature": 20}).status_code
        except:
            self.assertEqual(0, 1, msg="Server not running")


class PositiveTests(Test):
    """
        Позитивные тесты
    """
    TEST_FLOAT = True
    # Данные для запросов без модификатора, например ?temperature=50
    WITHOUT_MOD = {
        'unknown': [-400.49, -399, -274, -273.51, 999998.501, 999999,
                    999999.49, 1000000, 2123212.21, 44322344],
        'ice': [-273.49, -273, -272.49, -272, -199.99, -50, -1, -0.51],
        'liquid': [-0.49, 0, 0.49, 1, 36.666, 88, 99, 99.49],
        'steam': [99.50, 100, 100.49, 101, 159.9, 350, 999998, 999998.49]
    }

    # Данные для запросов с модификатором C, например ?temperature=50C
    WITH_MOD_C = {
        'unknown': ['-666.66C', '-299C', '-274C', '-273.51C', '999998.5001C', '999999C', '999999.49C',
                    '1000000C', '1974212.21C', '73222144'],
        'ice': ['-273.49C', '-273C', '-272.49C', '-272C', '-143.287C', '-30C', '-1C', '-0.51C'],
        'liquid': ['-0.49C', '0C', '0.49C', '1C', '74.1C', '53C', '99C', '99.49C'],
        'steam': ['99.51C', '100C', '100.49C', '101C', '213.222C', '1050C', '999998C', '999998.49C']
    }
    # Данные для запросов с модификатором K, например ?temperature=50K
    WITH_MOD_K = {
        'unknown': ['-143.2K', '-23K', '-1K', '-0.51K', '1000270.51K', '1000271K', '1000271.49K',
                    '1000272K', '3000000.1K', '8888888K'],
        'ice': ['-0.49K', '0K', '0.49K', '1K', '187.1K', '270K', '273K', '273.49K'],
        'liquid': ['273.51K', '274K', '274.49K', '275K', '314.14K', '299K', '373K', '373.49K'],
        'steam': ['373.501K', '374K', '374.49K', '375K', '232500.2K', '469821K', '1000270K', '1000270.49K']
    }

    # Данные для запросов с модификатором F, например ?temperature=50F
    WITH_MOD_F = {
        'unknown': ['-999.999F', '-500F', '-460F', '-459.51F', '1800028.51F', '1800029F',
                    '1800029.49F', '1800030F', '3000000.1F', '8888888F'],
        'ice': ['-459.49F', '-459F', '-458.51F', '-458F', '-200.1F', '-27F', '-0.49F',
                '0F', '0.49F', '32F', '32.49F'],
        'liquid': ['32.51F', '33F', '33.49F', '34F', '78.66F', '189F', '211F', '211.49F'],
        'steam': ['211.501F', '212F', '212.49F', '213F', '1232500.2F', '1600000F', '1800028F',
                  '1800028.49F']
    }

    def test_without_mod(self):
        for exp_res, requests_data in self.WITHOUT_MOD.items():
            for req in requests_data:
                if not self.TEST_FLOAT and '.' in str(req):
                    continue
                with self.subTest():
                    self.positive_request(temperature=req,
                                          expected_water_state=exp_res,
                                          status_code=200,
                                          msg="Передаваемое значение {} -- "
                                              "Ожидаемый статус {} -- "
                                              "Ожидаемый результат {}".format(req, 200, exp_res))

    def test_with_mod_c(self):
        for exp_res, requests_data in self.WITH_MOD_C.items():
            for req in requests_data:
                if not self.TEST_FLOAT and '.' in str(req):
                    continue
                with self.subTest():
                    self.positive_request(temperature=req,
                                          expected_water_state=exp_res,
                                          status_code=200,
                                          msg="Передаваемое значение {} -- "
                                              "Ожидаемый статус {} -- "
                                              "Ожидаемый результат {}".format(req, 200, exp_res)
                                          )

    def test_with_mod_k(self):
        for exp_res, requests_data in self.WITH_MOD_K.items():
            for req in requests_data:
                if not self.TEST_FLOAT and '.' in str(req):
                    continue
                with self.subTest():
                    self.positive_request(temperature=req,
                                          expected_water_state=exp_res,
                                          status_code=200,
                                          msg="Передаваемое значение {} -- "
                                              "Ожидаемый статус {} -- "
                                              "Ожидаемый результат {}".format(req, 200, exp_res)
                                          )

    def test_with_mod_f(self):
        for exp_res, requests_data in self.WITH_MOD_F.items():
            for req in requests_data:
                if not self.TEST_FLOAT and '.' in str(req):
                    continue
                with self.subTest():
                    self.positive_request(temperature=req,
                                          expected_water_state=exp_res,
                                          status_code=200,
                                          msg="Передаваемое значение {} -- "
                                              "Ожидаемый статус {} -- "
                                              "Ожидаемый результат {}".format(req, 200, exp_res)
                                          )


class NegativeTests(Test):
    """
        Блок эквивалентных негативных тестов
    """

    def __exp_on_br(self, value):
        return '{}"error": "Invalid temperature {}"{}'.format("{", value, "}")

    EMPTY = {"": ['', ' ', ' ' * 50]}
    STRING = {
        'a': ['a'], 'D': ['D'], 'abc' * 50: ['abc' * 50], 'ABC' * 50: ['ABC' * 50],
        'QWEjkl' * 50: ['QWEjkl' * 50],
        'QWEjkl' * 500: ['QWEjkl' * 500],
        # "\u041f\u0420\u0418\u0412\u0415\u0422": ["ПРИВЕТ"], # Не могу протестить юникод, возвращаемое всегда отличается
        '12345A': ['12345A'],
        '123a45A': ['123a45A'],
        'A12345': ['A12345'],
        '12345s': ['12345s'],
        '12345aAAAAa': ['12345aAAAAa']
    }

    STRING_AS_DIGIT = {2321 ** 2233: [2321 ** 2233], 2321 ** 23 + 0.1111222: [2321 ** 23 + 0.1111222],
                       '09': ['09'], '-01': ['-01'], '+01110': [repr('+01110')], '1,5': ['1,5']}

    SPEC_CHAR = {'!@#$%^&*()=+': ['!@#$%^&*()=+'], '!@$%^&*()#': ['!@$%^&*()#', '!@$%^&*()#']}

    def test_empty_values(self):
        for exp_res, requests_data in self.EMPTY.items():
            for req in requests_data:
                with self.subTest():
                    self.positive_request(
                        temperature=req,
                        expected_water_state=self.__exp_on_br(exp_res),
                        status_code=400,
                        msg="Передаваемое значение {} -- "
                            "Ожидаемый статус {} -- "
                            "Ожидаемый результат {}".format(req, 400, self.__exp_on_br(exp_res))
                    )

    def test_string_values(self):
        for exp_res, requests_data in self.STRING.items():
            for req in requests_data:
                with self.subTest():
                    self.positive_request(
                        temperature=req,
                        expected_water_state=self.__exp_on_br(exp_res),
                        status_code=400,
                        msg="Передаваемое значение {} -- "
                            "Ожидаемый статус {} -- "
                            "Ожидаемый результат {}".format(req, 400, self.__exp_on_br(exp_res))
                    )

    def test_digit(self):
        for exp_res, requests_data in self.STRING_AS_DIGIT.items():
            for req in requests_data:
                with self.subTest():
                    self.positive_request(
                        temperature=req,
                        expected_water_state=self.__exp_on_br(exp_res),
                        status_code=400,
                        msg="Передаваемое значение {} -- "
                            "Ожидаемый статус {} -- "
                            "Ожидаемый результат {}".format(req, 400, self.__exp_on_br(exp_res))
                    )

    def test_special_characters(self):
        for exp_res, requests_data in self.SPEC_CHAR.items():
            for req in requests_data:
                with self.subTest():
                    self.positive_request(
                        temperature=req,
                        expected_water_state=self.__exp_on_br(exp_res),
                        status_code=400,
                        msg="Передаваемое значение {} -- "
                            "Ожидаемый статус {} -- "
                            "Ожидаемый результат {}".format(req, 400, self.__exp_on_br(exp_res))
                    )


class TestStress(Test):
    """
        Сделаем нагрузочный тест, что бы убедится что сервис
        будет продолжать работать под нагрузкой
    """

    def multiple_positive_call(self, **kwargs):
        for _ in range(kwargs["counts"]):
            self.positive_request(temperature=kwargs["temperature"],
                                  expected_water_state=kwargs["expected_water_state"],
                                  status_code=kwargs["status_code"])

    def test_multiple_call(self):
        clients = []
        data = [{"temperature": 50, "expected_water_state": 'liquid', "counts": 50, 'status_code': 200},
                {"temperature": "50K", "expected_water_state": 'ice', "counts": 75, 'status_code': 200},
                {"temperature": "-999.51F", "expected_water_state": 'unknown', "counts": 43, 'status_code': 200},
                {"temperature": "999998.49C", "expected_water_state": 'steam', "counts": 66, 'status_code': 200},
                {"temperature": 1000000, "expected_water_state": 'unknown', "counts": 15, 'status_code': 200},
                {"temperature": "asdsadwawdasd",
                 "expected_water_state": '{}"error": "Invalid temperature {}"{}'.format("{", "asdsadwawdasd", "}"),
                 "counts": 50, 'status_code': 400}]

        for i in range(len(data)):
            clients.append(Thread(target=self.multiple_positive_call,
                                  kwargs=data[i]))
        for c in clients:
            c.start()
        for c in clients:
            c.join()

    def test_stress_500(self):
        self.multiple_positive_call(temperature=-200,
                                    expected_water_state='ice',
                                    counts=500,
                                    status_code=200)

if __name__ == '__main__':
    unittest.main()
