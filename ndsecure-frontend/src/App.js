import React from 'react';
import { BrowserRouter as Router, Route, Routes, Link } from 'react-router-dom';
import { Navbar, Nav, Container } from 'react-bootstrap';
import HackerLayout from './components/HackerLayout';
import CreateNote from './components/CreateNote';
import ViewNote from './components/ViewNote';
import Register from './components/Register';
import Login from './components/Login';
import Dashboard from './components/Dashboard';
import { getCurrentUser, logout } from './services/auth';
import 'bootstrap/dist/css/bootstrap.min.css';
import './styles/HackerTheme.css';

function App() {
  const currentUser = getCurrentUser();

  const handleLogout = () => {
    logout();
    window.location.reload();
  };

  return (
    <Router>
      <HackerLayout>
        <Navbar bg="dark" variant="dark" expand="lg" className="mb-4">
          <Container>
            <Navbar.Brand as={Link} to="/" className="hacker-text">NDSecure</Navbar.Brand>
            <Navbar.Toggle aria-controls="basic-navbar-nav" />
            <Navbar.Collapse id="basic-navbar-nav">
              <Nav className="ml-auto">
                {currentUser ? (
                  <>
                    <Nav.Link as={Link} to="/dashboard" className="hacker-text">Dashboard</Nav.Link>
                    <Nav.Link as={Link} to="/create" className="hacker-text">Create Note</Nav.Link>
                    <Nav.Link onClick={handleLogout} className="hacker-text">Logout</Nav.Link>
                  </>
                ) : (
                  <>
                    <Nav.Link as={Link} to="/login" className="hacker-text">Login</Nav.Link>
                    <Nav.Link as={Link} to="/register" className="hacker-text">Register</Nav.Link>
                  </>
                )}
              </Nav>
            </Navbar.Collapse>
          </Container>
        </Navbar>

        <Container>
          <Routes>
            <Route path="/" element={currentUser ? <Dashboard /> : <Login />} />
            <Route path="/create" element={<CreateNote />} />
            <Route path="/view/:id" element={<ViewNote />} />
            <Route path="/register" element={<Register />} />
            <Route path="/login" element={<Login />} />
            <Route path="/dashboard" element={<Dashboard />} />
          </Routes>
        </Container>
      </HackerLayout>
    </Router>
  );
}

export default App;