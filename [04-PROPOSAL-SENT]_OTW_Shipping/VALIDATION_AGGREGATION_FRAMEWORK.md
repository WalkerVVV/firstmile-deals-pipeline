# VALIDATION & AGGREGATION FRAMEWORK: Shipping Analysis System

## Overview
This framework ensures data quality, calculation accuracy, and proper aggregation of results from multiple parallel agents.

## 1. VALIDATION FRAMEWORK

### 1.1 Input Validation (Phase 1)

#### Data Quality Checks
```python
class InputValidator:
    def validate_shipping_data(self, df):
        validations = {
            'structure': self.check_structure(df),
            'completeness': self.check_completeness(df),
            'consistency': self.check_consistency(df),
            'business_rules': self.check_business_rules(df)
        }
        return ValidationReport(validations)

    def check_structure(self, df):
        required_columns = ['tracking', 'weight', 'zone', 'service', 'cost']
        return all(col in df.columns for col in required_columns)

    def check_completeness(self, df):
        critical_fields = ['tracking', 'weight', 'zone']
        null_counts = {col: df[col].isnull().sum() for col in critical_fields}
        return all(count == 0 for count in null_counts.values())

    def check_consistency(self, df):
        checks = {
            'weight_range': df['weight'].between(0.01, 150).all(),
            'zone_range': df['zone'].between(1, 8).all(),
            'positive_costs': (df['cost'] > 0).all(),
            'unique_tracking': df['tracking'].duplicated().sum() == 0
        }
        return checks

    def check_business_rules(self, df):
        rules = {
            'express_cost_higher': self.validate_express_premium(df),
            'zone_cost_progression': self.validate_zone_progression(df),
            'weight_cost_correlation': self.validate_weight_correlation(df)
        }
        return rules
```

#### Validation Report Structure
```json
{
    "validation_status": "pass | fail | warning",
    "timestamp": "2024-11-15T10:30:00Z",
    "details": {
        "rows_validated": 10000,
        "issues_found": 15,
        "critical_errors": 0,
        "warnings": 15
    },
    "issues": [
        {
            "severity": "warning",
            "type": "outlier",
            "description": "Weight 175 lbs exceeds normal range",
            "row_numbers": [1234],
            "suggested_action": "verify_or_exclude"
        }
    ]
}
```

### 1.2 Calculation Validation (Phase 2)

#### Rate Calculation Validation
```python
class RateValidator:
    def validate_rates(self, current_costs, xparcel_costs):
        return {
            'range_check': self.check_rate_ranges(current_costs, xparcel_costs),
            'savings_sanity': self.check_savings_reality(current_costs, xparcel_costs),
            'pattern_check': self.check_rate_patterns(current_costs, xparcel_costs)
        }

    def check_rate_ranges(self, current, xparcel):
        # Current costs typically $5-50 for ground
        current_valid = all(5 <= c <= 50 for c in current if c > 0)

        # Xparcel typically $3-30
        xparcel_valid = all(3 <= x <= 30 for x in xparcel if x > 0)

        return current_valid and xparcel_valid

    def check_savings_reality(self, current, xparcel):
        savings_pct = [(c-x)/c*100 for c, x in zip(current, xparcel) if c > 0]

        # Savings should be 20-60% typically, flag if outside 0-70%
        realistic = all(0 <= s <= 70 for s in savings_pct)

        # Average should be 30-50%
        avg_savings = sum(savings_pct) / len(savings_pct)
        avg_realistic = 20 <= avg_savings <= 60

        return realistic and avg_realistic

    def check_rate_patterns(self, current, xparcel):
        # Rates should increase with weight and zone
        # Xparcel should generally be lower than current
        patterns = {
            'xparcel_lower': sum(x < c for x, c in zip(xparcel, current)) / len(current) > 0.8,
            'no_negative': all(x > 0 for x in xparcel) and all(c > 0 for c in current)
        }
        return all(patterns.values())
```

### 1.3 Cross-Agent Validation (Phase 3)

