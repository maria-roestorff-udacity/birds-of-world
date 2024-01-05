import os
from jose import jwk, jws

ALGORITHMS = os.environ['ALGORITHMS']

RSA_PRIVATE_KEY_STR = ""

RSA_PUBLIC_KEY_STR = ""

RSA_PRIVATE_KEY = jwk.construct(RSA_PRIVATE_KEY_STR, ALGORITHMS).to_dict()
RSA_PUBLIC_KEY = jwk.construct(RSA_PUBLIC_KEY_STR, ALGORITHMS).to_dict()


JWT_HEADERS = {
    "alg": ALGORITHMS,
    "typ": "JWT",
    "kid": "mock-test-kid"
}


def mock_get_jwks():
    jwks = {
        'keys': [{
            'kid': JWT_HEADERS['kid'],
            'use': 'sig',
            **RSA_PUBLIC_KEY
        }]
    }
    return jwks


def create_test_token(payload, algorithm):
    return jws.sign(payload, RSA_PRIVATE_KEY, headers=JWT_HEADERS, algorithm=algorithm)
