#!/usr/bin/env python3
import unittest
from mock import patch
import pytest

from ckanext.datagovuk.plugin import DatagovukPlugin
from ckan.plugins.toolkit import ValidationError


class TestS3ResourcesPlugin:
    plugin = DatagovukPlugin()

    def test_s3_config_exception(self):
        with pytest.raises(KeyError) as context:
            self.plugin.before_create_or_update({}, {"upload": "dummy value"})
        assert str(context.value) == "'Required S3 config options missing'"

    @patch("ckanext.datagovuk.plugin.upload.config_exists")
    def test_upload_early_abort(self, mock_check_config):
        resource = {
            "package_id": u"some-pointless-data-1",
            "url": "organogram-senior.csv",
            "timestamp": "2020-01-09T12-11-41Z",
            "name": "2020-01-09 Organogram (Senior)",
        }

        self.plugin.before_create_or_update({}, resource)
        assert not mock_check_config.called

    @patch("ckanext.datagovuk.plugin.upload.config_exists")
    def test_format_api_early_abort(self, mock_check_config):
        resource = {
            "package_id": u"some-pointless-data-1",
            "url": "organogram-senior.csv",
            "timestamp": "2020-01-09T12-11-41Z",
            "name": "2020-01-09 Organogram (Senior)",
            "format": "API",
            "upload": "test.csv"
        }

        self.plugin.before_create_or_update({}, resource)
        assert not mock_check_config.called

