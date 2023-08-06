"""
cquest_secret_manager

python implementation of the functionalities of secret manager

https://gitlab.com/cquest1/cquest_secret_manager
"""

from google.cloud import secretmanager
from loguru import logger


# === SECRET =========================================================================================================
# LIST SECRETS
def list_secrets(project_id, path_to_secret_manager_creds):
    """
    List all secrets in the given project.
    """

    # Create the Secret Manager client.
    client = secretmanager.SecretManagerServiceClient.from_service_account_json(
        path_to_secret_manager_creds
    )
    logger.info("Connected to secret manager")

    # Build the resource name of the parent project.
    parent = f"projects/{project_id}"

    # List all secrets.
    logger.info("Listing secrets:")
    for secret in client.list_secrets(request={"parent": parent}):
        logger.info("Found secret: {}".format(secret.name))


# CREATE A SECRET
def create_secret(project_id, secret_id, path_to_secret_manager_creds):
    """
    Create a new secret with the given name. A secret is a logical wrapper
    around a collection of secret versions. Secret versions hold the actual
    secret material.
    """

    # Create the Secret Manager client.
    client = secretmanager.SecretManagerServiceClient.from_service_account_json(
        path_to_secret_manager_creds
    )

    # Build the resource name of the parent project.
    parent = f"projects/{project_id}"

    # Create the secret.
    response = client.create_secret(
        request={
            "parent": parent,
            "secret_id": secret_id,
            "secret": {"replication": {"automatic": {}}},
        }
    )

    # Print the new secret name.
    logger.info("Created secret: {}".format(response.name))


# CREATE A SECRET
def delete_secret(project_id, secret_id, path_to_secret_manager_creds):
    """
    Create a new secret with the given name. A secret is a logical wrapper
    around a collection of secret versions. Secret versions hold the actual
    secret material.
    """

    # Create the Secret Manager client.
    client = secretmanager.SecretManagerServiceClient.from_service_account_json(
        path_to_secret_manager_creds
    )

    # Build the resource name of the parent project.
    name = f"projects/{project_id}/secrets/{secret_id}"

    # Delete the secret.
    client.delete_secret(request={"name": name})

    # Print the new secret name.
    logger.info("Deleted secret: {}".format(secret_id))


# === SECRET VERSION =================================================================================================
# LIST SECRET VERSION OF A SECRET
def list_secret_versions(project_id, secret_id, path_to_secret_manager_creds):
    """
    Access the payload for the given secret version if one exists. The version
    can be a version number as a string (e.g. "5") or an alias (e.g. "latest").
    """

    # Create the Secret Manager client.
    client = secretmanager.SecretManagerServiceClient.from_service_account_json(
        path_to_secret_manager_creds
    )

    # Build the resource name of the secret version.
    parent = f"projects/{project_id}/secrets/{secret_id}"

    # Access the secret version.
    version_list = client.list_secret_versions(request={"parent": parent})

    # List secret versions
    #
    # WARNING: Do not print the secret in a production environment - this
    # snippet is showing how to access the secret material.
    logger.info("Listing versions of the secret:")
    for version in version_list:
        logger.info("Found secret version: {}".format(version.name))


# ACCESS A SECRET VERSION
def access_secret_version(
    project_id, secret_id, version_id, path_to_secret_manager_creds
):
    """
    Access the payload for the given secret version if one exists. The version
    can be a version number as a string (e.g. "5") or an alias (e.g. "latest").
    """

    # Create the Secret Manager client.
    client = secretmanager.SecretManagerServiceClient.from_service_account_json(
        path_to_secret_manager_creds
    )

    # Build the resource name of the secret version.
    name = f"projects/{project_id}/secrets/{secret_id}/versions/{version_id}"

    # Access the secret version.
    response = client.access_secret_version(request={"name": name})

    # Print the secret payload.
    #
    # WARNING: Do not print the secret in a production environment - this
    # snippet is showing how to access the secret material.
    payload = response.payload.data.decode("UTF-8")
    return payload
    # logger.info("Plaintext: {}".format(payload))


# ADD A SECRET VERSION
def add_secret_version(project_id, secret_id, payload, path_to_secret_manager_creds):
    """
    Add a new secret version to the given secret with the provided payload.
    """

    # Import the Secret Manager client library.
    from google.cloud import secretmanager

    # Create the Secret Manager client.
    client = secretmanager.SecretManagerServiceClient.from_service_account_json(
        path_to_secret_manager_creds
    )

    # Build the resource name of the parent secret.
    parent = client.secret_path(project_id, secret_id)

    # Convert the string payload into a bytes. This step can be omitted if you
    # pass in bytes instead of a str for the payload argument.
    payload = payload.encode("UTF-8")

    # Add the secret version.
    response = client.add_secret_version(
        request={"parent": parent, "payload": {"data": payload}}
    )

    # Print the new secret version name.
    logger.info("Added secret version: {}".format(response.name))


# DELETE SECRETE VERSION
def delete_secret_version(
    project_id, secret_id, version_id, path_to_secret_manager_creds
):
    """
    Delete the payload for the given secret version if one exists. The version
    can be a version number as a string (e.g. "5") or an alias (e.g. "latest").
    """

    # Import the Secret Manager client library.
    from google.cloud import secretmanager

    # Create the Secret Manager client.
    client = secretmanager.SecretManagerServiceClient.from_service_account_json(
        path_to_secret_manager_creds
    )

    # Build the resource name of the secret version.
    name = f"projects/{project_id}/secrets/{secret_id}/versions/{version_id}"

    # Delete the secret version.
    client.destroy_secret_version(request={"name": name})

    # Print the secret payload.
    #
    # WARNING: Do not print the secret in a production environment - this
    # snippet is showing how to access the secret material.
    # payload = response.payload.data.decode("UTF-8")
    logger.info("Secret deleted: {}".format(secret_id))
