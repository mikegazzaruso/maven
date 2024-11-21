import React from 'react';
import {
  Box,
  Typography,
  Button,
  LinearProgress,
  Paper,
  CircularProgress,
} from '@mui/material';
import { styled } from '@mui/material/styles';

const StyledPaper = styled(Paper)(({ theme }) => ({
  padding: theme.spacing(3),
  marginTop: theme.spacing(3),
  backgroundColor: theme.palette.background.paper,
}));

const StatusBox = styled(Box)(({ theme }) => ({
  marginTop: theme.spacing(2),
  marginBottom: theme.spacing(2),
}));

const VideoResult = ({ taskId, status, error, onDownload, currentStep, progress }) => {
  const isCompleted = status === 'completed';
  const isFailed = status === 'failed';
  const isProcessing = status === 'processing';

  const getStatusColor = () => {
    if (isCompleted) return 'success.main';
    if (isFailed) return 'error.main';
    return 'primary.main';
  };

  const getStatusMessage = () => {
    if (isCompleted) return 'Video generation completed!';
    if (isFailed) return 'Video generation failed';
    if (isProcessing) return currentStep || 'Processing...';
    return 'Starting video generation...';
  };

  return (
    <StyledPaper elevation={3}>
      <StatusBox>
        <Typography variant="h6" color={getStatusColor()} gutterBottom>
          {getStatusMessage()}
        </Typography>
        
        {isProcessing && (
          <Box sx={{ width: '100%', mt: 2 }}>
            <LinearProgress 
              variant="determinate" 
              value={progress} 
              sx={{ height: 10, borderRadius: 5 }}
            />
            <Typography variant="body2" color="text.secondary" align="right" sx={{ mt: 1 }}>
              {Math.round(progress)}%
            </Typography>
          </Box>
        )}

        {!isCompleted && !isFailed && (
          <Box display="flex" alignItems="center" gap={1} sx={{ mt: 2 }}>
            <CircularProgress size={20} />
            <Typography variant="body2" color="text.secondary">
              Please wait while we generate your video...
            </Typography>
          </Box>
        )}

        {error && (
          <Typography color="error" sx={{ mt: 2 }}>
            Error: {error}
          </Typography>
        )}
      </StatusBox>

      {isCompleted && (
        <Button
          variant="contained"
          color="primary"
          onClick={onDownload}
          fullWidth
        >
          Download Video
        </Button>
      )}
      <Typography variant="body2" color="text.secondary" sx={{ mt: 2 }}>
        Task ID: {taskId}
      </Typography>
    </StyledPaper>
  );
};

export default VideoResult;
