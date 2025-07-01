import React from 'react';
import { 
  Box, 
  Paper, 
  Typography, 
  Table, 
  TableBody, 
  TableCell, 
  TableContainer, 
  TableHead, 
  TableRow 
} from '@mui/material';

/**
 * PayoffMatrix Component - Displays a game theory payoff matrix
 * 
 * @param {Object} props
 * @param {Array} props.payoffMatrix - 2D array of payoff tuples [(p1, p2), ...]
 * @param {Array} props.pureNash - Array of pure Nash equilibria coordinates [(row, col), ...]
 * @param {boolean} props.editable - Whether the matrix is editable
 * @param {function} props.onCellChange - Callback for when a cell is edited
 */
const PayoffMatrix = ({ 
  payoffMatrix = [], 
  pureNash = [], 
  editable = false,
  onCellChange = null
}) => {
  if (!payoffMatrix || payoffMatrix.length === 0) {
    return (
      <Box sx={{ textAlign: 'center', p: 2 }}>
        <Typography variant="body1">No payoff matrix available</Typography>
      </Box>
    );
  }

  const rows = payoffMatrix.length;
  const cols = payoffMatrix[0].length;

  // Check if coordinate is a Nash equilibrium
  const isNash = (rowIndex, colIndex) => {
    return pureNash.some(coord => coord[0] === rowIndex && coord[1] === colIndex);
  };

  // Generate column headers (B1, B2, ...)
  const colHeaders = Array.from({ length: cols }, (_, i) => `B${i + 1}`);
  
  // Generate row headers (A1, A2, ...)
  const rowHeaders = Array.from({ length: rows }, (_, i) => `A${i + 1}`);

  // Handle cell value change
  const handleCellChange = (rowIndex, colIndex, player, value) => {
    if (onCellChange && editable) {
      const newValue = parseInt(value, 10) || 0;
      const currentCell = [...payoffMatrix[rowIndex][colIndex]];
      
      if (player === 1) {
        currentCell[0] = newValue;
      } else {
        currentCell[1] = newValue;
      }
      
      onCellChange(rowIndex, colIndex, currentCell);
    }
  };

  return (
    <TableContainer component={Paper} sx={{ overflow: 'auto', maxWidth: '100%' }}>
      <Table size="medium" aria-label="payoff matrix">
        <TableHead>
          <TableRow>
            <TableCell />
            {colHeaders.map((header, index) => (
              <TableCell key={index} align="center" sx={{ fontWeight: 'bold', width: '80px' }}>
                {header}
              </TableCell>
            ))}
          </TableRow>
        </TableHead>
        <TableBody>
          {payoffMatrix.map((row, rowIndex) => (
            <TableRow key={rowIndex}>
              <TableCell component="th" scope="row" sx={{ fontWeight: 'bold' }}>
                {rowHeaders[rowIndex]}
              </TableCell>
              {row.map((cell, colIndex) => {
                const nash = isNash(rowIndex, colIndex);
                return (
                  <TableCell 
                    key={colIndex} 
                    align="center" 
                    padding="none"
                    sx={{
                      border: '1px solid #ddd',
                      position: 'relative',
                      backgroundColor: nash ? 'rgba(76, 175, 80, 0.1)' : 'inherit'
                    }}
                  >
                    <Box className="payoff-cell" sx={{ 
                      p: 2, 
                      border: nash ? '2px solid #4caf50' : 'none',
                    }}>
                      <Box className="payoff-value">
                        {editable ? (
                          <>
                            <input
                              type="number"
                              value={cell[0]}
                              onChange={(e) => handleCellChange(rowIndex, colIndex, 1, e.target.value)}
                              style={{ width: '40px', color: '#e53935', fontWeight: 'bold', textAlign: 'center' }}
                            />
                            <input
                              type="number"
                              value={cell[1]}
                              onChange={(e) => handleCellChange(rowIndex, colIndex, 2, e.target.value)}
                              style={{ width: '40px', color: '#1e88e5', fontWeight: 'bold', textAlign: 'center' }}
                            />
                          </>
                        ) : (
                          <>
                            <span className="p1-payoff">{cell[0]}</span>
                            <span className="p2-payoff">{cell[1]}</span>
                          </>
                        )}
                      </Box>
                      {nash && (
                        <Box
                          sx={{
                            position: 'absolute',
                            top: 0,
                            right: 0,
                            backgroundColor: '#4caf50',
                            color: 'white',
                            padding: '2px 4px',
                            fontSize: '0.7rem',
                            borderRadius: '0 0 0 4px'
                          }}
                        >
                          NE
                        </Box>
                      )}
                    </Box>
                  </TableCell>
                );
              })}
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </TableContainer>
  );
};

export default PayoffMatrix;
