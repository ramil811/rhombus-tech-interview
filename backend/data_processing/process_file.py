import pandas as pd

def process_file(file_path):
    data = None

    if file_path.endswith('.csv'):
        data = pd.read_csv(file_path)
    elif file_path.endswith('.xlsx'):
        data = pd.read_excel(file_path)

    print("==== Data before type inference ====")
    print(data.dtypes)
    print("====================================")

    # for each column infer the data type
    for col in data.columns:
        # Attempt to convert to numeric first
        # return integer if possible, otherwise float
        if col != 'Score':
            continue
        print(data[col])
        try:
            data_converted = pd.to_numeric(data[col], errors='coerce')
            print(data[col].apply(lambda x: isinstance(x, int)).any())
            print(data_converted.isna().any())
            # if data_converted[col].isna().any() or data_converted[col].apply(lambda x: x.isinstance(x, float)).any():
            #     data_converted[col] = data_converted[col].astype(float)
            # else:
            #     data_converted[col] = data_converted[col].astype(int)
            print(data_converted)
        except ValueError as e:
            print(e)
            pass
        print("====================================")

    print("==== Data after type inference ====")
    print(data.dtypes)
        

process_file('sample_data.csv')
