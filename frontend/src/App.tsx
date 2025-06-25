import React, { useState } from 'react';
import Container from '@mui/material/Container';
import Stepper from '@mui/material/Stepper';
import Step from '@mui/material/Step';
import StepLabel from '@mui/material/StepLabel';
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import ModelSelector from './components/ModelSelector';
import AppContextForm from './components/AppContextForm';
import TestPlanForm from './components/TestPlanForm';
import TestPlanReview from './components/TestPlanReview';

const steps = [
  'Select Model',
  'Set App Context',
  'Generate Test Plan',
  'Review & Download Scripts',
];

function App() {
  const [activeStep, setActiveStep] = useState(0);
  const [model, setModel] = useState<string | null>(null);
  const [appContext, setAppContext] = useState<any>(null);
  const [testPlan, setTestPlan] = useState<any>(null);

  return (
    <Container maxWidth="md" sx={{ py: 4 }}>
      <Typography variant="h4" align="center" gutterBottom>
        AI-Powered Selenium Test Generator
      </Typography>
      <Stepper activeStep={activeStep} sx={{ mb: 4 }}>
        {steps.map((label) => (
          <Step key={label}>
            <StepLabel>{label}</StepLabel>
          </Step>
        ))}
      </Stepper>
      <Box>
        {activeStep === 0 && (
          <ModelSelector
            onNext={(selected) => {
              setModel(selected);
              setActiveStep(1);
            }}
            selectedModel={model}
          />
        )}
        {activeStep === 1 && (
          <AppContextForm
            onNext={(context) => {
              setAppContext(context);
              setActiveStep(2);
            }}
            initialContext={appContext}
          />
        )}
        {activeStep === 2 && (
          <TestPlanForm
            model={model}
            appContext={appContext}
            onNext={(plan) => {
              setTestPlan(plan);
              setActiveStep(3);
            }}
          />
        )}
        {activeStep === 3 && (
          <TestPlanReview
            testPlan={testPlan}
            onBack={() => setActiveStep(2)}
          />
        )}
      </Box>
    </Container>
  );
}

export default App;
