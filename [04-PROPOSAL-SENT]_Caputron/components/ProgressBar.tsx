import React from 'react';
import { ProgressBarProps } from '../types';
import { colors } from '../constants';

const ProgressBar: React.FC<ProgressBarProps> = ({ 
  percentage, 
  color = colors.fmGreen, 
  label 
}) => (
  <div className="mb-4">
    <div className="flex justify-between mb-1">
      <span className="text-sm font-medium" style={{ color: colors.fmGray900 }}>{label}</span>
      <span className="text-sm font-medium" style={{ color }}>{percentage}%</span>
    </div>
    <div className="w-full bg-gray-200 rounded-full h-2.5">
      <div 
        className="h-2.5 rounded-full transition-all duration-500"
        style={{ width: `${percentage}%`, backgroundColor: color }}
      />
    </div>
  </div>
);

export default ProgressBar;