import os
from dotenv import load_dotenv
from keycloak import KeycloakOpenID, KeycloakAdmin

# Ensure environment variables are set
KEYCLOAK_URL = os.getenv('KEYCLOAK_URL')
REALM_NAME = os.getenv('REALM_NAME')
CLIENT_ID = 'fastapi-test'
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
ADMIN_ID = os.getenv('ADMIN_ID')
ADMIN_SECRET = os.getenv('ADMIN_SECRET')

# # Check if environment variables are properly set
# if not all([KEYCLOAK_URL, REALM_NAME, CLIENT_ID, CLIENT_SECRET]):
#     raise ValueError("One or more required environment variables are missing.")

# Configure Keycloak OpenID client
keycloak_openid = KeycloakOpenID(
    server_url=KEYCLOAK_URL,
    realm_name=REALM_NAME,
    client_id='fastapi-test',
    client_secret_key='Qml2NtS5ecrXl5899BqYGiLBITNToI9k',
    verify=True
)

# Configure Keycloak Admin client
keycloak_admin = KeycloakAdmin(
    server_url=KEYCLOAK_URL,
    # username=ADMIN_ID,
    # password=ADMIN_SECRET,
    realm_name=REALM_NAME,
    user_realm_name=REALM_NAME,
    client_id=CLIENT_ID,
    client_secret_key=CLIENT_SECRET,
    verify=True
)
# users = keycloak_admin.get_users()
# Get user details by username (or email)


# token = keycloak_openid.token(username='van',password='van123')
# print(token)
# # Example: Test a call to get the realm roles (check if admin connection is working)
# try:
#     roles = keycloak_admin.get_roles()
#     print("Successfully retrieved roles:", roles)
# except Exception as e:
#     print("Error occurred while retrieving roles:", str(e))
