import os
import glob
from datetime import datetime
import pandas as pd

path = '/home/knn/Desktop/Goc.Store'

files = glob.iglob(path + '/**/*.*', recursive=True)
# df = pd.DataFrame(columns=['dirname', 'basename', 'create_date', 'modified_date'])
data = []
for f_ in files:

    if f_.find("node_modules") != -1 or f_.find(".git") != -1:
        pass
    else:

        temp = {"dirname": os.path.dirname(f_),
                'basename': os.path.basename(f_),
                'create_date': datetime.fromtimestamp(os.path.getctime(f_)),
                'modified_date': datetime.fromtimestamp(os.path.getmtime(f_)),
                'size': os.path.getsize(f_)}

        data.append(temp)

df = pd.DataFrame.from_dict(data)
df.modified_date.max().strftime('%Y-%m-%d %H:%M:%S')