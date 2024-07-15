import React, { useState, useEffect } from 'react';
import ReactDOM from 'react-dom';
import 'bootstrap/dist/css/bootstrap.min.css';
import './App.css';
import { Button, Card, Container, Col, Row, Modal, Spinner } from 'react-bootstrap';
// import FileUpload from './components/Fileupload2_newui_noerrorhandling_backup';
import FileUpload from './components/Fileupload2';
import PDFViewer from './components/PDFviewer';
import Clausedisplay from './components/Clausedisplay';
import PDFHighlight from './components/PDFHighlight'; // Import the new component
import Deviationdisplay from './components/Deviationdisplay';
// import { Document } from 'react-pdf/renderer'

function App() {
  // const [items, setItems] = useState([]);
  const items = ['Question 1: Highlight the parts (if any) of this contract related to "Document Name" that should be reviewed by a lawyer. Details: The name of the contract Answer: Services Agreement', 'Question 2: Highlight the parts (if any) of this contract related to "Parties" that should be reviewed by a lawyer. Details: The two or more parties who signed the contract Answer: You and Intel are each a “party” (collectively, the “parties”) to the Agreement.']
  const [clauseData, setClauseData] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [uploadedData, setUploadedData] = useState('');
  const [fileName, setFileName] = useState(''); // Add this state for the file name
  // the below react hook is to handle the data received from the first pdf after uploading and then chaning state of UploadedData to be able to send it to claudeDisplay
  const handleFileUpload = async (data) => {
    setUploadedData(data);
    setFileName(data["file"]); // Assuming the file name is included in the uploaded data
    console.log(uploadedData,fileName,uploadedData['file'],uploadedData['predictions']);

  };
  // the below react hook is to handle the data received from the second pdf after uploading and then chaning state of UploadedData2 to be able to send it to claudeDisplay
  const [uploadedData2, setUploadedData2] = useState('');
  const handleFileUpload2 = async (data) => {
    setUploadedData(data);
    setFileName(data["file"]); // Assuming the file name is included in the uploaded data
    console.log(uploadedData2,fileName,uploadedData2['file'],uploadedData2['predictions']);
  };
  const [comparisonResult, setComparisonResult] = useState(false);

  //below function is to be able to take in the Uploadeddata and Uploadeddata2 and then do a post request to the server
  const deviation = async () => {

    try {
      const predictions1 = {
        // Your first set of predictions
        // For example:
        // question1: "answer1",
        // question2: "answer2",
      };

      const predictions2 = {
        // Your second set of predictions
        // For example:
        // question1: "answer1",
        // question2: "answer2",
      };

      const requestBody = {
        predictions1: uploadedData['predictions'],
        predictions2: uploadedData2['predictions'],
        method: "bert" // or "levenshtein" or "jaccard"
      };

      const response = await fetch('http://127.0.0.1:8000/compare_contracts2', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(requestBody),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const result = await response.json();
      console.log(result);

      // Handle the response data
      if (result.additions && result.subtractions && result.potential_modifications) {
        console.log("Additions:", result.additions);
        console.log("Subtractions:", result.subtractions);
        console.log("Potential Modifications:", result.potential_modifications);
        setComparisonResult(result);
        // Further processing or state updates can be done here
        // For example, updating React state:
        // setComparisonResult(result);
      } else {
        console.error("Unexpected response structure:", result);
      }

    } catch (error) {
      console.error("There was an error sending the request:", error);
    }
  };


  // useEffect(() => {
  //   // Example API call to fetch data
  //   fetch('/api/items')
  //     .then(response => response.json())
  //     .then(data => setItems(data))
  //     .catch(error => console.error('Error fetching data:', error));
  // }, []);
  // const fileUrl = 'C:\Users\ASUS\intelproject\intel\public\Intel Trust Authority Service Agreement v1.0.pdf';

  return (
    <div className="App">
      <Row className="imgBg">
        <Row style={{ margin: '1rem' }}>
        <div className="logo-main">
          <img src="https://upload.wikimedia.org/wikipedia/commons/6/64/Intel-logo-2022.png"/>
        </div>
          <h1>We are Deviation Detectives</h1>
          <h1>Streamline your Contract-reviewing process in just a few clicks!</h1>
        </Row>
        <Row style={{ margin: '1rem' }}>
          <Col>
            <h2>Contract</h2>
            <div >
              <FileUpload onFileUpload={handleFileUpload} />
              {console.log("upload 1 is", uploadedData)}
            </div>
          </Col>
          <Col>
            <h2>Template</h2>
            <div >
              <FileUpload onFileUpload={handleFileUpload2} />
              {console.log("upload 2 is", uploadedData2)}
            </div>
          </Col>
        </Row>
      </Row>

      <Row style={{ margin: '1rem' }}>
        <Modal show={isLoading} centered backdrop="static" keyboard={false}>
          <Modal.Body style={{ textAlign: 'center' }}>
            <Spinner animation="border" role="status" />
            <p style={{ marginTop: '10px' }}>Processing your PDF. This may take a few moments...</p>
          </Modal.Body> 
        </Modal>
        <Col style={{ margin: '1rem', }}>
          <h2>
            Clauses
          </h2>

          <Clausedisplay data={uploadedData['predictions']} />

        </Col>

        <Col style={{ margin: '1rem' }}>
          <h2>
            Clauses
          </h2>

          <Clausedisplay data={uploadedData2['predictions']} />

        </Col>

      </Row>
      <Row style={{ margin: '1rem', display: 'flex', justifyContent: 'center' }}>


        <Button variant="primary" className="btn-primary" style={{ width: '11rem' }} onClick={deviation}>Compare Contracts</Button>
        {comparisonResult && (
          <Row style={{ margin: '1rem' }}>
            {/* <Col>
              <div className='deviation'>
                <h2>Potential Modifications</h2>
                <Clausedisplay data={comparisonResult.potential_modifications} />
              </div>
            </Col>
            <Col>
              <div className='deviation'>
                <h2>Additions</h2>
                <Clausedisplay data={comparisonResult.additions} />
              </div>
            </Col>
            <Col>
              <div className='deviation'>
                <h2>Subtractions</h2>
                <Clausedisplay data={comparisonResult.subtractions} />
              </div>
            </Col> */}
            <Deviationdisplay data={comparisonResult}></Deviationdisplay>
          </Row>
          
         
        )}
      </Row>
     
      {console.log("THE PARTS ARE", uploadedData['file'], uploadedData['predictions'])}
      {/* Add the new PDFHighlight component */}
      {/* {console.log(fileName,comparisonResult.additions,comparisonResult.subtractions,comparisonResult.modifications)} */}
      {comparisonResult && (
        <PDFHighlight
          fileName={uploadedData['file']}
          additions={comparisonResult.additions}
          subtractions={comparisonResult.subtractions}
          modifications={comparisonResult.potential_modifications}
        />
      )}


      {/* <Row>
          <Col   style ={{width:'100%'}}>
          
            <PDFViewer   style ={{width:'100%'}}/>

          </Col>
          <Col   style ={{width:'100%'}}>
          
            <PDFViewer   style ={{width:'100%'}} />

          </Col>

        </Row> */}




    </div>
  );
}

export default App;
