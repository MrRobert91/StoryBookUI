import React from 'react';
import ReactDOM from 'react-dom/client';
import { BrowserRouter } from 'react-router-dom';
import App from './App';
import './styles/index.css';
import { AuthProvider } from './context/AuthContext';
import { CreditProvider } from './context/CreditContext';

ReactDOM.createRoot(document.getElementById('root') as HTMLElement).render(
  <React.StrictMode>
    <BrowserRouter>
      <AuthProvider>
        <CreditProvider>
          <App />
        </CreditProvider>
      </AuthProvider>
    </BrowserRouter>
  </React.StrictMode>
);