#### Consistency Checks
```python
class CrossAgentValidator:
    def validate_consistency(self, agent_outputs):
        return {
            'row_counts': self.check_row_counts(agent_outputs),
            'total_reconciliation': self.check_totals(agent_outputs),
            'service_mapping': self.check_service_consistency(agent_outputs)
        }

    def check_row_counts(self, outputs):
        # All agents should process same number of rows
        row_counts = [
            outputs['data_processing']['rows_processed'],
            outputs['rate_calculator']['packages_calculated'],
            outputs['zone_analyst']['packages_analyzed'],
            outputs['weight_analyst']['packages_analyzed']
        ]
        return len(set(row_counts)) == 1

    def check_totals(self, outputs):
        # Sum of zone subtotals should equal grand total
        zone_total = sum(outputs['zone_analyst']['costs_by_zone'].values())
        grand_total = outputs['savings_calculator']['total_current_cost']

        tolerance = 0.01  # 1% tolerance for rounding
        return abs(zone_total - grand_total) / grand_total < tolerance

    def check_service_consistency(self, outputs):
        # Service mappings should cover all services
        original_services = set(outputs['data_processing']['unique_services'])
        mapped_services = set(outputs['service_mapper']['mappings'].keys())
        return original_services == mapped_services
```

## 2. AGGREGATION FRAMEWORK

### 2.1 Data Aggregation Pipeline

#### Master Aggregator
```python
class MasterAggregator:
    def __init__(self):
        self.agent_results = {}
        self.aggregated_data = {}

    def collect_agent_output(self, agent_id, output):
        """Collect output from individual agent"""
        self.agent_results[agent_id] = {
            'data': output,
            'timestamp': datetime.now(),
            'status': 'collected'
        }

    def aggregate_all_results(self):
        """Combine all agent outputs into unified dataset"""
        return {
            'shipping_analysis': self.aggregate_shipping_data(),
            'cost_analysis': self.aggregate_cost_data(),
            'savings_analysis': self.aggregate_savings_data(),
            'projections': self.aggregate_projections()
        }

    def aggregate_shipping_data(self):
        """Combine base shipping data with calculations"""
        base_data = self.agent_results['data_processing']['data']['cleaned_data']
        rates = self.agent_results['rate_calculator']['data']['rate_calculations']

        # Merge dataframes
        combined = base_data.copy()
        combined['current_cost'] = rates['current_costs']
        combined['xparcel_cost'] = rates['xparcel_costs']
        combined['savings'] = rates['savings']
        combined['savings_pct'] = rates['savings_percentage']

        return combined

    def aggregate_cost_data(self):
        """Aggregate cost metrics from multiple agents"""
        return {
            'by_zone': self.agent_results['zone_analyst']['data']['zone_costs'],
            'by_weight': self.agent_results['weight_analyst']['data']['weight_costs'],
            'by_service': self.agent_results['service_mapper']['data']['service_costs'],
            'totals': {
                'current_total': sum(self.agent_results['rate_calculator']['data']['current_costs']),
                'xparcel_total': sum(self.agent_results['rate_calculator']['data']['xparcel_costs']),
                'total_savings': sum(self.agent_results['rate_calculator']['data']['savings'])
            }
        }

    def aggregate_savings_data(self):
        """Combine savings metrics from all dimensions"""
        savings = self.agent_results['savings_calculator']['data']

        return {
            'summary': savings['savings_summary'],
            'by_category': {
                'zone': savings['detailed_savings']['by_zone'],
                'weight': savings['detailed_savings']['by_weight'],
                'service': savings['detailed_savings']['by_service']
            },
            'top_opportunities': savings['top_opportunities'],
            'projections': savings['projections']
        }
```

### 2.2 Hierarchical Aggregation

