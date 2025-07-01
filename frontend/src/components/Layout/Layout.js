import React from 'react';
import { useLocation } from 'react-router-dom';
import Header from './Header';
import Footer from './Footer';
import { Box, Container } from '@mui/material';

const Layout = ({ children }) => {
  const location = useLocation();
  
  return (
    <Box sx={{ display: 'flex', flexDirection: 'column', minHeight: '100vh' }}>
      <Header />
      <Container component="main" sx={{ 
        flexGrow: 1, 
        py: 4,
        px: { xs: 2, md: 4 }
      }}>
        {children}
      </Container>
      <Footer />
    </Box>
  );
};

export default Layout;
