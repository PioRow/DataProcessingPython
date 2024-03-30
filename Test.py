#załączenie dependencji
from  Rowicki_Piotr_PD2 import *
import pandas as pd
import  numpy as np
import sqlite3
import os

database=os.path.join("stackexchange.db")
conn = sqlite3.connect(database)
# sql
sqlRes_2=pd.read_sql_query("""SELECT Posts.Title, RelatedTab.NumLinks
FROM
(
SELECT RelatedPostId AS PostId, COUNT(*) AS NumLinks
FROM PostLinks
GROUP BY RelatedPostId
) AS RelatedTab
JOIN Posts ON RelatedTab.PostId=Posts.Id
WHERE Posts.PostTypeId=1
ORDER BY NumLinks DESC
 """,con=conn)
print(sqlRes_2)
conn.close()