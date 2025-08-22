# import pandas as pd
# import gzip
# import io

# def load_symbol_mapping(path="data/complete.csv.gz"):
#     with gzip.open(path, 'rb') as f:
#         df = pd.read_csv(io.BytesIO(f.read()))
#     return dict(zip(df['symbol'], df['instrument_key']))

import pandas as pd

class SymbolMapper:
    def __init__(self, csv_path):
        print(csv_path)
        self.symbol_df = pd.read_csv(csv_path)

    def get_instrument_key(self, symbol):
        print(symbol)
        # print(self.symbol_df.head())
        instrument = self.symbol_df[self.symbol_df['tradingsymbol'] == symbol]
        print(" ---------- FOUND INSTRUMENT ------------")
        if not instrument.empty:
            return instrument.iloc[0]['instrument_key']
        return None
