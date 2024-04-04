from utils import generate_token


def test_should_generate_token():
    generated_token = generate_token()

    assert generated_token
    assert "str" in str(type(generated_token))
