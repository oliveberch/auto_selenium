import React, { useState } from 'react';
import api from '../api';
import Box from '@mui/material/Box';
import Button from '@mui/material/Button';
import TextField from '@mui/material/TextField';
import Typography from '@mui/material/Typography';
import CircularProgress from '@mui/material/CircularProgress';

interface TestPlanFormProps {
  model: string | null;
  appContext: any;
  onNext: (plan: any) => void;
}

const TestPlanForm: React.FC<TestPlanFormProps> = ({ model, appContext, onNext }) => {
  const [requirements, setRequirements] = useState('');
  const [codebase, setCodebase] = useState<File | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    try {
      const formData = new FormData();
      if (codebase) formData.append('codebase', codebase);
      formData.append('requirements', requirements);
      if (model) formData.append('model_id', model);
      const res = await api.post('/test-plan/generate', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });
      onNext(res.data);
    } catch (err: any) {
      setError(err?.response?.data?.detail || 'Failed to generate test plan.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Box component="form" onSubmit={handleSubmit}>
      <Typography variant="h6" gutterBottom>Generate Test Plan</Typography>
      <TextField
        label="Requirements (optional)"
        value={requirements}
        onChange={e => setRequirements(e.target.value)}
        fullWidth
        multiline
        minRows={3}
        sx={{ mb: 2 }}
      />
      <Button
        variant="contained"
        component="label"
        sx={{ mb: 2 }}
      >
        Upload Codebase (zip)
        <input
          type="file"
          accept=".zip"
          hidden
          onChange={e => setCodebase(e.target.files?.[0] || null)}
        />
      </Button>
      {codebase && <Typography variant="body2">Selected: {codebase.name}</Typography>}
      {error && <Typography color="error" sx={{ mt: 2 }}>{error}</Typography>}
      <Box sx={{ mt: 2 }}>
        <Button type="submit" variant="contained" disabled={loading || !codebase}>
          {loading ? <CircularProgress size={24} /> : 'Generate Test Plan'}
        </Button>
      </Box>
    </Box>
  );
};

export default TestPlanForm; 