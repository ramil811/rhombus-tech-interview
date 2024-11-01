import React, { useState } from 'react';
import axios from './helper/axios';
import { File, Upload } from '@phosphor-icons/react';
import dayjs from 'dayjs';

const App = () => {
    const [file, setFile] = useState(null);
    const [message, setMessage] = useState('');
    const [error, setError] = useState(false);
    const [uploaded, setUploaded] = useState(false);
    const [processedData, setProcessedData] = useState(null);
    const [dataTypes, setDataTypes] = useState(null);
    const [dataHeading, setDataHeading] = useState([]);
    const [dataRows, setDataRows] = useState([]);

    const handleFileChange = (e) => {
      setMessage('');
      setError(false);
      setUploaded(false);
      setFile(e.target.files[0]);
    }

    const uploadFile = async () => {
      if (!file) {
        setMessage('Please select a file to upload');
        setError(true);
      } else {
        const formData = new FormData();
        formData.append('file', file);
        try {
          const response = await axios.post('/data/upload/', formData, {
            headers: {
              'Content-Type': 'multipart/form-data'
            }
          });
          // console.log(response);
          const fileData = response?.data?.processed_data;
          setProcessedData({...fileData});
          setDataTypes(response?.data?.data_types);
          setMessage('File uploaded successfully');
          setUploaded(true);
          setError(false);
        } catch (error) {
          // console.log(error);
          setMessage(error?.response?.data?.message || 'File upload failed');
          setError(true);
        }
      }
    }

    return (
        <div className="bg-neutral-900 min-h-100 text-white px-20 flex items-center justify-center">
          <div className="w-full flex flex-col justify-center align-center">
            <div id="header" className="mb-10 w-100 flex justify-center">
              <h1 className="font-semibold text-4xl">Infer Data Types</h1>
            </div>
            <div className="w-100 flex justify-center mb-10">
              <div id="file-input" className="w-2/4 py-10 px-20 flex flex-col items-center border border-white rounded-lg cursor-pointer" onClick={(e) => document.getElementById('file-input-field').click()}>
                {file ? <>
                    <File size={32} color="#e6e6e6" weight="fill" /> <br/> {file.name}
                  </>
                :
                  <>
                    <Upload size={32} color="#e6e6e6" weight="fill" /> <br/> Choose File to Upload
                  </>
                }
              </div>
            </div>
            <input id="file-input-field" className='hidden' type="file" onChange={handleFileChange} />
            <div className="w-100 flex justify-center mb-10">
              <button onClick={uploadFile} className="border border-white px-10 py-5 rounded-md">Upload</button>
            </div>
            <div id="alerts" className='w-100 flex justify-center'>
              {message && 
                <div id="message" className={`${error ? 'bg-rose-700' : 'bg-green-500' } py-4 w-2/4 flex justify-center`}>
                  {message}
                </div>
              }
            </div>
            {(uploaded === true && Object.keys(processedData).length > 0) && <>
              <div id="processed-data" className="w-100 flex justify-center mt-10">
                {/* use grid to show data */}
                {Object.keys(processedData).map((key, index) => (
                  <div id="column" key={`header-${index}`} >
                    <div className="border border-white px-5 py-2 text-center">{key} <br/> ({dataTypes[index]})</div>
                    {Object.values(processedData[key]).map((value, row_index) => (
                      <div key={`data-${row_index}`} className="border border-white px-5 py-2 text-center">
                        {dataTypes[index] === 'DateTime' ? dayjs(value).format('DD/MM/YYYY') : value.toString()}
                      </div>
                    ))}
                  </div>
                ))}
              </div>
            </>}
          </div>
        </div>
    )
}

export default App;