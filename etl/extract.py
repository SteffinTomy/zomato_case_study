import os
import glob
import pandas as pd

def extract_all_csvs(base_path):
    all_files = glob.glob(
        os.path.join(base_path, "**", "*.csv"),
        recursive=True
    )

    print(f"Found {len(all_files)} CSV files")

    dataframes = []

    for idx, file in enumerate(all_files, start=1):
        try:
            print(f"Reading file {idx}: {file}")

            df = pd.read_csv(
                file,
                sep="|",
                engine="python"
            )

            df.columns = [c.strip().lower() for c in df.columns]

            df["source_file"] = os.path.basename(file)
            df["source_city"] = os.path.basename(os.path.dirname(file))

            dataframes.append(df)

        except Exception as e:
            print(f"ERROR reading {file}: {e}")

    if not dataframes:
        return pd.DataFrame()

    return pd.concat(dataframes, ignore_index=True)
