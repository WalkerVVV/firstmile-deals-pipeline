// FirstMile official color palette
export const colors = {
  // Brand core
  fmGreen: '#5EC148',
  fmGreenShade: '#4AA63E',
  fmNavy: '#04202F',
  // Accent
  fmMint: '#A3E49C',
  fmSky: '#1B9BE0',
  // Semantic
  success: '#00A651',
  warning: '#FF9A05',
  error: '#E24F4F',
  // Neutrals
  fmOffWhite: '#FAFBF9',
  fmGray500: '#6F767B',
  fmGray900: '#2D3438',
  // Legacy mappings for compatibility
  primary: '#5EC148',
  secondary: '#1B9BE0',
  accent: '#A3E49C',
  dark: '#04202F',
  light: '#FAFBF9'
};

export const volumeData = {
  daily: 1000,
  monthly: 30000,
  annual: 365000
};

export const carrierData = [
  { name: 'UPS', count: 636, percentage: 63.6, color: colors.fmNavy },
  { name: 'USPS', count: 364, percentage: 36.4, color: colors.fmSky }
];

export const serviceData = [
  { name: 'UPS Ground', count: 636, percentage: 63.6 },
  { name: 'USPS Ground Advantage', count: 333, percentage: 33.3 },
  { name: 'USPS Priority Mail', count: 30, percentage: 3.0 },
  { name: 'USPS First Class Mail International', count: 1, percentage: 0.1 }
];

export const weightData = [
  { range: '1-5 oz', percentage: 10, count: 100 },
  { range: '6-10 oz', percentage: 18, count: 180 },
  { range: '11-15.99 oz', percentage: 45, count: 450 },
  { range: '1-5 lbs', percentage: 22, count: 220 },
  { range: '6-10 lbs', percentage: 3, count: 30 },
  { range: '11+ lbs', percentage: 2, count: 20 }
];

export const dimensionsData = [
  '5" × 8" × 8"',
  '3" × 10" × 10"',
  '1" × 6" × 9"',
  '4" × 4" × 6"',
  '5" × 4" × 8"'
];

export const topStates = [
  'Florida (FL)',
  'California (CA)',
  'Texas (TX)',
  'Pennsylvania (PA)',
  'New York (NY)',
  'Ohio (OH)',
  'Illinois (IL)',
  'North Carolina (NC)',
  'Massachusetts (MA)',
  'Michigan (MI)'
];