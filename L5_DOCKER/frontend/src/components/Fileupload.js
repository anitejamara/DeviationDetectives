import React, { useState } from 'react';
import axios from 'axios';
import { Container, Form, Button, Alert } from 'react-bootstrap';

const FileUpload = () => {
    const [file,setFile]= useState(null)
    const handleFileInputChange =(event)=>{
        console.log(event.target)
        setFile(event.target.files[0])

    }
    const handleSubmit = async (event) => {
        event.preventDefault();
        const formData = new FormData();
        formData.append('file_upload', file);  // 'file' should be your File object

        try {
          const response = await fetch('http://127.0.0.1:8000/analyze_contract', {
            method: 'POST',
            body: formData,
          });

          if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
          }

          const data = await response.json();
          console.log(data);
        //   ! ADD CODE TO HANDLE ALL THE ERRORS FROM THE BACKEND(NOT PDF, EMPTY PDF etc)
        } catch (error) {
          console.error('Error:', error);
        }
      };
    const fetch_trial = async(event) => {
        const endpoint='http://127.0.0.1:8000/analyze_contract';
        const response = await fetch(endpoint,
            {
                method:"GET",
                // mode: "cors",
                // body:'abc',
            }
        );
        console.log(await response.text())
    }

    return (
        <Container>
            <h2 className="my-4">File Upload</h2>
            <Form>
                <Form.Group controlId="formFile" className="mb-3">
                    <Form.Label>Choose a file</Form.Label>
                    <Form.Control type="file" onChange={handleFileInputChange} />
                </Form.Group>
            </Form>
            <Button variant="primary" onClick={handleSubmit}>Upload</Button>
            <Button variant="primary" onClick={fetch_trial}>Testing</Button>

            {/* {message && <Alert className="mt-4" variant={message.includes('error') ? 'danger' : 'success'}>{message}</Alert>} */}
        </Container>
    );
};

export default FileUpload;