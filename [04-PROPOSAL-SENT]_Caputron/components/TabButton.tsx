import React from 'react';
import { TabButtonProps } from '../types';
import { colors } from '../constants';

const TabButton: React.FC<TabButtonProps> = ({ id, label, icon: Icon, activeTab, setActiveTab }) => (
  <button
    onClick={() => setActiveTab(id)}
    className={`flex items-center space-x-2 px-4 py-2 rounded-lg transition-all ${
      activeTab === id
        ? 'text-white shadow-md'
        : 'text-gray-600 hover:text-white hover:bg-opacity-20 hover:bg-white'
    }`}
    style={{ 
      backgroundColor: activeTab === id ? colors.fmGreen : 'transparent',
      color: activeTab === id ? 'white' : colors.fmGray500
    }}
  >
    <Icon size={18} />
    <span className="font-medium">{label}</span>
  </button>
);

export default TabButton;