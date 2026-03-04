import pandas as pd
import os

def save(dir_archive, sheets, sheets_names):

    for sheets, sheets_names in zip(sheets, sheets_names):
        
        df = pd.DataFrame(sheets)

        archive = os.path.join(dir_archive, f"{sheets_names}.csv")
        df.to_csv(path_or_buf=archive, sep=";", index=False)


