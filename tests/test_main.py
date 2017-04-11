# -*- coding: utf-8 -*-
import re
import os
import unittest

import responses
from click.testing import CliRunner

from jobs_detector import settings
from jobs_detector.main import jobs_detector


class HackerNewsTestCase(unittest.TestCase):

    def setUp(self):
        self.post_id = '11814828'
        fixture_path = os.path.join(settings.BASE_DIR, 'tests',
                                    'fixtures', '{}.html'.format(self.post_id))
        with open(fixture_path) as f:
            content = f.read()
        responses.add(responses.GET,
                      re.compile(re.escape(settings.BASE_URL.format(self.post_id))),
                      body=content, status=200,
                      content_type='text/html')

    @responses.activate
    def test_hacker_news_default_keywords(self):
        runner = CliRunner()
        result = runner.invoke(
            jobs_detector,
            ['hacker_news', '-i', self.post_id]
        )
        expected = [
                    'Total job posts: 781',
                    'keywords:',
                    'Remote: 174 (22%)',
                    'Postgres: 85 (10%)',
                    'Python: 160 (20%)',
                    'Javascript: 781 (100%)',
                    'React: 143 (18%)',
                    'Pandas: 6 (0%)'
                    ]
        #self.assertEqual(result, expected)
        for msg in expected:
            self.assertTrue(msg in result.output)

    @responses.activate
    def test_hacker_news_custom_keywords(self):
        runner = CliRunner()
        result = runner.invoke(
            jobs_detector,
            ['hacker_news',
             '-i', self.post_id,
             '-k', 'python,django']
        )
        expected = [
                    'Total job posts: 781',
                    'keywords:',
                    'python: 160 (20%)',
                    'django: 39 (4%)'
                    ]
        for msg in expected:
            self.assertTrue(msg in result.output)

    @responses.activate
    def test_hacker_news_combinations(self):#####
        runner = CliRunner()
        result = runner.invoke(
            jobs_detector,
            ['hacker_news',
             '-i', self.post_id,
             '-c', 'python-remote,python-django,django-remote']
        )
        expected = [
                    'Total job posts: 781',
                    'keywords:',
                    'Remote: 174 (22%)',
                    'Postgres: 85 (10%)',
                    'Python: 160 (20%)',
                    'Javascript: 781 (100%)',
                    'React: 143 (18%)',
                    'Pandas: 6 (0%)',
                    'Combinations:',
                    'python-remote: 30 (3%)',
                    'django-remote: 8 (1%)',
                    'python-django: 38 (4%)'
                    ]
        for msg in expected:
            self.assertTrue(msg in result.output)

    @responses.activate
    def test_hacker_news_keywords_and_combinations(self):
        runner = CliRunner()
        result = runner.invoke(
            jobs_detector,
            ['hacker_news',
             '-i', self.post_id,
             '-k', 'python,django',
             '-c', 'python-remote,python-django,django-remote']
        )
        expected = [
                    'Total job posts: 781',
                    'keywords:',
                    'python: 160 (20%)',
                    'django: 39 (4%)',
                    'Combinations:',
                    'python-remote: 30 (3%)',
                    'django-remote: 8 (1%)',
                    'python-django: 38 (4%)'
                    ]
        for msg in expected:
            self.assertTrue(msg in result.output)
