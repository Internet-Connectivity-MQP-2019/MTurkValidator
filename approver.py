import sys
import jwt
import pandas as pd

secret = sys.argv[1]
infilename = sys.argv[2]
outfilename = infilename.split(".")[0] + "_processed.csv"

def check_token(token):
    try:
        result = jwt.decode(token, secret, algorithms=['HS256'])
        if result["count"] >= 150:
            return (True, None)
        else:
            return (False, "Invalid number of datapoints")
    except jwt.exceptions.InvalidSignatureError:
        return (False, "Invalid token")

df = pd.read_csv(infilename)
df["Approve"] = df["Approve"].astype(str)
df["Reject"] = df["Reject"].astype(str)

for i, row in df.iterrows():
    passed, failure_reason = check_token(row["Answer.token"])

    if passed:
        df.at[i, "Approve"] = "x"
        df.at[i, "Reject"] = ""
    else:
        df.at[i, "Approve"] = ""
        df.at[i, "Reject"] = failure_reason

df.to_csv(outfilename)
