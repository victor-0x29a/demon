from utils import generate_token, token_is_valid
from constants import SECRET


def test_should_generate_token():
    generated_token = generate_token()

    assert generated_token
    assert "str" in str(type(generated_token))


def test_should_validate_token():
    valid_token = generate_token()

    invalid_token = "foo.bar"

    assert token_is_valid(valid_token, SECRET)

    assert not token_is_valid(invalid_token, SECRET)
