import { useEffect, useState } from 'react';
import { Card, CardContent, Typography, Grid, Box, CircularProgress } from '@mui/material';
import axios from 'axios';

export default function Dashboard() {
  const [stats, setStats] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    const loadStats = async () => {
      try {
        const response = await axios.get('/dashboard/stats');
        const payload = response.data;

        setStats([
          { title: 'Documents Indexed', value: String(payload.documents_indexed ?? 0) },
          { title: 'Active Sessions', value: String(payload.active_sessions ?? 0) },
          { title: 'LLM Model', value: payload.llm_model ?? 'unknown' },
        ]);
      } catch (err) {
        setError(err?.response?.data?.detail || err?.message || 'Unable to load dashboard statistics.');
      } finally {
        setLoading(false);
      }
    };

    loadStats();
  }, []);

  if (loading) {
    return (
      <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
        <CircularProgress size={20} />
        <Typography>Loading dashboard statistics...</Typography>
      </Box>
    );
  }

  return (
    <Box>
      <Typography variant="h4" sx={{ mb: 3 }}>Dashboard</Typography>
      {error ? (
        <Typography color="error">{error}</Typography>
      ) : (
        <Grid container spacing={3}>
          {stats.map((stat) => (
            <Grid item xs={12} md={4} key={stat.title}>
              <Card>
                <CardContent>
                  <Typography variant="subtitle2" color="text.secondary">
                    {stat.title}
                  </Typography>
                  <Typography variant="h5">{stat.value}</Typography>
                </CardContent>
              </Card>
            </Grid>
          ))}
        </Grid>
      )}
    </Box>
  );
}
