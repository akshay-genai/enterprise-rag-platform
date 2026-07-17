import { Typography, Paper, Box } from '@mui/material';
import FileUploader from '../components/FileUploader';

export default function UploadPage() {
  return (
    <Box>
      <Typography variant="h4" sx={{ mb: 3 }}>Upload Documents</Typography>
      <Paper sx={{ p: 3 }}>
        <FileUploader />
      </Paper>
    </Box>
  );
}
