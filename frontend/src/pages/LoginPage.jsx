import { Box, Button, Paper, TextField, Typography } from '@mui/material';

export default function LoginPage() {
  return (
    <Box sx={{ display: 'flex', justifyContent: 'center', mt: 6 }}>
      <Paper sx={{ p: 4, width: 420 }}>
        <Typography variant="h5" sx={{ mb: 3 }}>Login</Typography>
        <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
          <TextField label="Email" variant="outlined" />
          <TextField label="Password" type="password" variant="outlined" />
          <Button variant="contained">Sign In</Button>
        </Box>
      </Paper>
    </Box>
  );
}
