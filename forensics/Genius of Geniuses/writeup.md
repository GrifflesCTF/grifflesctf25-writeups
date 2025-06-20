The flag is embedded in the image using least significant bits. Notably, the image was encrypted in BGR as hinted by the use of the opencv library, hence online tools that use RGB order will not work. Decoding (sample code is included in [encLsb.py](encLsb.py)), we obtain the base64 string "Z3JpZmZsZXNDVEZ7MU5UMF83SDNfVU5SRTRDSDQ4TDNfVkUxTH0=". Decrypting this gives the flag --> grifflesCTF{1NT0_7H3_UNRE4CH48L3_VE1L}

Alternatively, [AperiSolve](https://www.aperisolve.com/) is able to retrieve the Base64 string easily:
![Aperisolve Image](image.png)