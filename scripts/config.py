RAPIDAPI_KEY = '187d7b0d2fmshb642a21912d2dbbp130898jsn0533211e9491'
RAPIDAPI_HOST = 'real-time-amazon-data.p.rapidapi.com'

'''
my_snowflake_public_key = b"""-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAySQ0PNDSB8dTR6Rb8fW7
13hGT6LlZwaiXpY3IoXCwGkS9N/YFV4cNerQ3DxudKFtz1J+ZDZ625pN14yUXKZE
ZU+NsCBKslRnDhMU5sBDBN4VAwG4gAFY0sM8V9LAS8IOhIxBjqcb903dIu4UNc+I
Vrz7F2dt78tYOb4JKTgq+UeNQZWrTr3OrrrtP4cQYI3oiQwSwe9iNYoswh6xHX5X
ZgL/0sDd1jtXn4ULROO8bTERy31SArQGLTBFSDeu0ccMbvzMDLxM3JMI26IPyU/i
eHgsEnDDkNBuqnyiMuiVutmwH4ID5F0ZoiD7GRyd6TQGSpSWcgppFBJnLkcMGnrS
qQIDAQAB
-----END PUBLIC KEY-----"""
my_snowflake_private_key = b"""-----BEGIN PRIVATE KEY-----
MIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQDJJDQ80NIHx1NH
pFvx9bvXeEZPouVnBqJeljcihcLAaRL039gVXhw16tDcPG50oW3PUn5kNnrbmk3X
jJRcpkRlT42wIEqyVGcOExTmwEME3hUDAbiAAVjSwzxX0sBLwg6EjEGOpxv3Td0i
7hQ1z4hWvPsXZ23vy1g5vgkpOCr5R41BlatOvc6uuu0/hxBgjeiJDBLB72I1iizC
HrEdfldmAv/SwN3WO1efhQtE47xtMRHLfVICtAYtMEVIN67Rxwxu/MwMvEzckwjb
og/JT+J4eCwScMOQ0G6qfKIy6JW62bAfggPkXRmiIPsZHJ3pNAZKlJZyCmkUEmcu
RwwaetKpAgMBAAECggEANlkd9EDIP2nQSs9SOLKZKsNI3EO7kHbucHhONXnHAY5i
nN/O1xcysC7eeGOrxL/Jl/dGR3WhBK1Q0ykc/Vu/p1AzjJ9tD3pWzirBvwe8FBid
vM4+N/glM+2k5GYBp3arzYzIOe9VUyEq20FRHKkSwb0Wa2B7CAv9rrx2ZTjUA76i
xB6aZyEueC5D1d0Y/mWNK5hvmAneruupspCoME7e4B666+bReop9Or0oqrL5mnNu
0B073NuHbPIcrkW8qMXHJmzhTOuK1fAiGJ+bc4uvhuJXIXjmilkdQRRQNvNCoB1K
Rcf7a9DmnHveld5KoyWqSpbQlsWV6Fx7bS4CXln1sQKBgQDxT+ier+2EBgCUsv3N
W4PQclrCFwpOfOqtdxlM+DnA5Onzbr3IWWcyZBGGPP7KALdr2WYBA5EuOhFZ4/GH
pJS9pDXbbiKcASNOX9h3hjefnwplDq3XnlKqc0ALMi2B6NF4Num2nmvPfWwX3ZZP
o9kTzvtGUx2LNqxsXTQhVdVpEwKBgQDVYlxm68mPguYBSUUZrkMeJNZHPCKQyhxW
NCU2y5eGCccQSOyC7zX98zDajxlVdfGe9ITmGiZsu0uncH+XNX0Fdu105tBmEMSP
ZDouzEXXmdmYd3kExA+rbyH4goCIo9Re9IhTAEGiTzs7rsLX4Nj9PCWOJW2jMzyi
9BimAbTo0wKBgECCjD1f6q8Qq7cU4qSzglmHOJwKbMbuvg4BeNIKyeW3TJO3VyTo
QZ5HAihQxgxahK5gP9Slj3o8K8dMGJWaeej4rS0sFDSAWV/qX4QUbWpOqgi6E99A
g/jtNoHHuEKyas0oYPJhB5FAhlUa98PymWWiP6pdLdi5lP6jK/x9Zb/hAoGBAMhG
nKGA9tp6qnRUl8WluJsnSfLsLykkeXozUSZf6iTFMpBHUa0G5e8nfRf1rXp3y8M8
jywFKUFufXB3d1mtu10QpYjORpU1cbeAA9f+pCLa5M9kezKM7oQiN4kuu4MD+YTy
EK2OlQvJP7ghrADAqgjslfcXjBLcOTJc1nGhMnI/AoGAFc7V6VdfmGAQiIHvaUsO
QWjg0CEfmUJo070A4OZDWmwdWxWn1wr08T5pg1kzp4E/hRcecPoph6PxUT42LIw8
D/IdvVRUFTmM0Tz1mmpSi+uzzQ/eBUlehYb/3BrabIQkkn24Ji6d43EvCtz3WyvG
b5sNcm8GSg70Z7go1tjbR84=
-----END PRIVATE KEY-----"""
'''


from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization

# Read the private key file
with open('C:\\Users\\Admin\\.ssh\\snowflake_key.p8', 'rb') as key_file:
    private_key_pem = key_file.read()

# Convert to the format Snowflake needs
private_key = serialization.load_pem_private_key(
    private_key_pem,
    password=None,  # Since you said no passphrase
    backend=default_backend()
)

# Serialize to DER format
my_snowflake_private_key = private_key.private_bytes(
    encoding=serialization.Encoding.DER,
    format=serialization.PrivateFormat.PKCS8,
    encryption_algorithm=serialization.NoEncryption()
)

snowflake_config = {
    "user": "luketrmai",
    "account": "jfspetv-wgb43135",
    "private_key": my_snowflake_private_key,
    "warehouse": "compute_wh",
    "database": "raw",
    "schema": "amazon_product",
}

snowflake_table = "product_details" 