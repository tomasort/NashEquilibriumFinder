import React from 'react';
import { Box, Container, Typography, Link } from '@mui/material';

const Footer = () => {
  return (
    <Box
      component="footer"
      sx={{
        py: 3,
        px: 2,
        mt: 'auto',
        backgroundColor: (theme) => theme.palette.grey[200]
      }}
    >
      <Container maxWidth="lg">
        <Typography variant="body2" color="text.secondary" align="center">
          © {new Date().getFullYear()} Nash Equilibrium Finder by Tomas Ortega and Pablo Mueller
        </Typography>
        <Typography variant="body2" color="text.secondary" align="center">
          <Link color="inherit" href="https://github.com/username/NashEquilibriumFinder" target="_blank" rel="noopener">
            GitHub
          </Link>{' | '}
          <Link color="inherit" href="/docs" target="_blank">
            Documentation
          </Link>
        </Typography>
      </Container>
    </Box>
  );
};

export default Footer;
