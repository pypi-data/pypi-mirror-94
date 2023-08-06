from os_android_apk_builder import apk_builder
from os_android_apk_builder.objs.KeyStoreProperties import KeyStoreProperties
from os_android_apk_builder.objs.VersionProperties import VersionProperties


print("yey!")
# # set your KeyStore properties
# key_store_props = KeyStoreProperties(key_store_file_path='/path/to/keystore/file.jks',
#                                      store_password='StorePassword123',
#                                      key_alias='alias name',
#                                      key_password='KeyPassword123',
#                                      v1_signing_enabled=True,
#                                      v2_signing_enabled=True)
#
# # set the version properties (version code and version name)
# version_props = VersionProperties(new_version_code=VersionProperties.RAISE_VERSION_BY_ONE,
#                                   new_version_name="1.0.3")
# # you can set VersionProperties.KEEP_OLD_VERSION and VersionProperties.RAISE_VERSION_BY_ONE to each of these version types
#
#
# apk_builder.build_apk(project_path='/path/to/android/project',
#                       apk_dst_dir_path='/path/to/apk/output/directory',
#                       key_store_properties=key_store_props,
#                       version_properties=version_props)
#
# apk_builder.build_app_bundle(project_path='/path/to/android/project',
#                              app_bundle_dst_dir_path='/path/to/app/bundle/output/directory',
#                              key_store_properties=key_store_props,
#                              version_properties=version_props)
#
# # you can also
# # key_store_props = KeyStoreProperties.build_from_file(file_path='path/to/properties.json')
