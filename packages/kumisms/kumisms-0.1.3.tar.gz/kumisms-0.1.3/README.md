# pykumisms

A class to interact with KumiSMS.

## Quick start

1. Import `kumisms` into your project

   ```python
   import kumisms
   ```

2. Create a KumiSMS object with your API key

   ```python
   gateway = KumiSMS("my_api_key")
   ```

3. Start making requests

   ```python
   gateway.send("+123456789", "Hello!")
   ```