import { Typography, Paper, Box } from '@mui/material';

export default function AdminPage() {
  return (
    <Box>
      <Typography variant="h4" sx={{ mb: 3 }}>Admin Page</Typography>
      <Paper sx={{ p: 3 }}>
        <Typography>Administration and analytics dashboard will appear here.</Typography>
      </Paper>
    </Box>
  );
}
