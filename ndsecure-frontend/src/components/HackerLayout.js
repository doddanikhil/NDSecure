import React from 'react';
import { Container } from 'react-bootstrap';
import '../styles/HackerTheme.css';

function HackerLayout({ children }) {
  return (
    <div className="hacker-background">
      <Container className="hacker-container">
        <div className="hacker-terminal">
          <div className="hacker-terminal-header">
            <span className="hacker-terminal-button"></span>
            <span className="hacker-terminal-button"></span>
            <span className="hacker-terminal-button"></span>
          </div>
          <div className="hacker-terminal-body">
            {children}
          </div>
        </div>
      </Container>
    </div>
  );
}

export default HackerLayout;