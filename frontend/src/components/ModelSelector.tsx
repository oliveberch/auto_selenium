import React, { useEffect, useState } from 'react';
import api from '../api';
import Box from '@mui/material/Box';
import Button from '@mui/material/Button';
import FormControl from '@mui/material/FormControl';
import InputLabel from '@mui/material/InputLabel';
import Select from '@mui/material/Select';
import type { SelectChangeEvent } from '@mui/material/Select';
import MenuItem from '@mui/material/MenuItem';
import Typography from '@mui/material/Typography';
import CircularProgress from '@mui/material/CircularProgress';

interface ModelSelectorProps {
  onNext: (model: string) => void;
  selectedModel: string | null;
}

const ModelSelector: React.FC<ModelSelectorProps> = ({ onNext, selectedModel }) => {
  const [models, setModels] = useState<{ name: string; id: string }[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [model, setModel] = useState(selectedModel || '');

  useEffect(() => {
    api.get('/models/')
      .then(res => {
        setModels(res.data.models);
      })
      .catch(err => {
        setError('Failed to load models: ' + (err?.message || 'Unknown error'));
      })
      .finally(() => {
        setLoading(false);
      });
  }, []);

  const handleSelect = (e: SelectChangeEvent) => {
    setModel(e.target.value as string);
  };

  const handleNext = async () => {
    await api.post('/models/select/', { model_id: model });
    onNext(model);
  };

  if (loading) return <CircularProgress />;
  if (error) return <Typography color="error">{error}</Typography>;

  return (
    <Box>
      <Typography variant="h6" gutterBottom>Select AI Model</Typography>
      <FormControl fullWidth sx={{ mb: 2 }}>
        <InputLabel id="model-label">Model</InputLabel>
        <Select
          labelId="model-label"
          value={model}
          label="Model"
          onChange={handleSelect}
        >
          {models.map((m) => (
            <MenuItem key={m.id} value={m.id}>{m.name}</MenuItem>
          ))}
        </Select>
      </FormControl>
      <Button variant="contained" onClick={handleNext} disabled={!model}>
        Next
      </Button>
    </Box>
  );
};

export default ModelSelector; 