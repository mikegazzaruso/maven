import React, { useState, useEffect } from 'react';
import { Container, CssBaseline, IconButton, Box, useMediaQuery } from '@mui/material';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import Brightness4Icon from '@mui/icons-material/Brightness4';
import Brightness7Icon from '@mui/icons-material/Brightness7';
import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import VideoForm from './components/VideoForm';
import VideoResult from './components/VideoResult';
import * as api from './api';

function App() {
  const prefersDarkMode = useMediaQuery('(prefers-color-scheme: dark)');
  const [mode, setMode] = useState(prefersDarkMode ? 'dark' : 'light');
  const [isLoading, setIsLoading] = useState(false);
  const [taskId, setTaskId] = useState(null);
  const [status, setStatus] = useState(null);
  const [error, setError] = useState(null);
  const [currentStep, setCurrentStep] = useState('');
  const [progress, setProgress] = useState(0);

  const theme = React.useMemo(
    () =>
      createTheme({
        palette: {
          mode,
          primary: {
            main: '#1976d2',
          },
          secondary: {
            main: '#dc004e',
          },
        },
      }),
    [mode],
  );

  const toggleColorMode = () => {
    setMode((prevMode) => (prevMode === 'light' ? 'dark' : 'light'));
  };

  useEffect(() => {
    let intervalId;

    if (taskId && status !== 'completed' && status !== 'failed') {
      intervalId = setInterval(async () => {
        try {
          const response = await api.checkStatus(taskId);
          setStatus(response.status);
          setCurrentStep(response.current_step || '');
          setProgress(response.progress || 0);
          if (response.error) {
            setError(response.error);
          }
        } catch (err) {
          console.error('Error checking status:', err);
          toast.error('Error checking video status');
        }
      }, 2000); // Poll every 2 seconds
    }

    return () => {
      if (intervalId) {
        clearInterval(intervalId);
      }
    };
  }, [taskId, status]);

  const handleSubmit = async (formData) => {
    setIsLoading(true);
    setError(null);
    setProgress(0);
    setCurrentStep('');
    try {
      const response = await api.generateVideo(formData);
      setTaskId(response.task_id);
      setStatus('queued');
      toast.info('Video generation started');
    } catch (err) {
      console.error('Error generating video:', err);
      toast.error('Error starting video generation');
      setError(err.message);
    } finally {
      setIsLoading(false);
    }
  };

  const handleDownload = async () => {
    try {
      const blob = await api.downloadVideo(taskId);
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `video_${taskId}.mp4`;
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
      document.body.removeChild(a);
      toast.success('Video downloaded successfully');
    } catch (err) {
      console.error('Error downloading video:', err);
      toast.error('Error downloading video');
    }
  };

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Box sx={{ minHeight: '100vh', bgcolor: 'background.default' }}>
        <Container>
          <Box sx={{ display: 'flex', justifyContent: 'flex-end', pt: 2 }}>
            <IconButton onClick={toggleColorMode} color="inherit">
              {mode === 'dark' ? <Brightness7Icon /> : <Brightness4Icon />}
            </IconButton>
          </Box>
          <VideoForm onSubmit={handleSubmit} isLoading={isLoading} />
          {taskId && (
            <VideoResult
              taskId={taskId}
              status={status}
              error={error}
              currentStep={currentStep}
              progress={progress}
              onDownload={handleDownload}
            />
          )}
          <ToastContainer 
            position="bottom-right"
            theme={mode}
          />
        </Container>
      </Box>
    </ThemeProvider>
  );
}

export default App;
