import React, { useState } from 'react';
import api from '../api';
import Box from '@mui/material/Box';
import Button from '@mui/material/Button';
import TextField from '@mui/material/TextField';
import Typography from '@mui/material/Typography';

interface AppContextFormProps {
  onNext: (context: any) => void;
  initialContext?: any;
}

const AppContextForm: React.FC<AppContextFormProps> = ({ onNext, initialContext }) => {
  const [url, setUrl] = useState(initialContext?.url || '');
  const [pages, setPages] = useState(initialContext?.pages || '');
  const [username, setUsername] = useState(initialContext?.username || '');
  const [password, setPassword] = useState(initialContext?.password || '');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    const context = { url, pages, username, password };
    await api.post('/app-context/', context);
    setLoading(false);
    onNext(context);
  };

  return (
    <Box component="form" onSubmit={handleSubmit}>
      <Typography variant="h6" gutterBottom>Set Application Context</Typography>
      <TextField
        label="App URL"
        value={url}
        onChange={e => setUrl(e.target.value)}
        fullWidth
        required
        sx={{ mb: 2 }}
      />
      <TextField
        label="Pages (comma-separated)"
        value={pages}
        onChange={e => setPages(e.target.value)}
        fullWidth
        required
        sx={{ mb: 2 }}
      />
      <TextField
        label="Username"
        value={username}
        onChange={e => setUsername(e.target.value)}
        fullWidth
        sx={{ mb: 2 }}
      />
      <TextField
        label="Password"
        value={password}
        onChange={e => setPassword(e.target.value)}
        type="password"
        fullWidth
        sx={{ mb: 2 }}
      />
      <Button type="submit" variant="contained" disabled={loading}>
        Next
      </Button>
    </Box>
  );
};

export default AppContextForm; 