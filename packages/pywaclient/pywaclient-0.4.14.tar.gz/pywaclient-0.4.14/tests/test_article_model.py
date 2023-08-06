#    Copyright 2020 Jonas Waeber
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.
import logging
import os
import sys
import unittest
from collections import Iterable
from typing import Dict

from models.user import User
from pywaclient.models.article import Article
from pywaclient.api import AragornApiClient


class TestArticleModel(unittest.TestCase):

    def setUp(self):
        self.client = AragornApiClient(
            name='TEST APPLICATION',
            url='https://gitlab.com/SoulLink/world-anvil-api-client',
            application_key=os.environ.get('WA_APPLICATION_KEY'),
            authentication_token=os.environ.get('WA_AUTH_TOKEN'),
            version='0.1.0'
        )
        self.maxDiff = None
        self.user = User(self.client)

    def testHasParentArticle(self):
        article = Article(self.client, self.client.article.get('7c6b1e91-210f-4519-929e-bb6c79c92899'))
        self.assertTrue(article.has_parent_article)

    def testGetParentArticle(self):
        article = Article(self.client, self.client.article.get('7c6b1e91-210f-4519-929e-bb6c79c92899'))
        parent = article.get_parent_article()
        self.assertEqual(parent.title, 'Test Parent Article')


if __name__ == '__main__':
    unittest.main()
