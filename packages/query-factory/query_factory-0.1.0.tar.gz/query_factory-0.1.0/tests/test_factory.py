import os
from unittest.mock import patch, call

import pytest

from query_factory import SQLQueryFactory
from query_factory import exceptions


@pytest.fixture()
def template_path():
    return os.path.join(os.path.dirname(__file__), "data", "sql_template_with_defaults.yaml")


def test_init(template_path):
    _ = SQLQueryFactory(template_path)


@patch("jinjasql.JinjaSql.prepare_query", return_value=("%s, %s", [1, 2]))
def test_get_query_with(prepare_query_mock, template_path):
    factory = SQLQueryFactory(template_path)
    factory.get_query_with(start_date="1", end_date="2", category_id="cat", market="pro")
    factory._jinjasql.prepare_query.assert_called_once_with(
        factory._query, data={
            "start_date": "1",
            "end_date": "2",
            "category_id": "cat",
            "market": "pro"
        }
    )


@patch("jinjasql.JinjaSql.prepare_query", return_value=("%s, %s", [1, 2]))
def test_get_query_with_defaults(prepare_query_mock, template_path):
    factory = SQLQueryFactory(template_path)
    factory.get_query_with(start_date="1", end_date="2")
    factory._jinjasql.prepare_query.assert_called_once_with(
        factory._query, data={
            "start_date": "1",
            "end_date": "2",
            "category_id": None,
            "market": "part"
        }
    )


def test_get_query_with_raises_extra(template_path):
    factory = SQLQueryFactory(template_path)
    with pytest.raises(exceptions.MissingOrExtraVariableException):
        factory.get_query_with(wrong_arg="1")


def test_get_query_with_raises_missing(template_path):
    factory = SQLQueryFactory(template_path)
    with pytest.raises(exceptions.MissingOrExtraVariableException):
        factory.get_query_with()


@patch("yaml.load", return_value={"wrong_key": "value"})
def test_malformed_raise(load_mock, template_path):
    with pytest.raises(exceptions.MalformedTemplate):
        _ = SQLQueryFactory(template_path)


def test_factory_describe(template_path):
    factory = SQLQueryFactory(template_path)
    description = factory.describe("start_date")
    assert description == "UTC datetime string to gather data from (inclusive)"


@patch("yaml.load", return_value={
    "description": "",
    "variables": {},
    "query_template_location": "./relative/path.sql"
})
@patch("query_factory.factory._fetch_from_path")
def test_factory_with_external_sql_local(fetch_from_path_mock, yaml_load_mock, template_path):
    factory = SQLQueryFactory(template_path)
    expected_calls = [
        call(template_path),
        call(
            os.path.abspath(os.path.join(os.path.dirname(__file__), "data", "relative", "path.sql"))
        )
    ]
    assert expected_calls == fetch_from_path_mock.call_args_list


@patch("yaml.load", return_value={
    "description": "",
    "variables": {},
    "query_template_location": "https://fake/url.sql"
})
@patch("query_factory.factory._fetch_from_url")
def test_factory_with_external_sql_url(fetch_from_url_mock, yaml_load_mock, template_path):
    factory = SQLQueryFactory(template_path)
    fetch_from_url_mock.assert_called_once_with("https://fake/url.sql")
