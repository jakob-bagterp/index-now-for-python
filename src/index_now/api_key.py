import random
import string
import uuid


def generate_api_key(length: int = 32) -> str:
    """Generate a random API key for IndexNow. Reference: [indexnow.org/documentation](https://www.indexnow.org/documentation)

    Args:
        length (int, optional): Length of the API key. Should be minimum 8 and maximum 128.

    Returns:
        str: An 8 to 128 character hexadecimal string, e.g. `5017988d51af458491d21ecab6ed1811` for a length of 32 characters.

    Example:
        How to generate a random API key:

        ```python linenums="1" hl_lines="3"
        from index_now import generate_api_key

        api_key = generate_api_key()

        print(api_key)
        ```

        This will print a random API key of 32 characters. Example:

        ```shell title=""
        5017988d51af458491d21ecab6ed1811
        ```

        How to generate a random API key with a custom length:

        ```python linenums="1" hl_lines="3-4"
        from index_now import generate_api_key

        api_key_16 = generate_api_key(length=16)
        api_key_64 = generate_api_key(length=64)

        print(api_key_16)
        print(api_key_64)
        ```

        This will print two random API keys of 16 and 64 characters. Example:

        ```shell title=""
        5017988d51af4584
        5017988d51af458491d21ecab6ed18115017988d51af458491d21ecab6ed1811
        ```
    """

    if not 8 <= length <= 128:
        raise ValueError("Length must be between 8 and 128.")

    if length <= 32:
        return str(uuid.uuid4()).replace("-", "")[:length]
    return "".join(random.choices(string.ascii_lowercase + string.ascii_uppercase + string.digits, k=length))
