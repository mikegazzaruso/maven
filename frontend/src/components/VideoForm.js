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
} from '@mui/material';

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
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  const handleSliderChange = (name) => (event, value) => {
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit(formData);
  };

  return (
    <Paper elevation={3} sx={{ p: 3, maxWidth: 600, mx: 'auto', mt: 4 }}>
      <Typography variant="h5" gutterBottom>
        Generate AI Video
      </Typography>
      <Box component="form" onSubmit={handleSubmit} sx={{ mt: 2 }}>
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
