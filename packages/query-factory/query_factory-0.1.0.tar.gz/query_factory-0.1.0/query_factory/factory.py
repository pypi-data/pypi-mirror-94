"""Factories."""

import os
import re

import requests
import yaml
from jinjasql import JinjaSql

from . import exceptions


def _fetch_manifest(path_or_url):
    if re.match(r"^https?://", path_or_url):
        manifest = _fetch_from_url(path_or_url)
    else:
        manifest = _fetch_from_path(path_or_url)
    return manifest


def _fetch_from_url(url):
    response = requests.get(url)
    if response.status_code != 200:
        raise exceptions.FetchTemplateError(response.status_code)
    return response.text


def _fetch_from_path(path):
    with open(path) as _f:
        content = _f.read()
    return content


def validate_template(template):
    mandatory_keys = {
        "description",
        "variables",
    }
    for key in mandatory_keys:
        if key not in template:
            raise exceptions.MalformedTemplate(f"Missing '{key}' section.")

    if "query_template" not in template and "query_template_location" not in template:
        raise exceptions.MalformedTemplate(f"Missing either 'query_template' "
                                           f"or 'query_template_location' section.")


class SQLQueryFactory:
    """
    SQL query factory to variabilize some query with various parameters on the go.

    Args:
        template_path (path-like): Template location. param_style (str): Style to use depending on you SQL query engine.
            See https://github.com/hashedin/jinjasql#multiple-param-styles
    """

    def __init__(self, template_path, param_style="format"):
        self._template_path = template_path
        self._query = None
        self._variables = None
        self.required_variables = None
        self.optional_variables = None

        self._load_template(template_path)
        self._jinjasql = JinjaSql(param_style=param_style)

    def __call__(self, **kwargs):
        """Build query with kwargs as data."""
        return self.get_query_with(**kwargs)

    def get_query_with(self, **kwargs):
        """Build query with kwargs as data."""
        self._check_kwargs(**kwargs)
        defaults = {key: value["default"] for key, value in self.optional_variables.items()}
        query, params = self._jinjasql.prepare_query(self._query, data={**defaults, **kwargs})
        return query % tuple(params)

    def describe(self, varname):
        """
        Fetch description provided in template.

        Args:
            varname (str): Varible name available in template.

        Returns:
            str: Description string.
        """
        try:
            specs = self._variables[varname]
        except KeyError as key:
            raise exceptions.NoSpecsForVariable(key)
        return specs.get("description", f"No description for '{varname}'")

    def _load_template(self, path_or_url):
        string = _fetch_manifest(path_or_url)
        self._load_template_from_string(string)

    def _load_template_from_string(self, string):
        template = yaml.load(string, Loader=yaml.FullLoader)
        validate_template(template)
        self._query = self._fetch_query(template)
        self._variables = template["variables"]
        self.required_variables = {name: specs for name, specs in self._variables.items()
                                   if specs.get("required", False)}
        self.optional_variables = {name: specs for name, specs in self._variables.items()
                                   if not specs.get("required", False)}
        if not self._query:
            raise exceptions.NoOrEmptyQueryException(f"Invalid query: '{self._query}'")

    def _check_kwargs(self, **kwargs):
        """Check completeness and compatibility of kwargs for the current template."""
        if not set(self.required_variables).issubset(kwargs):
            missing = set(self.required_variables) - set(kwargs)
            raise exceptions.MissingOrExtraVariableException(
                f"Wrong varibales passed. Missing required: {missing}"
            )
        if not set(kwargs).issubset(set(self._variables)):
            extra = set(kwargs) - set(self._variables)
            raise exceptions.MissingOrExtraVariableException(
                f"Wrong varibales passed. Extras: {extra}"
            )

    def _fetch_query(self, template):
        if "query_template" in template:
            return template["query_template"]
        if "query_template_location" in template:
            return self._fetch_query_from_location(template["query_template_location"])

    def _fetch_query_from_location(self, location):
        if re.match(r"^https?://", location):
            return _fetch_from_url(location)
        else:
            path_to_query = os.path.abspath(
                os.path.join(
                    os.path.dirname(self._template_path),
                    location
                )
            )
            return _fetch_from_path(path_to_query)
