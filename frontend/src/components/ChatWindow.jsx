import { Box, Typography, Paper, Divider } from '@mui/material';
import MessageBubble from './MessageBubble';

export default function ChatWindow({ messages = [] }) {
  return (
    <Paper sx={{ p: 2, height: 480, overflow: 'auto', bgcolor: '#fff' }}>
      <Typography variant="h6" sx={{ mb: 2 }}>Conversation</Typography>
      <Divider sx={{ mb: 2 }} />
      <Box sx={{ display: 'flex', flexDirection: 'column', gap: 1.5 }}>
        {messages.length === 0 ? (
          <Typography color="text.secondary">No messages yet. Ask a question to begin.</Typography>
        ) : (
          messages.map((message) => <MessageBubble key={message.id} message={message} />)
        )}
      </Box>
    </Paper>
  );
}
