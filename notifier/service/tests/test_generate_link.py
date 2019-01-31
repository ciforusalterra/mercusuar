import unittest

from notifier.service.generate_link import generate_link


class TestGenerateLink(unittest.TestCase):

    def setUp(self):
        self.base_url: str = 'https://localhost/'
        self.customer_id: str = '1234'
        self.corporate_id: str = 'qwer'

    def test_generate_link_success(self):
        """
        Given generate_link right params, it should return full url.
        :return:
        """
        expected_url = 'https://localhost/1234/qwer/'
        full_url = generate_link(self.base_url, self.customer_id, self.corporate_id)
        self.assertEqual(expected_url, full_url)

    def test_generate_link_wrong_params(self):
        """
        Given generate_link wrong params, it should return False.
        :return:
        """
        full_url = generate_link(self.base_url, self.customer_id, 456)
        self.assertFalse(full_url)
