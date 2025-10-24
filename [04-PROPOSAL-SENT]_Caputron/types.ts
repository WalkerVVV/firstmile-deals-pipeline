export interface VolumeData {
  daily: number;
  monthly: number;
  annual: number;
}

export interface CarrierInfo {
  name: string;
  count: number;
  percentage: number;
  color: string;
}

export interface ServiceInfo {
  name: string;
  count: number;
  percentage: number;
}

export interface WeightInfo {
  range: string;
  percentage: number;
  count: number;
}

export interface TabButtonProps {
  id: string;
  label: string;
  icon: React.ComponentType<{ size?: number }>;
  activeTab: string;
  setActiveTab: (tab: string) => void;
}

export interface StatCardProps {
  icon: React.ComponentType<{ size?: number; style?: React.CSSProperties }>;
  label: string;
  value: string;
  subvalue?: string;
  color?: string;
}

export interface ProgressBarProps {
  percentage: number;
  color?: string;
  label: string;
}