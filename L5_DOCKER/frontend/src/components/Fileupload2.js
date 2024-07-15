import React, { useState } from 'react';
import { Container, Form, Button, Card, Modal } from 'react-bootstrap';

const FileUpload = ({ onFileUpload }) => {
  const [file, setFile] = useState(null);
  const [error, setError] = useState(null);
  const [showErrorModal, setShowErrorModal] = useState(false);
  const [uploadNotification,setUploadNotification]=useState(false)

  const handleFileInputChange = (event) => {
    const selectedFile = event.target.files[0];
    setError(null);

    if (selectedFile) {
      if (selectedFile.type !== 'application/pdf') {
        setError('Invalid file type. Please upload a PDF file.');
        setShowErrorModal(true);
        setFile(null);
      } else if (selectedFile.size === 0) {
        setError('The selected PDF file is empty (0 bytes). Please choose a valid PDF file.');
        setShowErrorModal(true);
        setFile(null);
      } else {
        setFile(selectedFile);
      }
    }
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    if (!file) {
      setError('No file selected. Please choose a PDF file before uploading.');
      setShowErrorModal(true);
      return;
    }


    const formData = new FormData();
    formData.append('file_upload', file);
    setUploadNotification(true)

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

      onFileUpload(data);
    } catch (error) {
      console.error('Error:', error);
      setError('An error occurred while uploading the file. Please try again.');
      setShowErrorModal(true);
    }
  };

  const handleCloseErrorModal = () => setShowErrorModal(false);
  const handleUploadNotification = () => setUploadNotification(false);

  return (
    <>
      <Card className='card' id='form'>
        <Card.Body className='card-body' id='formcard'>
          <Card.Title className='card-title' style={{textAlign:'center'}}>File Upload</Card.Title>
          <Form>
            <Form.Group controlId="formFile" style={{textAlign:'center'}} className="mb-3">
              <Form.Label style={{textAlign:'center'}} >Choose a file</Form.Label>
              <Form.Control type="file" onChange={handleFileInputChange} accept=".pdf" />
            </Form.Group>
            <Button style={{width:'6rem', alignSelf:'center'}} variant="primary" onClick={handleSubmit} disabled={!file}>Upload</Button>
          </Form>
        </Card.Body>
      </Card>

      <Modal show={showErrorModal} onHide={handleCloseErrorModal}>
        <Modal.Header closeButton style={{ backgroundColor: '#f8d7da', color: '#721c24', borderBottom: '1px solid #f5c6cb' }}>
          <Modal.Title>Error</Modal.Title>
        </Modal.Header>
        <Modal.Body style={{ backgroundColor: '#f8d7da', color: '#721c24' }}>
          {error}
        </Modal.Body>
        <Modal.Footer style={{ backgroundColor: '#f8d7da', borderTop: '1px solid #f5c6cb' }}>
          <Button variant="danger" onClick={handleCloseErrorModal}>
            Close
          </Button>
        </Modal.Footer>
      </Modal>
      {<Modal show={uploadNotification} onHide={handleUploadNotification} style={{ color: '#333333' }}>
        <Modal.Header closeButton style={{ color: '#333333',backgroundColor:'#d0cfcfd1' }} >
          <Modal.Title>Successfully Uploaded</Modal.Title>
        </Modal.Header>
        <Modal.Body style={{ color: '#333333',backgroundColor:'#d0cfcfd1' }}>
          Your file has been uploaded!<br></br>
          Please wait while your file is being processed
        </Modal.Body>
        <Modal.Footer style={{ color: '#333333',backgroundColor:'#d0cfcfd1' }} >
          <Button style={{ backgroundColor:'#0D6EFD' }} onClick={handleUploadNotification}>
            Close
          </Button>
        </Modal.Footer>
      </Modal>}
    </>
  );
};

export default FileUpload;