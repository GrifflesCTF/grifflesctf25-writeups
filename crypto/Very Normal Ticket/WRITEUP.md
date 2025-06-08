## Part 1

We see a bunch of gibberish written on the ticket. From the line "6 Mxqh 2025", we can guess that it probably means "6 June 2025" (date of the CTF). It is not difficult to verify that "June" indeed maps to "Mxqh" via Caesar cipher with a shift of 3.
- Alternatively, you can dump the entire first 3 lines (or maybe even just a part of it) into https://www.dcode.fr/cipher-identifier and it should identify Caesar cipher correctly.

Now, we decrypt everything else to get:
```
Concert by Griffles Dancers
General admission (2 pax)
6 June 2025

Name: Griffles
Order ID: Z3JpZmZsZXNDVEZ7ZDRuY2luZydzX215
```

Well, `Z3JpZmZsZXNDVEZ7ZDRuY2luZydzX215` looks sus. We dump it into [Cyberchef](https://gchq.github.io/CyberChef/#input=WjNKcFptWnNaWE5EVkVaN1pEUnVZMmx1WnlkelgyMTU) and it automatically decrypts it from Base64 to `grifflesCTF{d4ncing's_my`
- Alternatively, you can use the [cipher identifier](https://www.dcode.fr/cipher-identifier) again and it will also identify the Base64 encryption.

## Part 2

We see 4 stickman images. Doing a reverse image search on them should yield results on the Dancing Men Cipher. Giving that a search, one of the top results would be https://www.dcode.fr/dancing-men-cipher and we can decrypt the images to get "true". Combining with the underscores beside the images, we get the 2nd part of the flag: `_true_`.
- Btw, the cipher does not distinguish between lowercase and uppercase, so I'm sorry theres no way to know if it's "TRUE" or "true". You just have to try both...

## Part 3

We see 2 qr codes. Scanning either of them doesn't work. How? We overlay them! (I mean, the qr codes kinda look like they have missing bits right...)

A simple way is to screenshot them and use a [background remover](https://www.remove.bg/), then upload to google slides or something similar to overlay them.

Scanning this new qr code, we get `p4ssi0n!!}`. This completes the flag, `grifflesCTF{d4ncing's_my_true_p4ssi0n!!}`.