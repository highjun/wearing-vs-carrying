from util import *

cur = os.path.splitext(os.path.basename(__file__))[0]

df = load_bout()
users = set(df["users"])
df["is_small"] = [1 if step< 120 else 0 for step in df["step"]]
for idx, user in enumerate(users):
    user_df = df.query(f"users == '{user}'")
    user_df = user_df.groupby(["bout_type","is_small"]).agg(step = ("step","sum"))
    user_df /= np.sum(user_df.values)
    user_df.reset_index(inplace = True)
    # if np.sum(user_df.query("bout_type == 'w'")["step"]) > 0.2:
    print(user)
    print(user_df)
    print("-"*30)   