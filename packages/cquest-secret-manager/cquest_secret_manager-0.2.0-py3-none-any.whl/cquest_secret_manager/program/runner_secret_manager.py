"""
    Script runs while not exited:
        a.displays menu
        b.asks which function to execute
        c.executes the function
        d.returns to menu

    Functions:
        0. Exit
        11. List secrets
        12. Create Secret
        13. Delete Secret
        21. List secret versions
        22. Access secret version
        23. Add secret version
        24. Delete secret version

"""
import json

import cquest_secret_manager_functions as sm


# PRINT MENU ----------------------------------------------------------------------------------------------------
def print_menu(dict_of_options):
    print("Please choose function to execute (enter according number):")
    for option_num in dict_of_options:
        print(str(option_num) + " : " + dict_of_available_options[option_num])


def loop_user_interaction(dict_of_options, path_to_credentials, prjct_id):
    # init input
    input_int = 99

    # repeat while no exit
    while input_int != 0:
        # print menu:
        print_menu(dict_of_options)
        # get input
        input_int = int(input())

        # Exit the loop if the input is 0
        if input_int == 0:
            print("Buy!")
            return

        else:
            # print input
            print("got: " + str(input_int))
            # execute function
            if input_int == 11:
                # 11. List secrets
                sm.list_secrets(
                    project_id=prjct_id,
                    path_to_secret_manager_creds=path_to_credentials,
                )
            elif input_int == 12:
                # 12. Create Secret
                scrt_id = input("Enter secret id for the new secret:")
                sm.create_secret(
                    project_id=prjct_id,
                    path_to_secret_manager_creds=path_to_credentials,
                    secret_id=scrt_id,
                )
            elif input_int == 13:
                # 13. Delete Secret
                scrt_id = input("Enter secret id which you want to delete:")
                sm.delete_secret(
                    project_id=prjct_id,
                    path_to_secret_manager_creds=path_to_credentials,
                    secret_id=scrt_id,
                )
            elif input_int == 21:
                # 21. List secret versions
                scrt_id = input(
                    "Enter secret id for which you want to see its versions:"
                )
                sm.list_secret_versions(
                    project_id=prjct_id,
                    path_to_secret_manager_creds=path_to_credentials,
                    secret_id=scrt_id,
                )
            elif input_int == 22:
                # 22. Access secret version
                scrt_id = input(
                    "Enter secret id for which you want to see its versions:"
                )
                sm.access_secret_version(
                    project_id=prjct_id,
                    path_to_secret_manager_creds=path_to_credentials,
                    secret_id=scrt_id,
                    version_id="latest",
                )
            elif input_int == 23:
                # 23. Add secret version
                scrt_id = input(
                    "Enter secret id for which you want to see its versions: "
                )

                # from string or from json file?
                print(
                    "Do you want to enter the payload as a string (1) or load it from a .json file (2)?"
                )
                int_option = int(input("Enter number: "))

                secret_payload_str = None
                if int_option == 1:
                    print("from string")
                    secret_payload_str = input(
                        "Please enter the payload string for the secret version: "
                    )

                elif int_option == 2:
                    # load and convert file to string
                    secret_payload_json_file_path = input(
                        "please enter filepath for the .json file from "
                        "which to create the secret version: "
                    )
                    with open(secret_payload_json_file_path, "r") as f:
                        secret_payload_str = json.dumps(json.load(f))

                # add secret version
                sm.add_secret_version(
                    project_id=prjct_id,
                    path_to_secret_manager_creds=path_to_credentials,
                    secret_id=scrt_id,
                    payload=secret_payload_str,
                )

            elif input_int == 24:
                # 24. Delete secret version
                scrt_id = input(
                    "Enter secret id for which you want to see its versions: "
                )
                sm.delete_secret_version(
                    project_id=prjct_id,
                    path_to_secret_manager_creds=path_to_credentials,
                    secret_id=scrt_id,
                    version_id="latest",
                )


# USER INTERACTION:
# create menu
dict_of_available_options = {
    00: "Exit",
    11: "List secrets",
    12: "Create Secret",
    13: "Delete Secret",
    21: "List versions of a secret",
    22: "Access secret version",
    23: "Add secret version",
    24: "Delete secret version",
}
# get path to ecret-manager-credentials
path_to_creds = input("Specify the path to secret-manager-service-account-creds: ")
# get project
project_id = input("Enter the project_id: ")

# manage secrets and versions
loop_user_interaction(dict_of_available_options, path_to_creds, project_id)
