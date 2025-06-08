This challenge trains you to look at places with common low-hanging fruits. To get the flag, find pieces of the flag sprinkled al over the site.

1. In `/`, you will find this comment:
	```
		<!-- Huh??? What is there to see here? Z3JpZmZsZXNDVEZ7bDB3Xw== -->
	```
	base64 decode `Z3JpZmZsZXNDVEZ7bDB3Xw==` to get: `grifflesCTF{l0w_`

2. In `/robots.txt`, you find that it has this route: `/4675163243/`. Go to that route and you will get the 2nd part: `h4ng1ng_fr`

3. Check cookies! You will find a cookie named `flag` with the value `u1ts_ar3_tA3tyyy}`. This is the 3rd part of the flag.

The flag is `grifflesCTF{l0w_h4ng1ng_fru1ts_ar3_tA3tyyy}`

**P.S.**
This was supposed to hint at the low-hanging fruits in the site.
```<p>Do you have what it takes? Where would it be possibly hidden? Our school canteen? The MPH? Performing Arts Center? The Classrooms? The new Rainforest? WHERE?????</p>```