# Ghost

**About**

Ghost is a tool based on Python, that can encrypt or decrypt text-files, strings and sock-streams.
In the base implementation it contains the core classes and functions for the de-/encryption
of strings and files and additional an encrypted chat-system.

**Encryption**

Ghost uses a simple but secure encryption, which decrypts a string with a given or random key to non-readable
cypher text. This text can be decrypted with the cypher text itself, the key, and the char-list
used for encryption. It can decode the usual utf-8 signs, but be aware that other signs like "ß" or "©" will be skipped 
in the encryption. A randomly generated key with 60 signs and the default 93 possible default-chars has 60^93 
possible positions and would take a lot more than 5*10^14 years to crack. Because of this, the encryption 
is with a random key probably uncrackable. 

**How to use**

You can install the phantom package with `pip install ghost-encrypt`. This contains how mentioned above, the functions 
and classes for the de-/encryption of strings, text-files and sock-streams, as well as the `arg-parser` package. The 
tool can be integrated, but it works as standalone, too. Just type `ghost --help` or if that doesn't work 
`py -m ghost --help` to get a list and an interface to execute the commands.

**Usage examples**

I personally use that script to de-/encrypt my passwords file and sometimes for chatting with my friends 
(Encryption can be removed by passing 'a' as the key). It is also very useful when u are storing data for
a game that shouldn't be modified or for decrypting passwords on a backend.
Look at the example files or at `__main__.py` to see some usages.
