import React, { useState } from 'react';
import api from '../api';
import Box from '@mui/material/Box';
import Button from '@mui/material/Button';
import Typography from '@mui/material/Typography';
import CircularProgress from '@mui/material/CircularProgress';

interface TestPlanReviewProps {
  testPlan: any;
  onBack: () => void;
}

const TestPlanReview: React.FC<TestPlanReviewProps> = ({ testPlan, onBack }) => {
  const [downloading, setDownloading] = useState(false);

  const handleDownload = async () => {
    setDownloading(true);
    try {
      // Call backend to generate scripts and get zip
      const res = await api.post('/scripts/generate/', {
        user_stories: testPlan.backlog.flatMap((epic: any) => epic.stories),
      }, { responseType: 'blob' });
      // Download the zip file
      const url = window.URL.createObjectURL(new Blob([res.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', 'selenium_scripts.zip');
      document.body.appendChild(link);
      link.click();
      link.parentNode?.removeChild(link);
    } finally {
      setDownloading(false);
    }
  };

  return (
    <Box>
      <Typography variant="h6" gutterBottom>Generated User Stories</Typography>
      {testPlan.backlog.map((epic: any, i: number) => (
        <Box key={i} sx={{ mb: 3 }}>
          <Typography variant="subtitle1"><b>Epic:</b> {epic.epic}</Typography>
          <Typography variant="body2" sx={{ mb: 1 }}>{epic.description}</Typography>
          {epic.stories.map((story: any, j: number) => (
            <Box key={j} sx={{ pl: 2, mb: 1, borderLeft: '2px solid #eee' }}>
              <Typography variant="subtitle2">{story.title}</Typography>
              <Typography variant="body2">{story.description}</Typography>
              <Typography variant="body2" color="text.secondary">Page: {story.page} | URL: {story.url}</Typography>
              <ul>
                {story.acceptance_criteria?.map((ac: string, k: number) => (
                  <li key={k}>{ac}</li>
                ))}
              </ul>
            </Box>
          ))}
        </Box>
      ))}
      <Box sx={{ mt: 2 }}>
        <Button variant="outlined" onClick={onBack} sx={{ mr: 2 }}>
          Back
        </Button>
        <Button variant="contained" onClick={handleDownload} disabled={downloading}>
          {downloading ? <CircularProgress size={24} /> : 'Download Selenium Scripts'}
        </Button>
      </Box>
    </Box>
  );
};

export default TestPlanReview; 