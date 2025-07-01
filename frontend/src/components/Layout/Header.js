import React, { useState } from 'react';
import { Link as RouterLink } from 'react-router-dom';
import { 
  AppBar, 
  Box, 
  Toolbar, 
  Typography, 
  Button, 
  IconButton,
  Drawer,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  Container,
  useMediaQuery
} from '@mui/material';
import { useTheme } from '@mui/material/styles';
import MenuIcon from '@mui/icons-material/Menu';
import HomeIcon from '@mui/icons-material/Home';
import AddIcon from '@mui/icons-material/Add';
import AnalyticsIcon from '@mui/icons-material/Analytics';
import SchoolIcon from '@mui/icons-material/School';

const navItems = [
  { text: 'Home', path: '/', icon: <HomeIcon /> },
  { text: 'Create Game', path: '/create', icon: <AddIcon /> },
  { text: 'Tutorial', path: '/tutorial', icon: <SchoolIcon /> }
];

const Header = () => {
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down('md'));
  const [drawerOpen, setDrawerOpen] = useState(false);

  const handleDrawerToggle = () => {
    setDrawerOpen(!drawerOpen);
  };

  const drawer = (
    <Box onClick={handleDrawerToggle} sx={{ textAlign: 'center' }}>
      <Typography variant="h6" sx={{ my: 2 }}>
        Nash Equilibrium Finder
      </Typography>
      <List>
        {navItems.map((item) => (
          <ListItem 
            button 
            component={RouterLink} 
            to={item.path} 
            key={item.text}
          >
            <ListItemIcon>
              {item.icon}
            </ListItemIcon>
            <ListItemText primary={item.text} />
          </ListItem>
        ))}
      </List>
    </Box>
  );

  return (
    <>
      <AppBar position="static">
        <Container maxWidth="xl">
          <Toolbar disableGutters>
            <Typography
              variant="h6"
              component={RouterLink}
              to="/"
              sx={{
                mr: 2,
                display: { xs: 'none', md: 'flex' },
                fontWeight: 700,
                color: 'inherit',
                textDecoration: 'none'
              }}
            >
              Nash Equilibrium Finder
            </Typography>

            {isMobile ? (
              <>
                <IconButton
                  color="inherit"
                  aria-label="open drawer"
                  edge="start"
                  onClick={handleDrawerToggle}
                  sx={{ mr: 2 }}
                >
                  <MenuIcon />
                </IconButton>
                <Typography
                  variant="h6"
                  component="div"
                  sx={{ flexGrow: 1, display: { xs: 'flex', md: 'none' } }}
                >
                  Nash Finder
                </Typography>
              </>
            ) : (
              <>
                <Box sx={{ flexGrow: 1, display: { xs: 'none', md: 'flex' } }}>
                  {navItems.map((item) => (
                    <Button
                      key={item.text}
                      component={RouterLink}
                      to={item.path}
                      sx={{ color: 'white', display: 'block', mx: 1 }}
                      startIcon={item.icon}
                    >
                      {item.text}
                    </Button>
                  ))}
                </Box>
              </>
            )}
          </Toolbar>
        </Container>
      </AppBar>

      <Drawer
        anchor="left"
        open={drawerOpen}
        onClose={handleDrawerToggle}
        ModalProps={{
          keepMounted: true // Better open performance on mobile
        }}
        sx={{
          display: { xs: 'block', md: 'none' },
          '& .MuiDrawer-paper': { boxSizing: 'border-box', width: 240 },
        }}
      >
        {drawer}
      </Drawer>
    </>
  );
};

export default Header;
