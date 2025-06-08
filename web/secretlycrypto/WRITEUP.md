1. By examining the source code, you will find that the username and password hash can be easily determined. This is given that AES is a symmetric encryption algorithm and all keys and IVs are known.

2. It is impossible to determine the actual password due to the MD5 hash. You should, however, see that only the password hash is required and sent in the POST request. You can mock the request with curl, Postman, or any other tool.

3. Using the secret obtained from the `/auth` endpoint, you can then exchange it for the flag from the `/flag` endpoint.

The username is `griffles`, the password is `kR!JA2VUR%8HxCkP`, and the password hash is `0bcb50168011c647cb1f6916c2ace7cc`.

The flag is `grifflesCTF{n07_4c7u4l1y_cRyp70_l0l}`.
