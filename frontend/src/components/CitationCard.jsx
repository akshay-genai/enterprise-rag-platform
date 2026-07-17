import { Paper, Typography, Stack } from '@mui/material';

export default function CitationCard({ source }) {
  return (
    <Paper sx={{ p: 2, mb: 1 }}>
      <Stack spacing={0.5}>
        <Typography variant="subtitle2">Citation</Typography>
        <Typography variant="body2">Document: {source.document}</Typography>
        <Typography variant="body2">Page: {source.page}</Typography>
      </Stack>
    </Paper>
  );
}
