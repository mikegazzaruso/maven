import React, { useState } from 'react';
import {
  Box,
  TextField,
  Select,
  MenuItem,
  FormControl,
  InputLabel,
  Button,
  Paper,
  Typography,
  Slider,
  FormControlLabel,
  Switch,
  Tooltip,
} from '@mui/material';
import InfoIcon from '@mui/icons-material/Info';

const LANGUAGES = [
  { value: "en", label: "English" },
  { value: "it", label: "Italian" },
  { value: "es", label: "Spanish" },
  { value: "fr", label: "French" },
  { value: "de", label: "German" },
];

const TEXT_MODELS = [
  { value: 0, label: "GPT-4" },
  { value: 1, label: "GPT-3.5" },
];

const IMAGE_MODELS = [
  { value: 0, label: "DALL-E 2" },
  { value: 1, label: "DALL-E 3" },
];

const VIDEO_LENGTHS = [
  { value: 0, label: "30 Seconds" },
  { value: 1, label: "1 Minute" },
  { value: 2, label: "4 Minutes" },
];

const VideoForm = ({ onSubmit, isLoading }) => {
  const [formData, setFormData] = useState({
    topic: '',
    num_images: 5,
    language: 'en',
    text_model: 0,
    image_model: 1,
    video_length: 1,
    security_key: '',
    openai_key: '',
    use_web_search: true
  });

  const [securityError, setSecurityError] = useState('');

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));
    if (name === 'security_key') {
      setSecurityError('');
    }
  };

  const handleSliderChange = (name) => (event, value) => {
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  const handleSwitchChange = (e) => {
    const { name, checked } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: checked,
    }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (formData.security_key !== 'mammata9098$$$') {
      setSecurityError('Access denied. Invalid security key.');
      return;
    }
    const formDataWithoutKey = { ...formData };
    delete formDataWithoutKey.security_key;
    onSubmit(formDataWithoutKey);
  };

  return (
    <Paper elevation={3} sx={{ p: 3, maxWidth: 600, mx: 'auto', mt: 4 }}>
      <Typography variant="h5" gutterBottom>
        Generate AI Video
      </Typography>
      <Box component="form" onSubmit={handleSubmit} sx={{ mt: 2 }}>
        <TextField
          fullWidth
          label="Security Key"
          name="security_key"
          type="password"
          value={formData.security_key}
          onChange={handleChange}
          required
          margin="normal"
          error={!!securityError}
          helperText={securityError}
        />

        <TextField
          fullWidth
          label="OpenAI API Key (optional)"
          name="openai_key"
          type="password"
          value={formData.openai_key}
          onChange={handleChange}
          margin="normal"
          helperText="If not provided, the server's API key will be used"
        />

        <Box sx={{ display: 'flex', alignItems: 'center', mt: 2, mb: 1 }}>
          <FormControlLabel
            control={
              <Switch
                name="use_web_search"
                checked={formData.use_web_search}
                onChange={handleSwitchChange}
                color="primary"
              />
            }
            label="Use Web Search"
          />
          <Tooltip title="When enabled, the system will search the web for the latest information about your topic before generating the video. This helps create more up-to-date and factual content." placement="right">
            <InfoIcon color="primary" fontSize="small" sx={{ ml: 1 }} />
          </Tooltip>
        </Box>

        <TextField
          fullWidth
          label="Topic"
          name="topic"
          value={formData.topic}
          onChange={handleChange}
          required
          margin="normal"
        />

        <Typography gutterBottom>Number of Images: {formData.num_images}</Typography>
        <Slider
          value={formData.num_images}
          onChange={handleSliderChange('num_images')}
          min={1}
          max={10}
          step={1}
          marks
          valueLabelDisplay="auto"
          sx={{ mb: 2 }}
        />

        <FormControl fullWidth margin="normal">
          <InputLabel>Language</InputLabel>
          <Select
            name="language"
            value={formData.language}
            onChange={handleChange}
            label="Language"
          >
            {LANGUAGES.map((lang) => (
              <MenuItem key={lang.value} value={lang.value}>
                {lang.label}
              </MenuItem>
            ))}
          </Select>
        </FormControl>

        <FormControl fullWidth margin="normal">
          <InputLabel>Text Model</InputLabel>
          <Select
            name="text_model"
            value={formData.text_model}
            onChange={handleChange}
            label="Text Model"
          >
            {TEXT_MODELS.map((model) => (
              <MenuItem key={model.value} value={model.value}>
                {model.label}
              </MenuItem>
            ))}
          </Select>
        </FormControl>

        <FormControl fullWidth margin="normal">
          <InputLabel>Image Model</InputLabel>
          <Select
            name="image_model"
            value={formData.image_model}
            onChange={handleChange}
            label="Image Model"
          >
            {IMAGE_MODELS.map((model) => (
              <MenuItem key={model.value} value={model.value}>
                {model.label}
              </MenuItem>
            ))}
          </Select>
        </FormControl>

        <FormControl fullWidth margin="normal">
          <InputLabel>Video Length</InputLabel>
          <Select
            name="video_length"
            value={formData.video_length}
            onChange={handleChange}
            label="Video Length"
          >
            {VIDEO_LENGTHS.map((length) => (
              <MenuItem key={length.value} value={length.value}>
                {length.label}
              </MenuItem>
            ))}
          </Select>
        </FormControl>

        <Button
          type="submit"
          variant="contained"
          color="primary"
          fullWidth
          disabled={isLoading}
          sx={{ mt: 3 }}
        >
          {isLoading ? 'Generating...' : 'Generate Video'}
        </Button>
      </Box>
    </Paper>
  );
};

export default VideoForm;
