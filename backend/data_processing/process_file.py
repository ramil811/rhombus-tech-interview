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

    data_types = [None for _ in range(len(data.columns))]

    # for each column infer the data type
    for index, col in enumerate(data.columns):
        # Attempt to convert to numeric first
        # return integer if possible, otherwise float
        try:
            # convert all values to numeric, 'NaN' for non-numeric values
            data_converted = data[col].apply(pd.to_numeric, errors='coerce')
            # fill NaN values with 0
            data_converted = data_converted.fillna(-1)
            # check if all values are -1
            if (data_converted == -1).all():
                pass
            else:
                # check if all values are integers
                if data_converted.apply(lambda x: x.is_integer()).all():
                    data_converted = data_converted.astype(int)
                    data_types[index] = data_converted.dtype
                    data[col] = data_converted
                else:
                    data_converted = data_converted.astype(float)
                    data[col] = data_converted
                    data_types[index] = data_converted.dtype
                continue
        except ValueError as e:
            pass

        # Attempt to convert to datetime
        try:
            data[col] = pd.to_datetime(data[col])
            data_types[index] = data[col].dtype
        except (ValueError, TypeError):
            pass

    print("==== Data after type inference ====")
    print(data.dtypes)
    return data_types
        

process_file('sample_data.csv')
