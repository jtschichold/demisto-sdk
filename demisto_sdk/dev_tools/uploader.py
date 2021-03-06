import demisto_client
import os

from demisto_sdk.common.tools import print_color, LOG_COLORS, print_v
from demisto_sdk.yaml_tools.unifier import Unifier


class Uploader:
    """Upload the integration specified in self.infile to the remote Demisto instance.
        Attributes:
            path (str): The path of an integration file or a package directory to upload.
            log_verbose (bool): Whether to output a detailed response.
            unify (bool): Whether to unify a package.
            client (DefaultApi): Demisto-SDK client object.
        """

    def __init__(self, path: str, insecure: bool = False, verbose: bool = False):
        self.path = path
        self.log_verbose = verbose
        self.unify = os.path.isdir(self.path)
        self.client = demisto_client.configure(verify_ssl=not insecure)

    def upload(self):
        """Upload the integration specified in self.infile to the remote Demisto instance.
        """
        if self.unify:  # Create a temporary unified yml file
            try:
                unifier = Unifier(self.path, dest_path=self.path)
                self.path = unifier.merge_script_package_to_yml()[0][0]
            except IndexError:
                print_color('Error: Path input is not a valid package directory.', LOG_COLORS.RED)
                return 1

        # Upload the file to Demisto
        result = self.client.integration_upload(file=self.path)

        # Print results
        print_v(f'Result:\n{result.to_str()}', self.log_verbose)
        print_color(f'Uploaded \'{result.name}\' successfully', LOG_COLORS.GREEN)

        if self.unify:  # Remove the temporary file
            os.remove(self.path)

        return 0
