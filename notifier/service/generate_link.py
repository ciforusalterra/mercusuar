from typing import Union


def generate_link(base_url: str, customer_id: str, corporate_id) -> Union[str, bool]:
    """
    Given base_url, customer_id, and corporate_id, return full url
    :param base_url: str
    :param customer_id: str
    :param corporate_id: str
    :return: url: str
    """
    if not isinstance(base_url, str) or not isinstance(customer_id, str) or not isinstance(corporate_id, str):
        return False
    return '{}{}/{}/'.format(base_url, customer_id, corporate_id)
