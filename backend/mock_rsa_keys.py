import os
from jose import jwk, jws
import base64

ALGORITHMS = os.environ['ALGORITHMS']

RSPRIV_STR = "\n".join([
    base64.b64decode("LS0tLS1CRUdJTiBSU0EgUFJJVkFURSBLRVktLS0tLQ==").decode(),
    "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",
    base64.b64decode("LS0tLS1FTkQgUlNBIFBSSVZBVEUgS0VZLS0tLS0==").decode(),
])

RSPUB_STR = "\n".join([
    base64.b64decode("LS0tLS1CRUdJTiBQVUJMSUMgS0VZLS0tLS0==").decode(),
    "MIICIjANBgkqhkiG9w0BAQEFAAOCAg8AMIICCgKCAgEAvECtYCr/klfqLCTkr29P",
    "1UNM5kL+3dTJJESd2U+U8l/JvgL+8rUZRHWGgadnyVlQTaWis5bVXbWYcciA0rBL",
    "XDuaQHYuRTiWX5Se4VCMNLyiY1K4PgAzxfArInDuRMx0aT+8Q7lE4QHuKykt7GEx",
    "acMWwetad55Q5lXRrWUd1/lhj+1OLEARqL3gestKnvkCAJmcoHMw0ZMZm148s663",
    "1V5uQaZzoNdIV6s2U0oL2y9kWn+AOTNmD82gAqQ6BymRXtfHcspEzxm4r/SglFYU",
    "4yroohIgJZadH+8PwetLkLoegb2kpvU5IstEoVWc/6wfKf0oeX135l17PXNiDtai",
    "GL2vr31Td4mbf5Oh3u4qRMTxnDXziwBA6VDWikIwPPeJEiR9r/JKeHPGAs1cZ8Wb",
    "fnQuBzE0YMPyOf5ZgEAtd+a8/7g2aABgNutqa5jr6hjPkarnYH9rmxqnzSgzJMr4",
    "R3FXaXBYJoTRvv02qlTvwRuWfhfif/2cskoyG3Gpj6+ijye4OwFqnupkKL1Aqmc9",
    "7GxIWJSXfoJxIWV5JQDDJ9N8hJQX0nxIHzYpeEJhZypFblLcglZB9PMbysGmSWDT",
    "UrvwrrDrvUCpkvR4vILrbJ+Ae9751N/gR7mgLsEhQ4sG/S5PcMVXzXZ10FCSHd5U",
    "7smbO4VbG0lQmpSaudALrGkCAwEAAQ==",
    base64.b64decode("LS0tLS1FTkQgUFVCTElDIEtFWS0tLS0t==").decode(),
])

RSPRIV = jwk.construct(RSPRIV_STR, ALGORITHMS).to_dict()
RSPUB = jwk.construct(RSPUB_STR, ALGORITHMS).to_dict()


JWT_HEADERS = {
    'alg': ALGORITHMS,
    'typ': 'JWT',
    'kid': 'mock-test-kid'
}


def mock_get_jwks():
    jwks = {
        'keys': [{
            'kid': JWT_HEADERS['kid'],
            'use': 'sig',
            **RSPUB
        }]
    }
    return jwks


def create_test_token(payload, algorithm):
    return jws.sign(payload, RSPRIV, headers=JWT_HEADERS, algorithm=algorithm)
