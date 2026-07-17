import { useState } from 'react';
import { Button, Typography, Stack, Alert } from '@mui/material';
import uploadApi from '../api/uploadApi';

export default function FileUploader() {
  const [file, setFile] = useState(null);
  const [message, setMessage] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleUpload = async () => {
    if (!file) {
      setError('Please choose a file first.');
      return;
    }

    try {
      setLoading(true);
      setError('');
      setMessage('');
      const response = await uploadApi.upload(file);
      setMessage(response?.data?.message || 'Upload successful');
    } catch (err) {
      setError(err?.response?.data?.detail || err?.message || 'Upload failed');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Stack spacing={2}>
      <input type="file" onChange={(e) => setFile(e.target.files?.[0] || null)} />
      <Button variant="contained" onClick={handleUpload} disabled={loading}>
        {loading ? 'Uploading...' : 'Upload Document'}
      </Button>
      {message && <Alert severity="success">{message}</Alert>}
      {error && <Alert severity="error">{error}</Alert>}
      <Typography variant="body2" color="text.secondary">
        Supported formats: PDF, DOCX, TXT
      </Typography>
    </Stack>
  );
}
