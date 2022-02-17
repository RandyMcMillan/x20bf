<HR>

<center><H4>0xbf20 - A general purpose messaging protocol</center>

## Status of this Proposal

This document proposes an Internet standards track protocol for transporting, broadcasting and syndication of messages over common internet communications channels. The distribution of all documents related to this proposal are unlimited and unencumbered by any [LICENSE](LICENSE), but some are included anyway.

## Abstract

This document describes the ox20bf protocol message structure and related operations associated with message field ordering and data typing. 0x20bf is meant to be simple, enabling flexability of implementation. Gnupg is used for text message encryption. Git version control is used for archiving messages.

## Protocol - Field definitions

### message field delimiter
`:` - message field delimiter

### gnupg (long/short key ID) of the reciever of a message
`GPGR` - gnupg (long/short key ID) of the reciever of a message

### gnupg (long/short key ID) of the sender of a message
`GPGS` - gnupg (long/short key ID) of the sender of a message

##### Example - ping short format
`:GPGR:GPGS:` `:<recipient>:<sender>:`

### algorithm field
`:ALGO:` indicates encryption algorithm used for message construction

##### Example
`:ALGO:ALGO:ALGO:ALGO:`

`:PUBKEY:CIPHER:HASH:COMPRESSION:`

`:RSA:AES256:SHA256:ZIP:`

##### gnupg supported algorithms:
```
Pubkey: RSA, ELG, DSA, ECDH, ECDSA, EDDSA
Cipher: IDEA, 3DES, CAST5, BLOWFISH, AES, AES192, AES256, TWOFISH,
        CAMELLIA128, CAMELLIA192, CAMELLIA256
Hash: SHA1, RIPEMD160, SHA256, SHA384, SHA512, SHA224
Compression: Uncompressed, ZIP, ZLIB, BZIP2
```

We assume messages are sent in the blind: `--include-key-block` will be the default, to enable offline decryption. [OpenPGP-Options.html](https://www.gnupg.org/documentation/manuals/gnupg/OpenPGP-Options.html)

### time fields
`:BTC_TIME:` - a Bitcoin block height in the "time chain".

`:BTC:` - a Bitcoin block height in the "time chain".

`:UNIX_TIME_SECONDS:` - UTC Time in seconds

`:UNIX_TIME_MILLIS:` - UTC Time in milliseconds

`:TIME:` - UTC Time in milliseconds

##### Example - ping time chain format
`:GPGR:GPGS:BTC_TIME:`

##### Example - ping UTC time format
`:GPGR:GPGS:UNIX_TIME_SECONDS:`

##### Example - ping full format (seconds)
`:GPGR:GPGS:BTC_TIME:UNIX_TIME_SECONDS:`

##### Example - ping full format (milliseconds)
`:GPGR:GPGS:BTC_TIME:UNIX_TIME_MILLIS:`

##### Example - ping abridged format (milliseconds) - abridged `:TIME:` is in millisoeconds
`:GPGR:GPGS:BTC:TIME:`

### time functions

`:NETWORK_MODULUS:`

##### variables:
genesis_time = 1231006505 (1/3/2009, 1:15:05 PM)

millis = current UNIX time in milliseconds (example: 1646634471416)

bitcoin\_network\_age = (millis - genesis\_time)

NETWORK\_MODULUS = (millis - genesis\_time) % BTC_TIME

```
NETWORK_MODULUS = bitcoin_network_age % BTC_TIME
or
NETWORK_MODULUS = (millis - genesis_time) % BTC_TIME
```
##### [Helper Functions](./sources/modulus_conversion_formulas.md):

```
n = (millis - genesis_time - NETWORK_MODULUS)/BTC_TIME
nBTC_TIME = (millis - genesis_time - NETWORK_MODULUS)
millis = (genesis_time + nBTC_TIME + NETWORK_MODULUS)
```

---

##### Examples:

```shell
066.2022 01:35:44 AM :NETWORK_MODULUS:516881:
066.2022 01:36:15 AM :NETWORK_MODULUS:548176:
066.2022 01:36:36 AM :NETWORK_MODULUS:569069:
```

---

`:NETWORK_WEEBLE:`

`:NETWORK_WOBBLE:`



---

TODO: more message structure

TODO: file structure

TODO: LOC - location specifications for offline resources

---

