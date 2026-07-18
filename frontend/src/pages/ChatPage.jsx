import { useMemo, useState } from 'react';
import { Button, TextField, Box, Stack, CircularProgress, Typography, MenuItem, Paper } from '@mui/material';
import ChatWindow from '../components/ChatWindow';
import CitationCard from '../components/CitationCard';
import useChat from '../hooks/useChat';
import { useChatContext } from '../context/ChatContext';
import feedbackApi from '../api/feedbackApi';

export default function ChatPage() {
  const [question, setQuestion] = useState('');
  const [rating, setRating] = useState(5);
  const [comments, setComments] = useState('');
  const [feedbackMessage, setFeedbackMessage] = useState('');
  const { sessionId } = useChatContext();
  const { messages, loading, error, sendMessage } = useChat(sessionId);

  const latestAssistantMessage = useMemo(
    () => [...messages].reverse().find((m) => m.role === 'assistant'),
    [messages],
  );
  const latestUserQuestion = useMemo(
    () => [...messages].reverse().find((m) => m.role === 'user'),
    [messages],
  );

  const onSend = async () => {
    if (!question.trim()) return;
    await sendMessage(question);
    setQuestion('');
  };

  const onFeedbackSubmit = async () => {
    if (!latestAssistantMessage || !latestUserQuestion) {
      setFeedbackMessage('Ask a question and wait for the assistant response before submitting feedback.');
      return;
    }

    try {
      await feedbackApi.submit({
        query: latestUserQuestion.content,
        response: latestAssistantMessage.content,
        rating,
        comments,
      });
      setFeedbackMessage('Feedback saved to PostgreSQL.');
      setComments('');
    } catch (err) {
      setFeedbackMessage(err?.response?.data?.detail || err?.message || 'Unable to save feedback.');
    }
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

      <Paper sx={{ p: 2 }}>
        <Typography variant="h6" sx={{ mb: 1 }}>Feedback</Typography>
        <Stack spacing={1.5}>
          <TextField
            select
            label="Rating"
            value={rating}
            onChange={(e) => setRating(Number(e.target.value))}
          >
            {[1, 2, 3, 4, 5].map((value) => (
              <MenuItem key={value} value={value}>
                {value}
              </MenuItem>
            ))}
          </TextField>
          <TextField
            label="Comments"
            multiline
            minRows={3}
            value={comments}
            onChange={(e) => setComments(e.target.value)}
          />
          <Button variant="outlined" onClick={onFeedbackSubmit}>
            Save feedback
          </Button>
          {feedbackMessage && <Typography color="text.secondary">{feedbackMessage}</Typography>}
        </Stack>
      </Paper>
    </Stack>
  );
}
