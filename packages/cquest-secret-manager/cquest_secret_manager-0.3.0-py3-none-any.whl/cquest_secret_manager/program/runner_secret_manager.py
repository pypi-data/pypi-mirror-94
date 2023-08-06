"""
    Script runs while not exited:
        a. Displays menu
        b. Asks which function to execute
        c. Executes the function
        d. Returns to menu

    Functions:
        0. Exit
        1. List secrets
        2. List secret versions
        3. Add secret
        4. Add secret version
        5. Delete secret
        6. Destroy secret version
        7. Access secret version
"""
import json
import sys

import google.api_core.exceptions
from cquest_secret_manager_functions import SecretManager
from loguru import logger


# Get input from menu ----------------------------------------------------------------
def get_user_input_int(start, end, question_message):
    input_int = None
    while input_int not in range(start, end):
        # Payload from string or from json file?
        logger.info(question_message)
        logger.info("Value has to be integer in range [{}...{}]".format(start, end - 1))

        try:
            input_int = int(input("Enter number: ").strip())
        except ValueError:
            logger.error("Value has to be integer")

    return input_int


class SecretManagerRunner:

    # Constructor ------------------------------------------------------------------------
    def __init__(self, path_to_credentials):
        self.func_list = [
            method for method in self.__dir__() if method.__contains__("secret")
        ]
        self.menu_list = self.create_menu()
        self.sm = SecretManager(path_to_secret_manager_creds=path_to_credentials)
        self.prjct_id = self.sm.project_id

    # MENU ===========================================================================================================
    # Create -----------------------------------------------------------------------------
    def create_menu(self):
        # reformat function names to be better readable -> to menu list
        menu_list = ["Exit"] + [
            " ".join(option.split("_")).capitalize() for option in self.func_list
        ]
        return menu_list

    # Print ------------------------------------------------------------------------------
    def print_menu(self):
        logger.info("Available functions:")
        for i in range(len(self.menu_list)):
            logger.info("*** " + str(i) + " : " + self.menu_list[i])

    # SECRETS and VERSIONS ==========================================================================================
    # List secrets ------------------------------------------------------------------------
    def list_secrets(self):
        self.sm.list_secrets()

    # List versions ----------------------------------------------------------------------
    def list_secret_versions(self):
        # Get input from user:
        scrt_id = input(
            "Enter secret id for which you want to see its versions: "
        ).strip()

        # List secrets
        self.sm.list_secret_versions(
            secret_id=scrt_id,
        )

    # Add secret -------------------------------------------------------------------------
    def add_secret(self):
        # Get input from user:
        scrt_id = input("Enter secret id for the new secret: ").strip()

        # Add secret
        self.sm.add_secret(secret_id=scrt_id)

    # Add version ------------------------------------------------------------------------
    def add_secret_version(self):
        # Get secret ID
        scrt_id = input("Enter secret id for which you want to add a version: ").strip()

        # Get input: from string vs json
        message = """
                    Would you like to
                    enter the payload as a string (1),
                    load it from a .json file (2),
                    return to menu (0)?
        """
        input_int = get_user_input_int(0, 3, message)

        # Exit
        if input_int == 0:
            return

        # Create payload string
        secret_payload_str = None
        if input_int == 1:
            # From String
            print("from string")
            secret_payload_str = input(
                "Enter the payload string for the secret version: "
            )

        elif input_int == 2:
            # load and convert json file to string
            secret_payload_json_file_path = input(
                "Enter filepath for the .json file from "
                "which to create the secret version: "
            )
            with open(secret_payload_json_file_path, "r") as f:
                secret_payload_str = json.dumps(json.load(f))

        # Add secret version
        self.sm.add_secret_version(
            secret_id=scrt_id,
            payload=secret_payload_str,
        )

    # Delete secret ----------------------------------------------------------------------
    def delete_secret(self):
        scrt_id = input("Enter secret id which you want to delete:").strip()
        self.sm.delete_secret(
            secret_id=scrt_id,
        )

    # Delete version ---------------------------------------------------------------------
    def destroy_secret_version(self):
        # Get user input secret_id
        scrt_id = input(
            "Enter secret id for which you want to delete a version: "
        ).strip()

        # Get list of enabled versions
        lst_of_enabled_versions = self.get_list_of_enabled_versions(scrt_id)

        # Get user input version id
        vrsn_id = input(
            "Enter version id (enabled version IDs: {}) to delete:".format(
                lst_of_enabled_versions
            )
        ).strip()

        # delete secret version
        try:
            self.sm.destroy_secret_version(
                secret_id=scrt_id,
                version_id=vrsn_id,
            )
        except google.api_core.exceptions.FailedPrecondition:
            logger.error("This version is already DESTROYED.")

    # Get Enabled Versions ---------------------------------------------------------------
    def get_list_of_enabled_versions(self, scrt_id):
        # get list of versions
        list_of_versions = self.sm.get_list_of_secret_versions(
            secret_id=scrt_id,
        )

        # Check if version is enabled --> add to list
        lst_of_enabled_vrsns = []
        for version in list_of_versions:
            if version["state"] == "ENABLED":
                vrsn_id = version["name"].split("/")[-1]
                lst_of_enabled_vrsns.append(vrsn_id)

        # Return list of enabled versions
        return lst_of_enabled_vrsns

    # Access version ---------------------------------------------------------------------
    def access_secret_version(self):
        scrt_id = input("Enter secret id for which you want access a version:").strip()

        # Get list of enabled versions
        lst_of_enabled_versions = self.get_list_of_enabled_versions(scrt_id)
        vrsn_id = input(
            "Enter version id (available IDs: {}) to access:".format(
                lst_of_enabled_versions
            )
        ).strip()

        try:
            self.sm.access_secret_version(
                secret_id=scrt_id,
                version_id=vrsn_id,
            )
        except google.api_core.exceptions.FailedPrecondition:
            logger.error(
                "This version is either DISABLED or DESTROYED -> can not access it."
            )

    # INTERACT WITH USER VIA MENU : LOOP ============================================================================
    def loop_user_interaction(self):

        # repeat while no exit
        while True:
            # Print menu
            self.print_menu()

            # Get input from user
            message = "Please enter integer to execute function: "
            input_int = get_user_input_int(0, len(self.menu_list), message)

            # Check for Exit
            if input_int == 0:
                break

            if input_int is None:
                continue

            # get function name
            func = self.func_list[input_int - 1]
            logger.info("Executing function: " + func)

            # execute function
            try:
                eval("self." + func + "()")
            except google.api_core.exceptions.NotFound:
                logger.error(
                    "Secret/Version not found! try listing secrets/versions to see available options"
                )
            except google.api_core.exceptions.PermissionDenied:
                logger.error(sys.exc_info()[0])

        # 0 --> EXIT --------------------------------------------------
        print("Buy!")


# USER INTERACTION: =================================================================================================
# Get path to ecret-manager-credentials
path_to_creds = input(
    "Specify the path to secret-manager-service-account-creds: "
).strip()

# Create Object of Secret Manager Runner
sm_runner = SecretManagerRunner(path_to_creds)

# Manage secrets and versions
sm_runner.loop_user_interaction()
