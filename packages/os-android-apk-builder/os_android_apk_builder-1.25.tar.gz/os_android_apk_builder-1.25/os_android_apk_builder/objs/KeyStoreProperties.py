from os_file_handler import file_handler as fh
from os_android_apk_builder.bp import _res


class KeyStoreProperties:
    def __init__(self,
                 key_store_file_path,
                 store_password,
                 key_alias,
                 key_password,
                 v1_signing_enabled,
                 v2_signing_enabled):
        self.key_store_file_path = key_store_file_path
        self.store_password = store_password
        self.key_alias = key_alias
        self.key_password = key_password
        self.v1_signing_enabled = v1_signing_enabled
        self.v2_signing_enabled = v2_signing_enabled

    def build_signin_dict(self):
        return {'storeFile': f'file("{self.key_store_file_path}")',
                'storePassword': f'"{self.store_password}"',
                'keyAlias': f'"{self.key_alias}"',
                'keyPassword': f'"{self.key_password}"',
                'v1SigningEnabled': str(self.v1_signing_enabled).lower(),
                'v2SigningEnabled': str(self.v2_signing_enabled).lower()
                }

    @staticmethod
    def build_from_file(file_path):
        """
        This is just a convenient build function to create the KeyStoreProperties instance from a JSON file.

        Ff you have a sign in file you can set it here (read the github repo for more info) to save you the hassle of inserting the key store props each time
        Args:
            file_path: the path to your sign_in_json_file.json in which the properties of your KeyStore will be saved
        """
        json_dict = fh.json_file_to_dict(file_path)
        return KeyStoreProperties(json_dict[_res.KEY_STORE_FILE_PATH],
                                  json_dict[_res.KEY_STORE_PASSWORD],
                                  json_dict[_res.KEY_KEY_ALIAS],
                                  json_dict[_res.KEY_KEY_PASSWORD],
                                  json_dict[_res.KEY_V1_SIGNING_ENABLED],
                                  json_dict[_res.KEY_V2_SIGNING_ENABLED])
