# Machina SDK Release 2.1.0

## Introduction
Welcome to the 2.1 release of the Machina SDK.  This release contains significant changes to the 
underlying cryptography, including the integration (by default) of the FIPS-validated version of the OpenSSL open source library.

Details are summarized below.

## New Features / Improvements

### CryptoPP Usage Mostly Replaced with OpenSSL
- SDK usage of the CryptoPP cryptography library has been replaced with the OpenSSL v1.0.2 library, which is
  [FIPS 140-2 validated](https://www.openssl.org/docs/fips.html).
- CryptoPP usage is limited to use of the
  [Shamir Secret Sharing](https://www.cryptopp.com/docs/ref/class_secret_sharing.html) algorithm (used in
  `ionicsdk.secretshare.SecretSharePersistor`).

### Alternative Cryptography Library (Platform-Specific) Available
- The SDK package includes an additional platform-specific implementation of the CryptoAbstract interface.  This
  library may be used instead of the OpenSSL FIPS implementation if needed, in order to work around cross-platform 
  limitations.
- The `ionicsdk.cryptoutil.setCryptoSharedLibraryCustomPath()` and
  `ionicsdk.cryptoutil.getCryptoSharedLibraryLoadedFilename()` APIs have been added to ascertain the version 
  of the loaded cryptography library.

### Identity Assertion Validation API Available
The API `ionicsdk.agent.Agent.validateassertion()` has been added, allowing SDK users to verify the authenticity of
identity assertions generated both externally, and by the SDK.

### Create Identity Assertion API Uses Default Nonce When None Provided 
On use of SDK identity assertion APIs, a default nonce is provided when no nonce is supplied by the caller.
- `ionicsdk.agent.Agent.createidassertion()`
- `ionicsdk.agent.Agent.validateassertion()`

### Additional Documentation Included with Release Distributable
The SDK release distributable now includes the following documents, in markdown and html formats:
- `README`, describing high-level SDK project functionality
- `LICENSE`, providing the Machina license agreement for Ionic resources
- `CHANGELOG`, with line items providing summary information about the issues included in each release
- `RELEASE_NOTES`, detailing the features and fixes included in the release

### Machina Service Policy Decision Simulation Support
The SDK now allows the use of a flag when calling `CreateKey` to perform a policy evaluation at the service 
without creating any keys.

## Issues Addressed
- A logging issue has been addressed in the OpenXml file cipher when reading unexpected content from a PowerPoint file.
- Issues have been corrected that caused some `doxygen` documentation to be excluded from the SDK distributables.
- The `ISCrypto` library module now includes additional logging, in order to easily diagnose usage issues.
- KeyVault requests now properly filter expired keys out of responses.
- The documentation for the CreateKey operation notes the service limitation on the number of newly created keys that
may be requested in a single request.
- The SDK [pypi page](https://pypi.org/project/ionicsdk/) now includes links to Python content 
  on the [Ionic Machina website](https://dev.ionic.com/sdk/docs/ionic_platform_sdk?language=python).
- The C and Python SDK implementations now provide APIs to perform multiple `CreateKey` operations 
  in the context of a single call to the Machina service.
 
## Discontinued Support
- Python 2 is no longer supported.  [Sunsetting Python 2](https://www.python.org/doc/sunset-python-2/)

## Additional Notes
- Since Crypto initialization now loads a library module dynamically, it should not be called in startup code.

## Supported Platforms
The Machina SDK is tested against the following platform configurations:

|Platform    |Version                     |
|------------|----------------------------|
|Linux       | CentOS 7.8-2003            |
|Linux       | Ubuntu 18.04               |
|Windows     | Windows 8.1 (32 and 64 bit)|
|Windows     | Windows 10 (32 and 64 bit) |
|macOS       | macOS 13 (High Sierra)     |
|macOS       | macOS 14 (Mojave)          |
|macOS       | macOS 15 (Catalina)        |
|Python      | 3.8.x                      |
