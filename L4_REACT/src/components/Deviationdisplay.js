import React from 'react';
import { Card, Col, Row } from 'react-bootstrap';

const Deviationdisplay = ({ data }) => {
  if (!data || Object.keys(data).length === 0) {
    return (
      <div>
        <Card className='clauseDisplay'>
          <Card.Body>
            <div className="expense-card">
              <div className="expense-details">
                <p>No Data Available</p>
              </div>
            </div>
          </Card.Body>
        </Card>
      </div>
    );
  }

  // Extract additions, subtractions, and potential_modifications from data
  const { additions, subtractions, potential_modifications } = data;

  return (
    <Row>
              {potential_modifications && potential_modifications.length > 0 && (
        <Col >
              <h2>Modifications</h2>
          <Card className='clauseDisplay'>
            <Card.Body>
              {potential_modifications.map((item, index) => (
                <div key={index} className="expense-card">
                  <div className="expense-details">
                    <p><strong>{item[0]}</strong></p>
                    <p>{item[1]}</p>
                    <p>{item[2]}</p>
                  </div>
                </div>
              ))}
            </Card.Body>
          </Card>
        </Col>
      )}
      {additions && additions.length > 0 && (
        <Col >
              <h2>Additions</h2>
          <Card className='clauseDisplay'>
            <Card.Body>
              {additions.map((item, index) => (
                <div key={index} className="expense-card">
                  <div className="expense-details">
                    <p><strong>{item[0]}</strong></p>
                    <p>{item[1]}</p>
                  </div>
                </div>
              ))}
            </Card.Body>
          </Card>
        </Col>
      )}

      {subtractions && subtractions.length > 0 && (
        <Col >
              <h2>Removed</h2>
          <Card className='clauseDisplay'>
            <Card.Body>
              {subtractions.map((item, index) => (
                <div key={index} className="expense-card">
                  <div className="expense-details">
                    <p><strong>{item[0]}</strong></p>
                    <p>{item[1]}</p>
                  </div>
                </div>
              ))}
            </Card.Body>
          </Card>
        </Col>
      )}


    </Row>
  );
};

export default Deviationdisplay;
