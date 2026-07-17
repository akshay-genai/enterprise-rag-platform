import { Drawer, List, ListItemButton, ListItemText, Toolbar } from '@mui/material';
import { Link } from 'react-router-dom';

const items = [
  { label: 'Dashboard', to: '/' },
  { label: 'Chat Interface', to: '/chat' },
  { label: 'Upload Documents', to: '/upload' },
  { label: 'Admin Page', to: '/admin' },
];

export default function Sidebar() {
  return (
    <Drawer
      variant="permanent"
      sx={{
        width: 250,
        flexShrink: 0,
        '& .MuiDrawer-paper': { width: 250, boxSizing: 'border-box' },
      }}
    >
      <Toolbar />
      <List>
        {items.map((item) => (
          <ListItemButton key={item.to} component={Link} to={item.to}>
            <ListItemText primary={item.label} />
          </ListItemButton>
        ))}
      </List>
    </Drawer>
  );
}
