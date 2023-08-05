# LogicPlum Module
LogicPlum is a client library for working with the LogicPlum platform API.


Example
------------
```
>>> import pandas as pd
>>> from logicplum import LogicPlum
>>>
>>> deployment_id = "DEPLOYMENT_ID"
>>> df = pd.read_csv("datatopredict.csv")
>>>
>>> lp = LogicPlum("YOUR-API-KEY")
>>>
>>> score = lp.score(deployment_id, df)
>>> score
```
