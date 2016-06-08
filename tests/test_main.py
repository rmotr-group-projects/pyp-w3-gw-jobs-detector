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
            'Total job posts: 761',

            'Keywords:',
            'Remote: 171 (22%)',
            'Postgres: 84 (11%)',
            'Python: 155 (20%)',
            'Javascript: 124 (16%)',
            'React: 141 (19%)',
            'Pandas: 6 (1%)',
        ]
        self.assertIsNone(result.exception, result.exception)
        
        for msg in expected:
            self.assertTrue(msg in result.output, result.output)

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
            'Total job posts: 761',

            'Keywords:',
            'Python: 155 (20%)',
            'Django: 39 (5%)',
        ]

        for msg in expected:
            self.assertTrue(msg in result.output, result.output)

    @responses.activate
    def test_hacker_news_combinations(self):
        runner = CliRunner()
        result = runner.invoke(
            jobs_detector,
            ['hacker_news',
             '-i', self.post_id,
             '-c', 'python-remote,python-django,django-remote']
        )
        expected = [
            'Total job posts: 761',

            'Keywords:',
            'Remote: 171 (22%)',
            'Postgres: 84 (11%)',
            'Python: 155 (20%)',
            'Javascript: 124 (16%)',
            'React: 141 (19%)',
            'Pandas: 6 (1%)',

            'Combinations:',
            'Python-remote: 29 (4%)',
            'Django-remote: 8 (1%)',
            'Python-django: 38 (5%)',
        ]
    
        for msg in expected:
            self.assertTrue(msg in result.output, result.output)

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
            'Total job posts: 761',

            'Keywords:',
            'Python: 155 (20%)',
            'Django: 39 (5%)',

            'Combinations:',
            'Python-remote: 29 (4%)',
            'Django-remote: 8 (1%)',
            'Python-django: 38 (5%)',
        ]
        for msg in expected:
            self.assertTrue(msg in result.output, result.output)
