from builtins import object
import six
import pytest

from ckan.tests import factories

import ckanext.report.model as report_model


@pytest.fixture
def report_setup():
    report_model.init_tables()


@pytest.mark.ckan_config(u'ckan.plugins', u'report tagless_report')
@pytest.mark.usefixtures(u'clean_db', u'with_plugins', u'report_setup')
class TestReportPlugin(object):

    def test_report_routes(self, app):
        u"""Test report routes"""
        res = app.get(u'/report')
        body = six.ensure_text(res.body)

        assert u"Reports" in body

    def test_tagless_report_listed(self, app):
        u"""Test tagless report is listed on report page"""
        res = app.get(u'/report')
        body = six.ensure_text(res.body)

        assert u'Tagless datasets' in body
        assert u'href="/report/tagless-datasets"' in body

    def test_tagless_report(self, app):
        u"""Test tagless report generation"""
        dataset = factories.Dataset()

        res = app.get(u'/report/tagless-datasets')
        body = six.ensure_text(res.body)

        assert u"Datasets which have no tags." in body
        assert 'href="/dataset/' + dataset['name'] + '"' in body
