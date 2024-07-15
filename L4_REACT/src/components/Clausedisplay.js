import React from 'react';
import { Card } from 'react-bootstrap';

const Clausedisplay = ({ data }) => {
  if (!data) {
    return (
      <div>
      <Card className='clauseDisplay'>
        <Card.Body>
          
            <div className="expense-card">
              <div className="expense-details">
                <p>Upload your contract to view clauses</p>
              </div>
            </div>
          
        </Card.Body>
      </Card>
    </div>
    );
  }
  const items = Object.entries(data);
// css code for scrollable card is in app.css file 
  return (
    <div>
      <Card className='clauseDisplay'>
        <Card.Body>
          {items.map(([question, answer], index) => (
            <div key={index} className="expense-card">
              <div className="expense-details">
                <p><strong>{question}</strong></p>
                <p>{answer}</p>
              </div>
            </div>
          ))}
        </Card.Body>
      </Card>
    </div>
  );
};

export default Clausedisplay;
