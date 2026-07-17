import { Paper, Typography, Box } from '@mui/material';

export default function MessageBubble({ message }) {
  const isUser = message.role === 'user';

  return (
    <Box sx={{ display: 'flex', justifyContent: isUser ? 'flex-end' : 'flex-start' }}>
      <Paper
        elevation={0}
        sx={{
          p: 1.5,
          maxWidth: '75%',
          bgcolor: isUser ? '#dbeafe' : '#f3f4f6',
          borderRadius: 3,
        }}
      >
        <Typography variant="body2" sx={{ fontWeight: 600, mb: 0.5 }}>
          {isUser ? 'You' : 'Assistant'}
        </Typography>
        <Typography variant="body2">{message.content}</Typography>
      </Paper>
    </Box>
  );
}
