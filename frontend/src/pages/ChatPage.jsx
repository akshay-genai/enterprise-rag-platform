import { useState } from 'react';
import { Button, TextField, Box, Stack, CircularProgress, Typography } from '@mui/material';
import ChatWindow from '../components/ChatWindow';
import CitationCard from '../components/CitationCard';
import useChat from '../hooks/useChat';

export default function ChatPage() {
  const [question, setQuestion] = useState('');
  const { messages, loading, error, sendMessage } = useChat();

  const onSend = async () => {
    if (!question.trim()) return;
    await sendMessage(question);
    setQuestion('');
  };

  return (
    <Stack spacing={2}>
      <Typography variant="h4">Chat Interface</Typography>
      <ChatWindow messages={messages} />
      <Box sx={{ display: 'flex', gap: 1 }}>
        <TextField
          fullWidth
          label="Ask a question"
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
        />
        <Button variant="contained" onClick={onSend} disabled={loading}>
          {loading ? <CircularProgress size={20} /> : 'Send'}
        </Button>
      </Box>
      {error && <Typography color="error">{error}</Typography>}
      {messages
        .filter((m) => m.role === 'assistant' && m.sources?.length)
        .map((m) => m.sources.map((source, index) => <CitationCard key={`${m.id}-${index}`} source={source} />))}
    </Stack>
  );
}
