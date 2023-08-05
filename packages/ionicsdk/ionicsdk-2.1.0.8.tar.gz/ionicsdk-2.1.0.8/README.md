# Ionic Python SDK

## Overview
This module provides Python developers with access to the core services of the Ionic Platform.  At a high level, the platform provides developers with straightforward methods to
* Securely create and retrieve data protection keys
* Use these keys to encrypt or decrypt application data
* Encrypt or decrypt arbitrary files
* Enroll users and devices with the Ionic backend system.

## Quick Start
Once you have access to an Ionic account (sign up for free at our [developer portal](https://ionic.com/developers/)), the Python environment makes it very simple to access some central features of the platform.   The example below assumes you have already enrolled your system and have a default peristor.

```python
import ionicsdk                            # top level module for all Ionic classes

plaintext = "Welcome to the Python SDK"    # create some text to encrypt
agent = ionicsdk.Agent()                   # the "Agent" class provides access to several common services.

cipher = ionicsdk.ChunkCipherV1(agent)     # a "cipher" object provides "encrypt" and "decrypt" operations.
                                           # it uses the supplied "agent" to create and retrieve keys.
ciphertext = cipher.encryptstr(plaintext)
print ciphertext
decrypted = cipher.decryptstr(ciphertext)
print decrypted
```

## Additional Information
The Ionic Python SDK distribution includes online documentation for the classes and methods.   You can review this documentation by browsing to the "index.html" file within the "docs" directory.  It is also available online at the [Machina Python SDK Documentation](https://dev.ionic.com/sdk/docs/ionic_platform_sdk?language=python)

In order to use the SDK, you will need to enroll in one or more "Ionic tenants".  If you don't already have an established tenant, you can create one for free at [the Ionic Machina Developer Portal](https://ionic.com/developers/), as well as find additional information, documentation, and community resources.
