import React from 'react';
import { StatCardProps } from '../types';
import { colors } from '../constants';

const StatCard: React.FC<StatCardProps> = ({ 
  icon: Icon, 
  label, 
  value, 
  subvalue, 
  color = colors.fmGreen 
}) => (
  <div className="bg-white rounded-lg p-6 shadow-sm hover:shadow-md transition-shadow">
    <div className="flex items-start justify-between">
      <div>
        <p className="text-sm mb-1" style={{ color: colors.fmGray500 }}>{label}</p>
        <p className="text-2xl font-bold" style={{ color }}>{value}</p>
        {subvalue && <p className="text-sm mt-1" style={{ color: colors.fmGray500 }}>{subvalue}</p>}
      </div>
      <div className="p-3 rounded-lg" style={{ backgroundColor: `${color}20` }}>
        <Icon size={24} style={{ color }} />
      </div>
    </div>
  </div>
);

export default StatCard;