import Typography from "@mui/material/Typography";
import Toolbar from "@mui/material/Toolbar";
import Container from '@mui/material/Container'
import Button from '@mui/material/Button'
import Box from '@mui/material/Box'
import AppBar from '@mui/material/AppBar'
import IconButton from '@mui/material/IconButton'
import Menu from '@mui/material/Menu'
import MenuItem from '@mui/material/MenuItem';
import ShoppingBasketRoundedIcon from '@mui/icons-material/ShoppingBasketRounded';
import SearchRoundedIcon from '@mui/icons-material/SearchRounded';
import PersonRoundedIcon from '@mui/icons-material/PersonRounded';

import { useState } from "react";

const pages = ['Home', 'Products', 'Blog', 'FAQ', 'Contact Us']
const settings = ['Profile', 'Order', 'Wish List', 'Payments', 'Logout']

export default function Header(props) {
  const [auth, setAuth] = useState(false);
  const [anchorNavMenu, setAnchorNavMenu] = useState(null);
  const [anchorUserMenu, setAnchorUserMenu] = useState(null);

  const authHandler = (event) => {
    setAuth(true)
  }
  const closeNavUserHandler = () => {
    setAnchorUserMenu(null)
  }

  const openNavUserHandler = (event) => {
    setAnchorUserMenu(event.currentTarget)
  }
  const renderUser = (
    <>
      <IconButton
        size="large"
        color="inherit"
        aria-controls="user-account-menu"
        aria-haspopup="true"
        onClick={openNavUserHandler}
      >
        <PersonRoundedIcon />
      </IconButton>
      <Menu
        id="user-account-menu"
        anchorEl={anchorUserMenu}
        anchorOrigin={{
          vertical: 'bottom',
          horizontal: 'right',
        }}
        keepMounted
        transformOrigin={{
          vertical: 'top',
          horizontal: 'right',
        }}
        open={Boolean(anchorUserMenu)}
        onClose={closeNavUserHandler}
      >
        {
          settings.map((setting) => (
            <MenuItem key={setting} >
              <Typography textAlign="center">{setting}</Typography>
            </MenuItem>
          ))
        }
      </Menu >
    </>
  )
  const renderGuest = (
    <Button
      variant="contained"
      onClick={authHandler}
    >
      Login/SignUp
    </Button>
  )

  return (
    <>
      <AppBar position="static" >
        <Container>
          <Toolbar disableGutters>
            <Typography
              variant="h6"
              noWrap
              component="a"
              sx={{
                mr: 2,
                display: { xs: 'none', md: 'flex' },
                fontFamily: 'Inter',
                color: 'inherit',
                textDecoration: 'none',
              }}
            >
              Tech UIT
            </Typography>
            <Box sx={{ flexGrow: 1, display: { xs: 'none', md: 'flex' } }}>
              {pages.map((page) => (
                <Button
                  key={page}
                  sx={{ my: 2, color: 'white', display: 'block' }}
                >
                  {page}
                </Button>
              ))}
            </Box>
            <Box sx={{ flexGrow: 1, display: { xs: 'none', md: 'flex' } }}>
              <IconButton size="large" color="inherit">
                <SearchRoundedIcon />
              </IconButton>
              <IconButton size="large" color="inherit">
                <ShoppingBasketRoundedIcon />
              </IconButton>
              {auth ? renderUser : renderGuest}
            </Box>
          </Toolbar>
        </Container>
      </AppBar>
    </>
  );
}