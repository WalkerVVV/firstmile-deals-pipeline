# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Context

This is a FirstMile shipping proposal for ODW Logistics, a high-volume eCommerce fulfillment customer shipping 220,000 packages/month from Hamilton, OH.

## Data Files

- **FULL RFP DATA 2.csv**: Complete RFP shipping data including all service levels
- **MI RFP DATA.csv**: Michigan-specific RFP shipping data subset
- **ODW_TIER_TOOL_COMPLETE.md**: Completed FirstMile tier tool with volume assumptions and customer details

## ODW Logistics Profile

- **Monthly Volume**: 220,000 packages
- **Service Mix**: 10% Priority, 90% Expedited, 0% Ground
- **Weight Distribution**: 72.3% between 2.6-6.0 lbs (optimal for FirstMile)
- **Ship From**: 345 High Street, Hamilton, OH 45011
- **Contact**: Dean B. Freson (513-785-4986)
- **Implementation Date**: July 15, 2025

## Analysis Framework

When analyzing shipping data for ODW Logistics:

1. **Volume Analysis**: Focus on the 220,000 monthly package volume baseline
2. **Service Level Mapping**:
   - Priority = Xparcel Priority (1-3 days)
   - Expedited = Xparcel Expedited (2-5 days)
   - Ground = Xparcel Ground (3-8 days)
3. **Weight Sweet Spot**: Emphasize the 2.6-6.0 lb weight range advantage
4. **Zone Distribution**: Analyze regional vs cross-country splits
5. **Cost Optimization**: Compare current carrier costs vs FirstMile pricing

## FirstMile Terminology

Always use FirstMile standard terminology:
- Refer to services as "Xparcel Ground", "Xparcel Expedited", "Xparcel Priority"
- Use "National Network" and "Select Network" instead of naming specific carriers
- Emphasize dynamic routing, Audit Queue, and single support team advantages

## Key Analysis Points

- Current service mix heavily weighted to expedited (90%)
- Weight profile ideal for FirstMile network (72.3% in optimal range)
- High sophistication customer with existing competitor invoice
- Daily scheduled pickup required (2:00 PM - 4:00 PM window)
- Amazon/eBay multi-channel shipper

## Outstanding Information Needed

- Shipping System/TMS name
- Actual zone distribution data
- Clarification on shipping origin (Hamilton 45011 vs Cincinnati 45241)