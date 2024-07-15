import React, { useState } from 'react';
import { Button, Card, Container, Col, Row } from 'react-bootstrap';

const PDFHighlight = ({ fileName, additions, subtractions, modifications }) => {
    console.log("THE DATA WITHIN PDFHIGHLIGHT IS ", fileName, additions, subtractions, modifications);
    const [pdfUrl, setPdfUrl] = useState('');

    const handleHighlight = async () => {
        try {
            const response = await fetch('http://127.0.0.1:8000/highlight_deviations', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    file_name: fileName,
                    additions: additions,
                    subtractions: subtractions,
                    modifications: modifications
                })
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const blob = await response.blob();
            const url = URL.createObjectURL(blob);
            setPdfUrl(url);
        } catch (error) {
            console.error('Error highlighting PDF:', error);
        }
    };

    return (
        <div style={{display:'flex',justifyContent:'center',margin:'20px'}}>
            <Button className='btn-primary' id='pdfhighlight' onClick={handleHighlight}>Highlight Deviations in PDF</Button>
            {pdfUrl && (
                <iframe src={pdfUrl} width="80%" height="600px" title="Highlighted PDF" />
            )}
        </div>
    );
};

export default PDFHighlight;
