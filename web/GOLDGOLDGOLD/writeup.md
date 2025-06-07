# Part 1, IDOR

1. On the inventory page, we have 10 cases, but no flag is revealed though. Look at the endpoint, notice a pattern? An example case endpoint looks like this: `/cases/case_1`. Try putting in some weird values into the endpoint, for example `case_11`. `case_11` leads us to a case that says only admins can open the case.

# Part 2, JWT Attack

2. Obviously, the credentials given to us does not have admin access. We need to find a way to trick the website into thinking that we are an admin.
3. Check the site's cookies. There is a cookie called token, which is a JWT. We can brute force the JWT's secret key to modify it.
4. Using `john --format=HMAC-SHA256 --wordlist=rockyou.txt jwt.txt`, we are able to get the secret key `ilovegold` (note that one must use JTR jumbo as HS256 is not supported in the original one)
5. Using an online JWT debugger, we can change the `user` from `Griffles` to `admin`. We then sign the new JWT with the secret key, `ilovegold`
6. With the new token, visit `case_11` again, and the flag is revealed.
7. The flag is grifflesCTF{w3_g0t_8_c8s3_h8rd3n3d_b1u3_g3m_m8_dr1ll8}
