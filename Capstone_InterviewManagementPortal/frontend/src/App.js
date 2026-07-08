import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import MainLayout from './components/Layout/MainLayout';
import Login from './pages/Login';
import ResetPassword from './pages/ResetPassword';
import Dashboard from './pages/Dashboard';
import Users from './pages/Users';
import CreateUser from './pages/CreateUser';
import EditUser from './pages/EditUser';
import Jobs from './pages/Jobs';               
import CreateJob from './pages/CreateJob';     
import EditJob from './pages/EditJob';       
import JobDetails from './pages/JobDetails';   
import ChangePassword from './pages/ChangePassword'; 
import Candidates from './pages/Candidates';
import CreateCandidate from './pages/CreateCandidate';
import EditCandidate from './pages/EditCandidate';
import CandidateDetails from './pages/CandidateDetails';

const ProtectedRoute = ({ children }) => {
  const token = localStorage.getItem('access_token');
  if (!token) {
    return <Navigate to="/login" replace />;
  }
  return children;
};

function App() {
  return (
    <Router>
      <Routes>
      
        <Route path="/login" element={<Login />} />
        <Route path="/reset-password" element={<ResetPassword />} />

        
        <Route path="/" element={
          <ProtectedRoute>
            <MainLayout><Dashboard /></MainLayout>
          </ProtectedRoute>
        } />
        <Route path="/dashboard" element={
          <ProtectedRoute>
            <MainLayout><Dashboard /></MainLayout>
          </ProtectedRoute>
        } />

        <Route path="/users" element={
          <ProtectedRoute>
            <MainLayout><Users /></MainLayout>
          </ProtectedRoute>
        } />
        <Route path="/users/create" element={
          <ProtectedRoute>
            <MainLayout><CreateUser /></MainLayout>
          </ProtectedRoute>
        } />
        <Route path="/users/edit/:id" element={
          <ProtectedRoute>
            <MainLayout><EditUser /></MainLayout>
          </ProtectedRoute>
        } />

     
        <Route path="/jobs" element={
          <ProtectedRoute>
            <MainLayout><Jobs /></MainLayout>
          </ProtectedRoute>
        } />
        <Route path="/jobs/create" element={
          <ProtectedRoute>
            <MainLayout><CreateJob /></MainLayout>
          </ProtectedRoute>
        } />
        <Route path="/jobs/edit/:id" element={
          <ProtectedRoute>
            <MainLayout><EditJob /></MainLayout>
          </ProtectedRoute>
        } />
        <Route path="/jobs/:id" element={
          <ProtectedRoute>
            <MainLayout><JobDetails /></MainLayout>
          </ProtectedRoute>
        } />

        
        <Route path="/change-password" element={
          <ProtectedRoute>
            <MainLayout><ChangePassword /></MainLayout>
          </ProtectedRoute>
        } />
        <Route path="/candidates" element={
  <ProtectedRoute>
    <MainLayout><Candidates /></MainLayout>
  </ProtectedRoute>
} />
<Route path="/candidates/create" element={
  <ProtectedRoute>
    <MainLayout><CreateCandidate /></MainLayout>
  </ProtectedRoute>
} />
<Route path="/candidates/edit/:id" element={
  <ProtectedRoute>
    <MainLayout><EditCandidate /></MainLayout>
  </ProtectedRoute>
} />
<Route path="/candidates/:id" element={
  <ProtectedRoute>
    <MainLayout><CandidateDetails /></MainLayout>
  </ProtectedRoute>
} />

     
        <Route path="*" element={
          <ProtectedRoute>
            <MainLayout><h2>Page Not Found</h2></MainLayout>
          </ProtectedRoute>
        } />
      </Routes>
    </Router>
    
  );
}

export default App;