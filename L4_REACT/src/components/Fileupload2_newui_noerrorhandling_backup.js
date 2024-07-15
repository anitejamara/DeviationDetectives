import React, { useState } from 'react';
import { Container, Form, Button, Card } from 'react-bootstrap';

const FileUpload = ({ onFileUpload }) => {
  const [file, setFile] = useState(null);

  const handleFileInputChange = (event) => {
    setFile(event.target.files[0]);
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    const formData = new FormData();
    formData.append('file_upload', file);  // 'file' should be your File object

    try {
      console.log("isndie handle submit try")
      const response = await fetch('http://127.0.0.1:8000/analyze_contract', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        console.log("This is the error")
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      console.log("within handle submit try, data is", data);

      // Pass the data to the parent component
      onFileUpload(data);
    } catch (error) {
      console.error('Error:', error);
    }
  };

  const fetch_trial = async () => {
    const endpoint = 'http://127.0.0.1:8000/analyze_contract';
    const response = await fetch(endpoint, {
      method: "GET",
    });
    console.log(await response.text());
  };

  return (
    <Card className='card' id='form'>
      <Card.Body className='card-body'id ='formcard'>
        <Card.Title className='card-title' style={{textAlign:'center'}}>File Upload</Card.Title>
        <Form>
          <Form.Group controlId="formFile" style={{textAlign:'center'}} className="mb-3">
            <Form.Label style={{textAlign:'center'}} >Choose a file</Form.Label>
            <Form.Control type="file" onChange={handleFileInputChange} />
          </Form.Group>
          <Button style ={{width:'6rem', alignSelf:'center'}} variant="primary" onClick={handleSubmit}>Upload</Button>
        </Form>
      </Card.Body>
    </Card>
  );
};

export default FileUpload;
