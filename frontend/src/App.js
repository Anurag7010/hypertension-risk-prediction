import React, { useState } from 'react';
import axios from 'axios';
import {
  Container,
  Typography,
  Box,
  TextField,
  Button,
  Paper,
  CircularProgress,
  AppBar,
  Toolbar,
  CssBaseline,
  Grid,
  Alert
} from '@mui/material';

const initialState = {
  male: '',
  age: '',
  currentSmoker: '',
  cigsPerDay: '',
  BPMeds: '',
  diabetes: '',
  totChol: '',
  sysBP: '',
  diaBP: '',
  BMI: '',
  heartRate: '',
  glucose: ''
};

function App() {
  const [form, setForm] = useState(initialState);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const validate = () => {
    for (const key in form) {
      if (form[key] === '' || isNaN(Number(form[key]))) {
        setError('Please fill all fields with valid numbers.');
        return false;
      }
    }
    setError(null);
    return true;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!validate()) return;
    setLoading(true);
    setResult(null);
    setError(null);
    try {
      const payload = Object.fromEntries(
        Object.entries(form).map(([k, v]) => [k, Number(v)])
      );
      const res = await axios.post('http://localhost:5000/predict', payload);
      setResult(res.data.prediction);
    } catch (err) {
      setError('Prediction failed. Please check your backend or input values.');
    } finally {
      setLoading(false);
    }
  };

  const fields = [
    { name: 'male', label: 'Male (1=Yes, 0=No)' },
    { name: 'age', label: 'Age' },
    { name: 'currentSmoker', label: 'Current Smoker (1=Yes, 0=No)' },
    { name: 'cigsPerDay', label: 'Cigarettes Per Day' },
    { name: 'BPMeds', label: 'On BP Medication (1=Yes, 0=No)' },
    { name: 'diabetes', label: 'Diabetes (1=Yes, 0=No)' },
    { name: 'totChol', label: 'Total Cholesterol' },
    { name: 'sysBP', label: 'Systolic BP' },
    { name: 'diaBP', label: 'Diastolic BP' },
    { name: 'BMI', label: 'BMI' },
    { name: 'heartRate', label: 'Heart Rate' },
    { name: 'glucose', label: 'Glucose' }
  ];

  return (
    <>
      <CssBaseline />
      <AppBar position="static" color="primary">
        <Toolbar>
          <Typography variant="h6" sx={{ flexGrow: 1 }}>
            Hypertension Risk Predictor
          </Typography>
        </Toolbar>
      </AppBar>
      <Container maxWidth="sm" sx={{ mt: 4 }}>
        <Paper elevation={4} sx={{ p: 4, mt: 4 }}>
          <Typography variant="h5" align="center" gutterBottom>
            Enter Patient Data
          </Typography>
          <Box component="form" onSubmit={handleSubmit} sx={{ mt: 2 }}>
            <Grid container spacing={2}>
              {fields.map((field) => (
                <Grid item xs={12} sm={6} key={field.name}>
                  <TextField
                    fullWidth
                    label={field.label}
                    name={field.name}
                    value={form[field.name]}
                    onChange={handleChange}
                    variant="outlined"
                    size="small"
                    type="number"
                    inputProps={{ step: 'any' }}
                  />
                </Grid>
              ))}
            </Grid>
            {error && (
              <Alert severity="error" sx={{ mt: 2 }}>{error}</Alert>
            )}
            <Box sx={{ display: 'flex', justifyContent: 'center', mt: 3 }}>
              <Button
                type="submit"
                variant="contained"
                color="primary"
                size="large"
                disabled={loading}
              >
                {loading ? <CircularProgress size={24} color="inherit" /> : 'Predict Risk'}
              </Button>
            </Box>
          </Box>
          {result && (
            <Box sx={{ mt: 4, textAlign: 'center' }}>
              <Alert severity={result === 'High Risk' ? 'error' : 'success'}>
                <Typography variant="h6">
                  Prediction: {result}
                </Typography>
              </Alert>
            </Box>
          )}
        </Paper>
        <Box sx={{ mt: 4, textAlign: 'center', color: 'text.secondary' }}>
          <Typography variant="body2">
            Hypertension Risk Predictor
          </Typography>
        </Box>
      </Container>
    </>
  );
}

export default App;


