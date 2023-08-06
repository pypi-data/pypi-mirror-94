"""
cquest_secret_manager

python implementation of the functionalities of secret manager

https://gitlab.com/cquest1/cquest_secret_manager
"""
import json

from google.cloud import secretmanager
from loguru import logger


class SecretManager:

    # Constructor --------------------------------------
    def __init__(self, path_to_secret_manager_creds):
        # Create the Secret Manager client.
        self.client = (
            secretmanager.SecretManagerServiceClient.from_service_account_json(
                path_to_secret_manager_creds
            )
        )
        logger.info("Connected to secret manager")
        self.project_id = json.load(open(path_to_secret_manager_creds))["project_id"]

    # === SECRET =====================================================================================================
    # GET THE LIST OF SECRET IDs
    def get_list_of_secrets(self):
        """
        Get the list of the secret IDs.
        """

        # Build the resource name of the parent project.
        parent = f"projects/{self.project_id}"

        # Save the names of all secrets to the list.
        logger.debug("Calling gcloud native list_secrets function")
        list_of_secrets = self.client.list_secrets(request={"parent": parent})

        # Return the list of the secret IDs
        return list_of_secrets

    # LIST (PRINT) SECRETS (IDs)
    def list_secrets(self):
        """
        List all secrets in the given project.
        """

        # Get list of the secrets
        list_of_secrets = self.get_list_of_secrets()

        # Log the IDs of all secrets.
        logger.info("Listing secrets:")
        for secret in list_of_secrets:
            logger.info("Found secret: {}".format(secret.name))

    # CREATE A SECRET
    def add_secret(self, secret_id):
        """
        Create a new secret with the given name. A secret is a logical wrapper
        around a collection of secret versions. Secret versions hold the actual
        secret material.
        """

        # Build the resource name of the parent project.
        parent = f"projects/{self.project_id}"

        # Create the secret.
        logger.debug("Calling gcloud native create_secret function")

        response = self.client.create_secret(
            request={
                "parent": parent,
                "secret_id": secret_id,
                "secret": {"replication": {"automatic": {}}},
            }
        )

        # Print the new secret name.
        logger.info("Created secret: {}".format(response.name))

        # Return the name of the new secret
        return response.name

    # CREATE A SECRET
    def delete_secret(self, secret_id):
        """
        Create a new secret with the given name. A secret is a logical wrapper
        around a collection of secret versions. Secret versions hold the actual
        secret material.
        """

        # Build the resource name of the parent project.
        name = f"projects/{self.project_id}/secrets/{secret_id}"

        # Delete the secret.
        logger.debug("Calling gcloud native delete_secrets function")

        self.client.delete_secret(request={"name": name})

        # Print the deleted secret name.
        logger.info("Deleted secret: {}".format(secret_id))

    # === SECRET VERSION =============================================================================================
    # GET A LIST OF VERSION IDs FOR A SECRET
    def get_list_of_secret_versions(self, secret_id):
        """
        Gets the list of version IDs for the secret if one exists.
        """

        # Build the resource name of the secret version.
        parent = f"projects/{self.project_id}/secrets/{secret_id}"

        # Access the secret version.
        logger.debug("Calling gcloud native list_secret_versions function")
        version_list = self.client.list_secret_versions(request={"parent": parent})

        # Create the list version IDs for the secret
        list_of_versions = []
        for version in version_list:
            # appends to the list a string in form f"projects/{project_id}/secrets/{secret_id}"
            list_of_versions.append({"name": version.name, "state": version.state.name})

        # Return the list of IDs
        return list_of_versions

    # LIST (PRINT) SECRET VERSIONS (IDs) OF A SECRET
    def list_secret_versions(self, secret_id):
        """
        Prints the list of the version IDs for the secret if one exists.
        """

        # Get the list of version IDs for the secret
        list_of_version_ids = self.get_list_of_secret_versions(secret_id)

        # Print version IDs
        logger.info("Listing versions of the secret '{}': ".format(secret_id))
        for vrsn_id in list_of_version_ids:
            logger.info(
                "Found secret version: {} , state: {}".format(
                    vrsn_id["name"], vrsn_id["state"]
                )
            )

    # ACCESS A SECRET VERSION
    def access_secret_version(self, secret_id, version_id="latest"):
        """
        Access the payload (the value of the secret version) for the given secret version if one exists.
        The version can be a version number as a string (e.g. "5") or an alias (e.g. "latest").
        """

        # Build the resource name of the secret version.
        name = f"projects/{self.project_id}/secrets/{secret_id}/versions/{version_id}"

        # Access the secret version and decode it
        logger.debug("Calling gcloud native access_secret_version function")

        response = self.client.access_secret_version(request={"name": name})
        payload = response.payload.data.decode("UTF-8")

        # Print the secret payload.
        # WARNING: Do not print the secret in a production environment - this
        # snippet is showing how to access the secret material.
        # logger.info("Plaintext: {}".format(payload))
        logger.debug("Plaintext: {}".format(payload))
        # return payload of the secret version
        return payload

    # ADD A SECRET VERSION
    def add_secret_version(self, secret_id, payload):
        """
        Add a new secret version to the given secret with the provided payload.
        Payload - the sensitive/secret data
        """

        # Build the resource name of the parent secret.
        parent = self.client.secret_path(self.project_id, secret_id)

        # Convert the string payload into a bytes. This step can be omitted if you
        # pass in bytes instead of a str for the payload argument.
        payload = payload.encode("UTF-8")

        # Add the secret version.
        logger.debug("Calling gcloud native add_secret_version function")

        response = self.client.add_secret_version(
            request={"parent": parent, "payload": {"data": payload}}
        )

        # Print the new secret version name.
        vrsn_id_added = response.name
        logger.info("For secret {} added version: {}".format(secret_id, vrsn_id_added))

        # Return the id of the added version
        return vrsn_id_added

    # DELETE SECRETE VERSION
    def destroy_secret_version(self, secret_id, version_id="latest"):
        """
        Delete the payload for the given secret version if one exists. The version
        can be a version number as a string (e.g. "5") or an alias (e.g. "latest").
        """

        # Build the resource name of the secret version.
        name = f"projects/{self.project_id}/secrets/{secret_id}/versions/{version_id}"

        # Delete the secret version.
        logger.debug("Calling gcloud native destroy_secret_version function")

        response = self.client.destroy_secret_version(request={"name": name})

        # Lod deleted secret version id
        vrsn_id_deleted = response.name
        logger.info(
            "For secret {} deleted version: {}".format(secret_id, vrsn_id_deleted)
        )

        # return deleted secret version id
        return vrsn_id_deleted
