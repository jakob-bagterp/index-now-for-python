import random
import string
import uuid


def generate_api_key(length: int = 32) -> str:
    """Generate a random API key for IndexNow. Reference: [indexnow.org/documentation](https://www.indexnow.org/documentation)

    Args:
        length (int, optional): Length of the API key. Should be minimum 8 and maximum 128.

    Returns:
        str: An 8 to 128 character hexadecimal string, e.g. `5017988d51af458491d21ecab6ed1811` for a length of 32 characters.
    """

    if not 8 <= length <= 128:
        raise ValueError("Length must be between 8 and 128.")

    if length <= 32:
        return str(uuid.uuid4()).replace("-", "")[:length]
    return "".join(random.choices(string.ascii_lowercase + string.digits, k=length))
