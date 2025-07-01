import React, { useState } from 'react';
import { 
  Box, 
  Button, 
  FormControl, 
  FormLabel, 
  RadioGroup, 
  Radio, 
  FormControlLabel,
  TextField,
  Card,
  CardContent,
  Typography,
  Grid,
  MenuItem,
  Select,
  InputLabel,
  Slider,
  Stack
} from '@mui/material';

/**
 * GameCreator Component - Form for creating new games
 * 
 * @param {Object} props
 * @param {function} props.onSubmit - Callback for submitting the game
 * @param {boolean} props.loading - Whether the submission is loading
 */
const GameCreator = ({ onSubmit, loading = false }) => {
  const [creationMode, setCreationMode] = useState('template');
  const [templateType, setTemplateType] = useState('prisoners_dilemma');
  const [rows, setRows] = useState(2);
  const [columns, setColumns] = useState(2);
  const [lowerLimit, setLowerLimit] = useState(-5);
  const [upperLimit, setUpperLimit] = useState(5);
  
  // For template parameters (e.g. for Prisoner's Dilemma)
  const [templateParams, setTemplateParams] = useState({
    prisoners_dilemma: { t: 5, r: 3, p: 1, s: 0 },
    battle_of_sexes: { a: 3, b: 2, c: 0 },
    coordination: { a: 5, b: 0, c: 3 },
    // Add parameters for other templates as needed
  });

  // Handler for creation mode change
  const handleModeChange = (event) => {
    setCreationMode(event.target.value);
  };

  // Handler for template type change
  const handleTemplateTypeChange = (event) => {
    setTemplateType(event.target.value);
  };

  // Handler for template parameter change
  const handleTemplateParamChange = (param, value) => {
    setTemplateParams(prevParams => ({
      ...prevParams,
      [templateType]: {
        ...prevParams[templateType],
        [param]: Number(value)
      }
    }));
  };

  // Handler for form submission
  const handleSubmit = (event) => {
    event.preventDefault();
    
    let payload = {};
    
    if (creationMode === 'template') {
      payload = {
        gameType: templateType,
        params: templateParams[templateType]
      };
    } else if (creationMode === 'random') {
      payload = {
        mode: 'r',
        rows,
        columns,
        lowerLimit,
        upperLimit
      };
    }
    
    onSubmit(creationMode, payload);
  };

  return (
    <Card elevation={3}>
      <CardContent>
        <Typography variant="h5" component="h2" gutterBottom>
          Create a New Game
        </Typography>
        
        <Box component="form" onSubmit={handleSubmit} sx={{ mt: 2 }}>
          <FormControl component="fieldset" sx={{ mb: 3 }}>
            <FormLabel component="legend">Creation Method</FormLabel>
            <RadioGroup row value={creationMode} onChange={handleModeChange}>
              <FormControlLabel 
                value="template" 
                control={<Radio />} 
                label="Common Game Template" 
              />
              <FormControlLabel 
                value="random" 
                control={<Radio />} 
                label="Random Game" 
              />
              <FormControlLabel 
                value="custom" 
                control={<Radio />} 
                label="Custom Game" 
                disabled
              />
            </RadioGroup>
          </FormControl>
          
          {creationMode === 'template' && (
            <Box sx={{ mb: 3 }}>
              <FormControl fullWidth sx={{ mb: 2 }}>
                <InputLabel>Game Type</InputLabel>
                <Select
                  value={templateType}
                  label="Game Type"
                  onChange={handleTemplateTypeChange}
                >
                  <MenuItem value="prisoners_dilemma">Prisoner's Dilemma</MenuItem>
                  <MenuItem value="battle_of_sexes">Battle of Sexes</MenuItem>
                  <MenuItem value="coordination">Coordination Game</MenuItem>
                  <MenuItem value="zero_sum">Zero Sum Game</MenuItem>
                </Select>
              </FormControl>
              
              {templateType === 'prisoners_dilemma' && (
                <Grid container spacing={2}>
                  <Grid item xs={6} sm={3}>
                    <TextField
                      label="Temptation (T)"
                      type="number"
                      value={templateParams.prisoners_dilemma.t}
                      onChange={(e) => handleTemplateParamChange('t', e.target.value)}
                      fullWidth
                    />
                  </Grid>
                  <Grid item xs={6} sm={3}>
                    <TextField
                      label="Reward (R)"
                      type="number"
                      value={templateParams.prisoners_dilemma.r}
                      onChange={(e) => handleTemplateParamChange('r', e.target.value)}
                      fullWidth
                    />
                  </Grid>
                  <Grid item xs={6} sm={3}>
                    <TextField
                      label="Punishment (P)"
                      type="number"
                      value={templateParams.prisoners_dilemma.p}
                      onChange={(e) => handleTemplateParamChange('p', e.target.value)}
                      fullWidth
                    />
                  </Grid>
                  <Grid item xs={6} sm={3}>
                    <TextField
                      label="Sucker (S)"
                      type="number"
                      value={templateParams.prisoners_dilemma.s}
                      onChange={(e) => handleTemplateParamChange('s', e.target.value)}
                      fullWidth
                    />
                  </Grid>
                  <Grid item xs={12}>
                    <Typography variant="caption" color="text.secondary">
                      For a valid Prisoner&apos;s Dilemma: T {'>'} R {'>'} P {'>'} S and 2R {'>'} T + S
                    </Typography>
                  </Grid>
                </Grid>
              )}
              
              {templateType === 'battle_of_sexes' && (
                <Grid container spacing={2}>
                  <Grid item xs={12} sm={4}>
                    <TextField
                      label="Parameter A"
                      type="number"
                      value={templateParams.battle_of_sexes.a}
                      onChange={(e) => handleTemplateParamChange('a', e.target.value)}
                      fullWidth
                    />
                  </Grid>
                  <Grid item xs={12} sm={4}>
                    <TextField
                      label="Parameter B"
                      type="number"
                      value={templateParams.battle_of_sexes.b}
                      onChange={(e) => handleTemplateParamChange('b', e.target.value)}
                      fullWidth
                    />
                  </Grid>
                  <Grid item xs={12} sm={4}>
                    <TextField
                      label="Parameter C"
                      type="number"
                      value={templateParams.battle_of_sexes.c}
                      onChange={(e) => handleTemplateParamChange('c', e.target.value)}
                      fullWidth
                    />
                  </Grid>
                  <Grid item xs={12}>
                    <Typography variant="caption" color="text.secondary">
                      For a valid Battle of Sexes: a {'>'} b {'>'} c, typically a = 3, b = 2, c = 0
                    </Typography>
                  </Grid>
                </Grid>
              )}

              {/* Add similar UIs for other template types */}
            </Box>
          )}
          
          {creationMode === 'random' && (
            <Grid container spacing={3}>
              <Grid item xs={12} sm={6}>
                <FormControl fullWidth>
                  <InputLabel>Rows</InputLabel>
                  <Select
                    value={rows}
                    label="Rows"
                    onChange={(e) => setRows(e.target.value)}
                  >
                    {[2, 3, 4, 5].map(val => (
                      <MenuItem key={val} value={val}>{val}</MenuItem>
                    ))}
                  </Select>
                </FormControl>
              </Grid>
              <Grid item xs={12} sm={6}>
                <FormControl fullWidth>
                  <InputLabel>Columns</InputLabel>
                  <Select
                    value={columns}
                    label="Columns"
                    onChange={(e) => setColumns(e.target.value)}
                  >
                    {[2, 3, 4, 5].map(val => (
                      <MenuItem key={val} value={val}>{val}</MenuItem>
                    ))}
                  </Select>
                </FormControl>
              </Grid>
              <Grid item xs={12}>
                <Typography id="payoff-range-slider" gutterBottom>
                  Payoff Range
                </Typography>
                <Stack direction="row" spacing={2} alignItems="center">
                  <TextField
                    label="Min"
                    type="number"
                    value={lowerLimit}
                    onChange={(e) => setLowerLimit(Number(e.target.value))}
                    size="small"
                  />
                  <Slider
                    value={[lowerLimit, upperLimit]}
                    onChange={(e, newValue) => {
                      setLowerLimit(newValue[0]);
                      setUpperLimit(newValue[1]);
                    }}
                    min={-10}
                    max={10}
                    valueLabelDisplay="auto"
                    aria-labelledby="payoff-range-slider"
                  />
                  <TextField
                    label="Max"
                    type="number"
                    value={upperLimit}
                    onChange={(e) => setUpperLimit(Number(e.target.value))}
                    size="small"
                  />
                </Stack>
              </Grid>
            </Grid>
          )}
          
          <Box sx={{ mt: 3, textAlign: 'center' }}>
            <Button 
              type="submit" 
              variant="contained" 
              color="primary" 
              size="large"
              disabled={loading}
            >
              Create Game
            </Button>
          </Box>
        </Box>
      </CardContent>
    </Card>
  );
};

export default GameCreator;
