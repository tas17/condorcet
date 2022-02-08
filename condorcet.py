import typer
from pathlib import Path
import pandas as pd


def main(infile: Path):
    if not Path(infile).exists():
        typer.echo(f"File {infile} does not exist", err=True)
        return
    df = pd.read_csv(infile)
    print(df.head(10))

    for c in df.columns:
        if df[c].isnull().values.any():
            print(f"dropping {c}")
            df.drop(c, axis=1,  inplace=True)
    if any(["Unnamed" in e for e in df.columns]):
        print("Unamed is remaining in the columns... parsing went wrong")
    if len(df.columns) == 0:
        print("Dropped every column, stopping programm")
        return
    participants = list(df.columns[1:])
    title = df.columns[0]
    songs = list(df[title])
    
    print(f"Starting condorcet session.\nThere are {len(participants)} participants, which are {sorted(participants)}.\nThere are {len(songs)} {title.lower()}, which are {sorted(songs)}")
    results = {s: 0 for s in songs}
    for i, s_i in enumerate(songs):
        for j, s_j in enumerate(songs):
            if i < j:
                res = duel(df, i, j, title)
                if res == 1:
                    results[s_j] += 1
                if res == -1:
                    results[s_i] += 1
    print(f"Recap of wins: {results}")

def duel(df, a: int, b: int, title):
    p1 = df.iloc[a]
    p1_name = p1[title]
    p2 = df.iloc[b]
    p2_name = p2[title]
    print(f"Duel between {p1_name} and {p2_name}")
    
    cpt_ab = 0
    cpt_ba = 0
    cpt_draw = 0
    for k in list(p1.index)[1:]:
        if p1[k] > p2[k]:
            cpt_ab += 1
        elif p1[k] < p2[k]:
            cpt_ba += 1
        else:
            cpt_draw += 1

    print(f"\t{cpt_ba} in favor of {p1_name}, {cpt_ab} in favor of {p2_name}, {cpt_draw} draws")
    diff = cpt_ab - cpt_ba
    if diff > 0:
        print(f"\t=> {p2_name} wins - with score of {diff}")
        res = 1
    elif diff < 0:
        print(f"\t=> {p1_name} wins - with score of {-diff}")
        res = -1
    else:
        print("\tNo winner here")
        res = 0

    return res

if __name__ == "__main__":
    typer.run(main)
