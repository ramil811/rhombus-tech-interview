import pandas as pd
import threading

lock = threading.Lock()

def process_file(sample_data, data_column_name, column_index, data_types, threaded, data=None):
        # columns that should be strings
        if data_column_name in ['Name', 'First Name', 'Last Name', 'City', 'State', 'Country', 'Address', 'Email', 'Full Name', 'Company', 'Description', 'Title', 'Website']:
            data_types[column_index] = 'String'
            sample_data[data_column_name] = sample_data[data_column_name].astype('string')
            if threaded:
                lock.acquire()
                try:
                    data[data_column_name] = data[data_column_name].astype('string')
                finally:
                    lock.release()
            return 

        # convert to boolean
        # check if the column contains unique 2 values
        if len(sample_data[data_column_name].unique()) == 2:
            sample_data[data_column_name] = sample_data[data_column_name].astype(bool)
            if threaded:
                lock.acquire()
                try:
                    data[data_column_name] = data[data_column_name].astype(bool)
                finally:
                    lock.release()
            data_types[column_index] = 'Boolean'
            return

        # Attempt to convert to numeric
        # return integer if possible, otherwise float
        try:
            # convert all values to numeric, 'NaN' for non-numeric values
            data_converted = sample_data[data_column_name].apply(pd.to_numeric, errors='coerce')
            # fill NaN values with 0
            data_converted = data_converted.fillna(-1)
            # check if all values are -1
            if (data_converted == -1).all():
                pass
            else:
                # check if all values are integers
                if data_converted.apply(lambda x: x.is_integer()).all():
                    data_converted = data_converted.astype(int)
                    data_types[column_index] = 'Integer'
                    sample_data[data_column_name] = data_converted
                    if threaded:
                        lock.acquire()
                        try:
                            data[data_column_name] = data[data_column_name].apply(pd.to_numeric, errors='coerce').fillna(-1).astype(int)
                        finally:
                            lock.release()
                else:
                    data_converted = data_converted.astype(float)
                    sample_data[data_column_name] = data_converted
                    data_types[column_index] = 'Float'
                    if threaded:
                        lock.acquire()
                        try:
                            data[data_column_name] = data[data_column_name].apply(pd.to_numeric, errors='coerce').fillna(-1).astype(float)
                        finally:
                            lock.release()
                return
        except ValueError as e:
            pass

        # Attempt to convert to datetime
        try:
            sample_data[data_column_name] = pd.to_datetime(sample_data[data_column_name])
            if threaded:
                lock.acquire()
                try:
                    data[data_column_name] = pd.to_datetime(data[data_column_name])
                finally:
                    lock.release()
            data_types[column_index] = 'DateTime'
            return
        except (ValueError, TypeError):
            pass

        # attempt to convert to categorical
        try:
            if len(sample_data[data_column_name].unique()) / len(sample_data[data_column_name]) < 1:
                data_converted = pd.Categorical(sample_data[data_column_name])
                sample_data[data_column_name] = data_converted
                if threaded:
                    lock.acquire()
                    try:
                        data[data_column_name] = pd.Categorical(data[data_column_name])
                    finally:
                        lock.release()
                data_types[column_index] = 'Categorical'
                return
        except (ValueError, TypeError):
            pass

        # if all else fails, keep the column as a object
        data_types[column_index] = 'object'
        return
        
def infer_and_convert_data_types(file_path):
    data = None
    if file_path.endswith('.csv'):
        data = pd.read_csv(file_path)
    elif file_path.endswith('.xlsx'):
        data = pd.read_excel(file_path)
    else:
        return None
    
    print("==== Data before type inference ====")
    print(data.dtypes)
    print("====================================")

    # for user-friendly data type names
    data_types = [None] * len(data.columns)

    infer_threads = []

    # check if data is too large to process in one go, then sample the data and process it
    # else process the data in one go
    if (len(data) > 10000):
        sample_data = data.sample(n=100)
        # chunk the data into 6 columns each
        for i in range(0, len(data.columns), 6):
            # create a thread for each column, send a sampled data to the thread for processing
            columns = data.columns[i:i+6]
            for j in range(len(columns)):
                infer_threads.append(threading.Thread(target=process_file, args=(sample_data, columns[j], i+j, data_types, True, data)))
                infer_threads[i+j].start()

        # wait for all threads to finish
        for thread in infer_threads:
            thread.join()
    else:
        for idx, column in enumerate(data.columns):
            process_file(data, column, idx, data_types, False)

    print("==== Data after type inference ====")
    print(data.dtypes)
    print("====================================")
    print("Data types: ", data_types)

    return data.to_dict(), data_types


if __name__ == '__main__':
    infer_and_convert_data_types('sample_data.csv')