#### Multi-Level Aggregation
```python
class HierarchicalAggregator:
    def aggregate_by_hierarchy(self, data):
        return {
            'company_level': self.aggregate_company(data),
            'service_level': self.aggregate_by_service(data),
            'zone_level': self.aggregate_by_zone(data),
            'weight_level': self.aggregate_by_weight(data),
            'time_level': self.aggregate_by_time(data)
        }

    def aggregate_company(self, data):
        """Top-level company metrics"""
        return {
            'total_packages': len(data),
            'total_current_spend': data['current_cost'].sum(),
            'total_xparcel_cost': data['xparcel_cost'].sum(),
            'total_savings': data['savings'].sum(),
            'average_savings_pct': data['savings_pct'].mean(),
            'implementation_impact': {
                'monthly': data['savings'].sum(),
                'annual': data['savings'].sum() * 12
            }
        }

    def aggregate_by_service(self, data):
        """Service-level breakdown"""
        return data.groupby('service').agg({
            'tracking': 'count',
            'current_cost': 'sum',
            'xparcel_cost': 'sum',
            'savings': 'sum',
            'weight': 'mean',
            'zone': 'mean'
        }).to_dict()

    def aggregate_by_zone(self, data):
        """Zone-level breakdown"""
        zone_agg = {}
        for zone in range(1, 9):
            zone_data = data[data['zone'] == zone]
            if len(zone_data) > 0:
                zone_agg[f'zone_{zone}'] = {
                    'volume': len(zone_data),
                    'volume_pct': len(zone_data) / len(data) * 100,
                    'current_cost': zone_data['current_cost'].sum(),
                    'xparcel_cost': zone_data['xparcel_cost'].sum(),
                    'savings': zone_data['savings'].sum(),
                    'avg_weight': zone_data['weight'].mean()
                }
        return zone_agg

    def aggregate_by_weight(self, data):
        """Weight bucket aggregation"""
        weight_buckets = [
            (0, 0.25, '0-4oz'),
            (0.25, 0.5, '4-8oz'),
            (0.5, 1.0, '8oz-1lb'),
            (1.0, 2.0, '1-2lb'),
            (2.0, 5.0, '2-5lb'),
            (5.0, 10.0, '5-10lb'),
            (10.0, 20.0, '10-20lb'),
            (20.0, 200.0, '20lb+')
        ]

        weight_agg = {}
        for min_w, max_w, label in weight_buckets:
            bucket_data = data[(data['weight'] > min_w) & (data['weight'] <= max_w)]
            if len(bucket_data) > 0:
                weight_agg[label] = {
                    'volume': len(bucket_data),
                    'volume_pct': len(bucket_data) / len(data) * 100,
                    'total_savings': bucket_data['savings'].sum(),
                    'avg_savings_pct': bucket_data['savings_pct'].mean()
                }
        return weight_agg
```

### 2.3 Statistical Aggregation

#### Advanced Metrics
```python
class StatisticalAggregator:
    def calculate_statistics(self, data):
        return {
            'descriptive': self.descriptive_stats(data),
            'distributions': self.distribution_analysis(data),
            'correlations': self.correlation_analysis(data),
            'outliers': self.outlier_detection(data)
        }

    def descriptive_stats(self, data):
        return {
            'savings': {
                'mean': data['savings'].mean(),
                'median': data['savings'].median(),
                'std': data['savings'].std(),
                'min': data['savings'].min(),
                'max': data['savings'].max(),
                'percentiles': {
                    '25': data['savings'].quantile(0.25),
                    '50': data['savings'].quantile(0.50),
                    '75': data['savings'].quantile(0.75),
                    '90': data['savings'].quantile(0.90),
                    '95': data['savings'].quantile(0.95)
                }
            }
        }

    def distribution_analysis(self, data):
        return {
            'weight_distribution': data['weight'].value_counts(bins=10).to_dict(),
            'zone_distribution': data['zone'].value_counts().to_dict(),
            'service_distribution': data['service'].value_counts().to_dict()
        }

    def correlation_analysis(self, data):
        return {
            'weight_savings_corr': data['weight'].corr(data['savings']),
            'zone_savings_corr': data['zone'].corr(data['savings']),
            'weight_zone_corr': data['weight'].corr(data['zone'])
        }

    def outlier_detection(self, data):
        Q1 = data['savings'].quantile(0.25)
        Q3 = data['savings'].quantile(0.75)
        IQR = Q3 - Q1

        outliers = data[(data['savings'] < Q1 - 1.5*IQR) | (data['savings'] > Q3 + 1.5*IQR)]

        return {
            'outlier_count': len(outliers),
            'outlier_percentage': len(outliers) / len(data) * 100,
            'outlier_impact': outliers['savings'].sum(),
            'top_outliers': outliers.nlargest(10, 'savings')[['tracking', 'savings']].to_dict()
        }
```

## 3. QUALITY ASSURANCE

