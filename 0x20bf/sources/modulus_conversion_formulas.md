```
(a - x) mod m = b
(a - x) = (nm + b)
(- x) = ((nm + b) - a)
-1(- x) = -1((nm + b) - a)
(x) = -1((nm + b) - a)
(x) = (-(nm + b) + a)
(x) = (-nm - b) + a)
```

```
(millis - genesis_time) mod BTC_TIME = NETWORK_MODULUS
(millis - genesis_time) = (nBTC_TIME + NETWORK_MODULUS)
(- genesis_time) = ((nBTC_TIME + NETWORK_MODULUS) - millis)
-1(- genesis_time) = -1((nBTC_TIME + NETWORK_MODULUS) - millis)
(genesis_time) = -1((nBTC_TIME + NETWORK_MODULUS) - millis)
(genesis_time) = (-(nBTC_TIME + NETWORK_MODULUS) + millis)
(genesis_time) = (-nBTC_TIME - NETWORK_MODULUS) + millis)
```

```
((genesis_time) + nBTC_TIME + NETWORK_MODULUS) = millis
(millis - (genesis_time) - NETWORK_MODULUS) = nBTC_TIME
(millis - (genesis_time) - NETWORK_MODULUS)/BTC_TIME = n
```
