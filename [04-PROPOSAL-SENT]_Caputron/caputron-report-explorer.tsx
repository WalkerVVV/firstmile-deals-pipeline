import React, { useState, useMemo } from 'react';
import { Package, TrendingUp, Truck, MapPin, Weight, Box, BarChart3, Globe } from 'lucide-react';
import { colors, volumeData, carrierData, serviceData, weightData, dimensionsData, topStates } from './constants';
import TabButton from './components/TabButton';
import StatCard from './components/StatCard';
import ProgressBar from './components/ProgressBar';

const CaputronReport = () => {
  const [activeTab, setActiveTab] = useState('overview');

  // Memoize static data to prevent recreation on each render
  const memoizedCarrierData = useMemo(() => carrierData, []);
  const memoizedServiceData = useMemo(() => serviceData, []);
  const memoizedWeightData = useMemo(() => weightData, []);
  const memoizedDimensionsData = useMemo(() => dimensionsData, []);
  const memoizedTopStates = useMemo(() => topStates, []);

  return (
    <div className="min-h-screen" style={{ backgroundColor: colors.fmOffWhite }}>
      {/* Header */}
      <div style={{ backgroundColor: colors.fmNavy }}>
        <div className="max-w-7xl mx-auto px-4 py-6">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-4">
              <div className="text-3xl font-bold" style={{ color: colors.fmGreen }}>
                FirstMile
              </div>
              <div className="text-gray-400">|</div>
              <h1 className="text-2xl font-semibold text-white">
                Caputron Shipping Analysis
              </h1>
            </div>
            <div className="text-sm" style={{ color: colors.fmOffWhite }}>
              <p>Prepared for: <span className="font-semibold">Robin Azzam, CEO</span></p>
              <p>Analysis Date: June 30, 2025</p>
            </div>
          </div>
        </div>
      </div>

      {/* Navigation */}
      <div style={{ backgroundColor: colors.fmNavy + '15' }} className="border-b">
        <div className="max-w-7xl mx-auto px-4 py-3">
          <div className="flex space-x-2 overflow-x-auto">
            <TabButton id="overview" label="Overview" icon={BarChart3} activeTab={activeTab} setActiveTab={setActiveTab} />
            <TabButton id="carriers" label="Carriers" icon={Truck} activeTab={activeTab} setActiveTab={setActiveTab} />
            <TabButton id="weight" label="Weight Analysis" icon={Weight} activeTab={activeTab} setActiveTab={setActiveTab} />
            <TabButton id="dimensions" label="Dimensions" icon={Box} activeTab={activeTab} setActiveTab={setActiveTab} />
            <TabButton id="geography" label="Geography" icon={MapPin} activeTab={activeTab} setActiveTab={setActiveTab} />
          </div>
        </div>
      </div>

      {/* Content */}
      <div className="max-w-7xl mx-auto px-4 py-8">
        {activeTab === 'overview' && (
          <div className="space-y-8">
            <div className="bg-white rounded-lg p-6 shadow-sm">
              <h2 className="text-xl font-semibold mb-4" style={{ color: colors.fmNavy }}>
                Executive Summary
              </h2>
              <p className="leading-relaxed" style={{ color: colors.fmGray500 }}>
                Analysis of shipping patterns reveals a dual-carrier operation with 
                strong emphasis on ground services. Based on current volume of 1,000 daily shipments, 
                the profile is characterized by lightweight packages, standardized dimensions, 
                and nationwide coverage with minimal international presence.
              </p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              <StatCard
                icon={Package}
                label="Daily Volume"
                value="1,000"
                subvalue="500-1,000 range"
                color={colors.fmGreen}
              />
              <StatCard
                icon={TrendingUp}
                label="Monthly Volume"
                value="30,000"
                subvalue="avg per month"
                color={colors.fmSky}
              />
              <StatCard
                icon={Globe}
                label="Annual Projection"
                value="365,000"
                subvalue="shipments/year"
                color={colors.fmGreenShade}
              />
            </div>

            <div className="bg-white rounded-lg p-6 shadow-sm">
              <h3 className="text-lg font-semibold mb-4" style={{ color: colors.fmNavy }}>Quick Insights</h3>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div className="flex items-center space-x-3">
                  <div className="w-3 h-3 rounded-full" style={{ backgroundColor: colors.success }}></div>
                  <span style={{ color: colors.fmGray900 }}>730 daily shipments under 1 pound (73%)</span>
                </div>
                <div className="flex items-center space-x-3">
                  <div className="w-3 h-3 rounded-full" style={{ backgroundColor: colors.fmGreen }}></div>
                  <span style={{ color: colors.fmGray900 }}>97% ground services, 3% expedited</span>
                </div>
                <div className="flex items-center space-x-3">
                  <div className="w-3 h-3 rounded-full" style={{ backgroundColor: colors.fmSky }}></div>
                  <span style={{ color: colors.fmGray900 }}>All 50 states + UK coverage</span>
                </div>
                <div className="flex items-center space-x-3">
                  <div className="w-3 h-3 rounded-full" style={{ backgroundColor: colors.fmMint }}></div>
                  <span style={{ color: colors.fmGray900 }}>Standard 5"×8"×8" packaging</span>
                </div>
              </div>
            </div>
          </div>
        )}

        {activeTab === 'carriers' && (
          <div className="space-y-8">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div className="bg-white rounded-lg p-6 shadow-sm">
                <h3 className="text-lg font-semibold mb-6" style={{ color: colors.fmNavy }}>Carrier Utilization</h3>
                {memoizedCarrierData.map(carrier => (
                  <ProgressBar
                    key={carrier.name}
                    label={`${carrier.name} - ${carrier.count} shipments/day`}
                    percentage={carrier.percentage}
                    color={carrier.color}
                  />
                ))}
              </div>

              <div className="bg-white rounded-lg p-6 shadow-sm">
                <h3 className="text-lg font-semibold mb-6" style={{ color: colors.fmNavy }}>Carrier Split Visual</h3>
                <div className="relative h-64 flex items-center justify-center">
                  <div className="relative w-48 h-48">
                    <div 
                      className="absolute inset-0 rounded-full"
                      style={{ backgroundColor: memoizedCarrierData[0].color }}
                    />
                    <div 
                      className="absolute inset-0 rounded-full"
                      style={{
                        background: `conic-gradient(${memoizedCarrierData[1].color} 0deg, ${memoizedCarrierData[1].color} ${memoizedCarrierData[1].percentage * 3.6}deg, transparent ${memoizedCarrierData[1].percentage * 3.6}deg)`
                      }}
                    />
                    <div className="absolute inset-4 bg-white rounded-full flex items-center justify-center">
                      <div className="text-center">
                        <p className="text-2xl font-bold" style={{ color: colors.dark }}>1,000</p>
                        <p className="text-sm text-gray-600">Daily Shipments</p>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <div className="bg-white rounded-lg p-6 shadow-sm">
              <h3 className="text-lg font-semibold mb-6" style={{ color: colors.fmNavy }}>Service Method Distribution</h3>
              <div className="space-y-4">
                {memoizedServiceData.map(service => (
                  <div key={service.name} className="flex items-center justify-between py-3 border-b last:border-0">
                    <div>
                      <p className="font-medium text-gray-800">{service.name}</p>
                      <p className="text-sm text-gray-600">{service.count} shipments/day</p>
                    </div>
                    <div className="text-right">
                      <p className="text-2xl font-bold" style={{ color: colors.fmGreen }}>
                        {service.percentage}%
                      </p>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}

        {activeTab === 'weight' && (
          <div className="space-y-8">
            <div className="bg-white rounded-lg p-6 shadow-sm">
              <h3 className="text-lg font-semibold mb-6">Weight Distribution Analysis</h3>
              <div className="space-y-6">
                {memoizedWeightData.map((item, index) => {
                  const isUnder1lb = index < 3;
                  return (
                    <div key={item.range} className="relative">
                      <div className="flex justify-between items-center mb-2">
                        <span className={`font-medium ${isUnder1lb ? 'text-green-700' : 'text-gray-700'}`}>
                          {item.range}
                        </span>
                        <span className="text-sm text-gray-600">
                          {item.count} shipments/day ({item.percentage}%)
                        </span>
                      </div>
                      <div className="w-full bg-gray-200 rounded-full h-8">
                        <div 
                          className="h-8 rounded-full flex items-center justify-end pr-2 transition-all duration-500"
                          style={{ 
                            width: `${item.percentage}%`,
                            backgroundColor: isUnder1lb ? colors.success : colors.fmSky
                          }}
                        >
                          <span className="text-xs text-white font-medium">{item.percentage}%</span>
                        </div>
                      </div>
                    </div>
                  );
                })}
              </div>
              
              <div className="mt-8 p-4 rounded-lg" style={{ backgroundColor: `${colors.success}10` }}>
                <p className="text-lg font-semibold" style={{ color: colors.success }}>
                  Key Finding: 73% Under 1 Pound
                </p>
                <p className="text-sm mt-1" style={{ color: colors.fmGray900 }}>
                  The majority of shipments fall within the lightweight category, 
                  with the 11-15.99 oz range representing the highest concentration at 45%.
                </p>
              </div>
            </div>
          </div>
        )}

        {activeTab === 'dimensions' && (
          <div className="space-y-8">
            <div className="bg-white rounded-lg p-6 shadow-sm">
              <h3 className="text-lg font-semibold mb-6">Top 5 Package Dimensions</h3>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                {memoizedDimensionsData.map((dim, index) => (
                  <div 
                    key={index}
                    className="border-2 rounded-lg p-4 hover:shadow-md transition-all"
                    style={{ 
                      borderColor: index === 0 ? colors.fmGreen : '#e5e7eb',
                      backgroundColor: index === 0 ? `${colors.fmGreen}05` : 'white'
                    }}
                  >
                    <div className="flex items-center justify-between mb-2">
                      <span className="text-2xl font-bold" style={{ color: colors.fmGreen }}>
                        #{index + 1}
                      </span>
                      <Box size={24} color={colors.fmSky} />
                    </div>
                    <p className="text-lg font-semibold" style={{ color: colors.fmNavy }}>{dim}</p>
                    {index === 0 && (
                      <p className="text-sm mt-1" style={{ color: colors.fmGray500 }}>Most Common</p>
                    )}
                  </div>
                ))}
              </div>
              
              <div className="mt-6 p-4 bg-gray-50 rounded-lg">
                <p className="text-sm text-gray-700">
                  <span className="font-semibold">Note:</span> Consistent package dimensions 
                  suggest standardized packaging practices, which can lead to operational 
                  efficiencies and cost optimization opportunities.
                </p>
              </div>
            </div>
          </div>
        )}

        {activeTab === 'geography' && (
          <div className="space-y-8">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div className="bg-white rounded-lg p-6 shadow-sm">
                <h3 className="text-lg font-semibold mb-6">Top 10 Destination States</h3>
                <div className="space-y-3">
                  {memoizedTopStates.map((state, index) => (
                    <div 
                      key={index}
                      className="flex items-center justify-between py-2 px-3 rounded-lg hover:bg-gray-50"
                    >
                      <div className="flex items-center space-x-3">
                        <div 
                          className="w-8 h-8 rounded-full flex items-center justify-center text-white font-bold"
                          style={{ 
                            backgroundColor: index < 3 ? colors.fmGreen : colors.fmSky
                          }}
                        >
                          {index + 1}
                        </div>
                        <span className="font-medium" style={{ color: colors.fmNavy }}>{state}</span>
                      </div>
                      <MapPin size={18} color={colors.fmMint} />
                    </div>
                  ))}
                </div>
              </div>

              <div className="bg-white rounded-lg p-6 shadow-sm">
                <h3 className="text-lg font-semibold mb-6">Geographic Coverage</h3>
                <div className="space-y-6">
                  <div className="p-4 rounded-lg" style={{ backgroundColor: `${colors.fmGreen}10` }}>
                    <div className="flex items-center justify-between mb-2">
                      <h4 className="font-semibold" style={{ color: colors.fmNavy }}>Domestic Coverage</h4>
                      <span className="text-2xl font-bold" style={{ color: colors.fmGreen }}>
                        100%
                      </span>
                    </div>
                    <p className="text-sm" style={{ color: colors.fmGray500 }}>All 50 states served</p>
                  </div>
                  
                  <div className="p-4 rounded-lg" style={{ backgroundColor: `${colors.fmMint}10` }}>
                    <div className="flex items-center justify-between mb-2">
                      <h4 className="font-semibold" style={{ color: colors.fmNavy }}>International Presence</h4>
                      <Globe size={24} color={colors.fmMint} />
                    </div>
                    <p className="text-sm" style={{ color: colors.fmGray500 }}>United Kingdom</p>
                    <p className="text-xs mt-1" style={{ color: colors.fmGray500 }}>Tower Hamlets, London</p>
                  </div>

                  <div className="border-t pt-4">
                    <h4 className="font-semibold mb-3" style={{ color: colors.fmNavy }}>Service Level Summary</h4>
                    <div className="grid grid-cols-2 gap-4">
                      <div className="text-center p-3 rounded-lg" style={{ backgroundColor: colors.fmOffWhite }}>
                        <p className="text-3xl font-bold" style={{ color: colors.fmGreen }}>97%</p>
                        <p className="text-sm" style={{ color: colors.fmGray500 }}>Ground Services</p>
                      </div>
                      <div className="text-center p-3 rounded-lg" style={{ backgroundColor: colors.fmOffWhite }}>
                        <p className="text-3xl font-bold" style={{ color: colors.fmSky }}>3%</p>
                        <p className="text-sm" style={{ color: colors.fmGray500 }}>Expedited</p>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
      
      {/* Footer */}
      <div className="bg-white border-t mt-12">
        <div className="max-w-7xl mx-auto px-4 py-6">
          <div className="text-center text-sm">
            <p className="font-semibold" style={{ color: colors.fmGreen }}>FirstMile</p>
            <p style={{ color: colors.fmGray500 }}>Shipping Intelligence Report • Current Volume: 1,000 daily shipments</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default CaputronReport;