### 3.1 End-to-End Validation
```python
class QualityAssurance:
    def final_validation(self, aggregated_data):
        return {
            'completeness': self.check_completeness(aggregated_data),
            'accuracy': self.check_accuracy(aggregated_data),
            'consistency': self.check_consistency(aggregated_data),
            'business_logic': self.check_business_logic(aggregated_data)
        }

    def check_completeness(self, data):
        required_elements = [
            'executive_summary',
            'shipment_details',
            'rate_comparison',
            'zone_analysis',
            'service_analysis',
            'weight_distribution',
            'savings_breakdown',
            'monthly_projections',
            'service_levels'
        ]
        return all(elem in data for elem in required_elements)

    def check_accuracy(self, data):
        # Verify calculations
        checks = {
            'savings_calculation': self.verify_savings_math(data),
            'percentage_calculation': self.verify_percentages(data),
            'projection_calculation': self.verify_projections(data)
        }
        return all(checks.values())

    def verify_savings_math(self, data):
        # Savings = Current - Xparcel
        calculated = data['current_cost'] - data['xparcel_cost']
        reported = data['savings']
        tolerance = 0.01
        return abs(calculated.sum() - reported.sum()) / reported.sum() < tolerance

    def verify_percentages(self, data):
        # Percentage = Savings / Current * 100
        calculated = (data['savings'] / data['current_cost'] * 100).mean()
        reported = data['savings_pct'].mean()
        return abs(calculated - reported) < 1  # 1% tolerance

    def verify_projections(self, data):
        # Annual = Monthly * 12 (with seasonal adjustments)
        monthly = data['monthly_savings']
        annual = sum([m * seasonal_factor(month) for month, m in enumerate(monthly)])
        reported = data['annual_projection']
        return abs(annual - reported) / reported < 0.05  # 5% tolerance
```

### 3.2 Report Validation
```python
class ReportValidator:
    def validate_excel_output(self, workbook):
        return {
            'structure': self.check_structure(workbook),
            'formatting': self.check_formatting(workbook),
            'formulas': self.check_formulas(workbook),
            'data_integrity': self.check_data_integrity(workbook)
        }

    def check_structure(self, wb):
        required_tabs = [
            'Executive Summary',
            'Shipment Details',
            'Rate Comparison',
            'Zone Analysis',
            'Service Analysis',
            'Weight Distribution',
            'Savings Breakdown',
            'Monthly Projections',
            'Service Levels'
        ]
        return all(tab in wb.sheetnames for tab in required_tabs)

    def check_formatting(self, wb):
        # Check header formatting, currency formatting, etc.
        ws = wb['Executive Summary']
        checks = {
            'header_exists': ws['A1'].value is not None,
            'header_formatted': ws['A1'].font.bold == True,
            'currency_format': '$' in ws['B8'].number_format
        }
        return all(checks.values())
```

## 4. ERROR RECOVERY & FALLBACK

### 4.1 Validation Failure Handling
```yaml
validation_failure_protocol:
    input_validation_fail:
        action: clean_and_retry
        fallback: use_statistical_imputation

    calculation_validation_fail:
        action: recalculate_with_defaults
        fallback: use_conservative_estimates

    aggregation_validation_fail:
        action: re_aggregate_from_source
        fallback: use_partial_results

    report_validation_fail:
        action: regenerate_report
        fallback: create_simplified_report
```

### 4.2 Aggregation Recovery
```python
def recover_from_aggregation_failure(failure_type, partial_data):
    recovery_strategies = {
        'missing_agent_data': lambda: use_default_values(),
        'inconsistent_totals': lambda: recalculate_from_source(),
        'outlier_contamination': lambda: apply_outlier_filtering(),
        'calculation_error': lambda: use_fallback_formulas()
    }

    strategy = recovery_strategies.get(failure_type, lambda: use_best_effort())
    return strategy()
```

## 5. FINAL OUTPUT VALIDATION

### 5.1 Success Criteria
```yaml
final_validation_criteria:
    mandatory:
        - all_9_tabs_present
        - savings_between_20_60_percent
        - no_negative_values
        - totals_reconcile

    recommended:
        - charts_generated
        - formatting_applied
        - outliers_documented
        - assumptions_stated

    quality_score:
        calculation: (mandatory_passed * 100 + recommended_passed * 20) / 120
        passing_score: 85
```

This framework ensures reliable, accurate, and professional shipping analysis results through comprehensive validation and intelligent aggregation.