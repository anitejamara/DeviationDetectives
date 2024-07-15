import React from 'react';
import { Container } from 'react-bootstrap';
const pdfUrl = '/Intel Trust Authority Service Agreement v1.0.pdf';
const PDFViewer = () => {
    // Assuming the PDF file is in the public directory
   
    console.log(process.env.PUBLIC_URL )
    return (
        <Container>
            <h2 className="my-4">PDF Viewer</h2>
            <div >
                <iframe
                    title="PDF Viewer"
                    src={process.env.PUBLIC_URL + pdfUrl}
                    width="100%"
                    height="100%"
                    type="application/pdf"
                >
                    This browser does not support PDFs. Please download the PDF to view it.
                </iframe>
            </div>
        </Container>
        
    );
};

export default PDFViewer;
