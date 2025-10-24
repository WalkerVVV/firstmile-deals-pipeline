# Brand Scout Research Guidelines - Tactical Playbook

## 🎯 Purpose

Actionable research strategies and Chrome DevTools MCP patterns for generating high-quality Brand Scout reports in 25-35 minutes.

---

## 🌐 Chrome DevTools MCP - Complete Tactical Guide

### Session Startup Protocol

**Before any research**:

```python
# 1. List available pages
mcp__chrome-devtools__list_pages()

# 2. Select existing page OR create new
mcp__chrome-devtools__select_page(pageIdx=0)
# OR
mcp__chrome-devtools__new_page(url="https://example.com")

# 3. Verify page is ready
mcp__chrome-devtools__take_snapshot()
```

### Core Research Patterns

#### Pattern 1: Homepage → About → Shipping (Standard Flow)

```python
# Step 1: Navigate to homepage
mcp__chrome-devtools__navigate_page(url="https://brand.com")
homepage_snapshot = mcp__chrome-devtools__take_snapshot()

# Step 2: Extract homepage data
homepage_data = mcp__chrome-devtools__evaluate_script(
  function="""() => {
    return {
      title: document.title,
      description: document.querySelector('meta[name="description"]')?.content,
      h1: document.querySelector('h1')?.textContent
    }
  }"""
)

# Step 3: Navigate to About
mcp__chrome-devtools__navigate_page(url="https://brand.com/about")
about_content = mcp__chrome-devtools__scrape_tool()

# Step 4: Navigate to Shipping
mcp__chrome-devtools__navigate_page(url="https://brand.com/shipping")
shipping_content = mcp__chrome-devtools__scrape_tool()
shipping_snapshot = mcp__chrome-devtools__take_snapshot()
```

#### Pattern 2: Checkout Flow Investigation

```python
# Step 1: Go to products page
mcp__chrome-devtools__navigate_page(url="https://brand.com/products")
products_snapshot = mcp__chrome-devtools__take_snapshot()

# Step 2: Identify and click first product
# (Use UID from snapshot)
mcp__chrome-devtools__click(uid="product-link-uid")

# Step 3: Add to cart
product_snapshot = mcp__chrome-devtools__take_snapshot()
mcp__chrome-devtools__click(uid="add-to-cart-button-uid")

# Step 4: Go to checkout
mcp__chrome-devtools__navigate_page(url="https://brand.com/checkout")
checkout_snapshot = mcp__chrome-devtools__take_snapshot()

# Step 5: Screenshot shipping options
shipping_screenshot = mcp__chrome-devtools__take_screenshot(
  fullPage=True,
  format="png"
)

# Step 6: Extract shipping data
shipping_options = mcp__chrome-devtools__evaluate_script(
  function="""() => {
    return Array.from(document.querySelectorAll('.shipping-option')).map(opt => ({
      name: opt.querySelector('.method-name')?.textContent,
      price: opt.querySelector('.price')?.textContent,
      time: opt.querySelector('.delivery-time')?.textContent
    }))
  }"""
)
```

#### Pattern 3: Contact Discovery (Multi-Source)

```python
# Method 1: Team/About page
mcp__chrome-devtools__navigate_page(url="https://brand.com/team")
team_content = mcp__chrome-devtools__scrape_tool()

team_members = mcp__chrome-devtools__evaluate_script(
  function="""() => {
    return Array.from(document.querySelectorAll('.team-member')).map(member => ({
      name: member.querySelector('.name')?.textContent,
      title: member.querySelector('.title')?.textContent,
      email: member.querySelector('a[href^="mailto:"]')?.href?.replace('mailto:', ''),
      bio: member.querySelector('.bio')?.textContent
    }))
  }"""
)

# Method 2: Contact page
mcp__chrome-devtools__navigate_page(url="https://brand.com/contact")
contact_data = mcp__chrome-devtools__evaluate_script(
  function="""() => {
    const emails = Array.from(document.querySelectorAll('a[href^="mailto:"]'))
      .map(a => a.href.replace('mailto:', ''));
    const phones = document.body.innerText
      .match(/\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}/g) || [];
    return { emails, phones };
  }"""
)

# Method 3: LinkedIn via web search (performed separately)
# WebSearch: "site:linkedin.com [BRAND] founder"
# WebSearch: "site:linkedin.com [BRAND] VP operations"
```

#### Pattern 4: Carrier Detection (Advanced)

```python
# Step 1: Navigate to shipping/tracking page
mcp__chrome-devtools__navigate_page(url="https://brand.com/track")
tracking_snapshot = mcp__chrome-devtools__take_snapshot()

# Step 2: Extract tracking URLs and carrier references
carrier_detection = mcp__chrome-devtools__evaluate_script(
  function="""() => {
    const text = document.body.innerText.toLowerCase();
    const html = document.documentElement.outerHTML.toLowerCase();

    const carriers = {
      detected: [],
      tracking_patterns: []
    };

    // Text-based detection
    if (text.includes('usps') || text.includes('postal')) carriers.detected.push('USPS');
    if (text.includes('ups')) carriers.detected.push('UPS');
    if (text.includes('fedex')) carriers.detected.push('FedEx');
    if (text.includes('dhl')) carriers.detected.push('DHL');

    // URL-based detection
    if (html.includes('tools.usps.com') || html.includes('track17.net')) {
      carriers.tracking_patterns.push('USPS tracking URL');
    }
    if (html.includes('wwwapps.ups.com')) {
      carriers.tracking_patterns.push('UPS tracking URL');
    }
    if (html.includes('fedex.com/tracking')) {
      carriers.tracking_patterns.push('FedEx tracking URL');
    }

    // Logo detection
    const images = Array.from(document.images).map(img => img.src.toLowerCase());
    images.forEach(src => {
      if (src.includes('usps')) carriers.detected.push('USPS (logo)');
      if (src.includes('ups')) carriers.detected.push('UPS (logo)');
      if (src.includes('fedex')) carriers.detected.push('FedEx (logo)');
    });

    return carriers;
  }"""
)

# Step 3: Check network requests for carrier APIs
network_requests = mcp__chrome-devtools__list_network_requests()
# Filter for carrier domains in request URLs
```

#### Pattern 5: Platform Detection

```python
platform_detection = mcp__chrome-devtools__evaluate_script(
  function="""() => {
    const html = document.documentElement.outerHTML.toLowerCase();
    const scripts = Array.from(document.scripts).map(s => s.src.toLowerCase());

    // Shopify detection
    if (html.includes('shopify') ||
        scripts.some(s => s.includes('cdn.shopify.com'))) {
      return 'Shopify';
    }

    // WooCommerce detection
    if (html.includes('wp-content') ||
        html.includes('woocommerce')) {
      return 'WooCommerce';
    }

    // Magento detection
    if (html.includes('magento') ||
        html.includes('skin/frontend')) {
      return 'Magento';
    }

    // BigCommerce detection
    if (scripts.some(s => s.includes('bigcommerce.com'))) {
      return 'BigCommerce';
    }

    return 'Unknown';
  }"""
)
```

### Advanced Techniques

#### Pagination Handling

```python
# Step 1: Check for "Load More" button
snapshot = mcp__chrome-devtools__take_snapshot()

# Step 2: If found, click it
mcp__chrome-devtools__click(uid="load-more-button-uid")

# Step 3: Wait for new content
mcp__chrome-devtools__wait_for(text="Additional items loaded", timeout=5000)

# Step 4: Take new snapshot
updated_snapshot = mcp__chrome-devtools__take_snapshot()
```

#### Modal/Popup Handling

```python
# Option 1: Dismiss dialog
mcp__chrome-devtools__handle_dialog(action="dismiss")

# Option 2: Click close button
snapshot = mcp__chrome-devtools__take_snapshot()
mcp__chrome-devtools__click(uid="modal-close-button-uid")
```

#### Slow Loading Pages

```python
# Option 1: Wait for specific text
mcp__chrome-devtools__wait_for(text="About Us", timeout=10000)

# Option 2: Navigate and wait
mcp__chrome-devtools__navigate_page(url="https://brand.com/about", timeout=10000)

# Option 3: Manual delay (use sparingly)
import time
time.sleep(3)
mcp__chrome-devtools__take_snapshot()
```

---

## 🔍 Web Search Strategy by Data Type

### Revenue Discovery

**High-Value Queries**:
```
"[BRAND] revenue 2024"
"[BRAND] annual sales"
"[BRAND] funding series A B C"
"[BRAND] Crunchbase"
"[BRAND] valuation"
"[BRAND] financial results"
```

**Secondary Sources**:
```
"[BRAND] growth rate"
"[BRAND] year over year"
"[BRAND] employee count" (revenue proxy)
```

### Contact Discovery

**LinkedIn Searches**:
```
"site:linkedin.com [BRAND] founder"
"site:linkedin.com [BRAND] CEO"
"site:linkedin.com [BRAND] VP operations"
"site:linkedin.com [BRAND] COO"
"site:linkedin.com [BRAND] head of logistics"
```

**Press & Media**:
```
"[BRAND] press release CEO"
"[BRAND] announces [recent event]"
"[BRAND] interview founder"
```

### Shipping Intelligence

**Policy & Complaints**:
```
"[BRAND] shipping policy"
"[BRAND] delivery time"
"[BRAND] shipping cost"
"[BRAND] shipping complaints Trustpilot"
"[BRAND] delivery issues Reddit"
"[BRAND] late delivery"
```

**Carrier Discovery**:
```
"[BRAND] tracking number format"
"[BRAND] ships with USPS UPS FedEx"
"[BRAND] order tracking"
```

### Competitor Intelligence

**Direct Comparison**:
```
"[BRAND] competitors"
"[BRAND] vs [COMPETITOR]"
"[BRAND] alternative brands"
"brands like [BRAND]"
```

**Market Position**:
```
"[BRAND] market share"
"[BRAND] industry position"
"[BRAND] competitive advantage"
```

---

## ✅ Data Validation Rules

### Cross-Reference Requirements

**Revenue Data**:
- ✅ Verify with 2+ sources (Crunchbase + press release)
- ⚠️ Single source or estimated from funding/employees
- ❌ Complete guess (leave blank)

**Contact Information**:
- ✅ Email domain matches company website
- ✅ LinkedIn profile exists and is current
- ⚠️ Generic email (info@, hello@) without verification
- ❌ Made-up contact (never submit)

**Shipping Data**:
- ✅ Verified on policy page AND checkout flow
- ✅ Carrier logos/tracking URLs present
- ⚠️ Policy page only, no checkout verification
- ⚠️ Inferred from tracking page domain

**Address**:
- ✅ Verified on company website footer/contact page
- ✅ Confirmed via Google Maps business listing
- ⚠️ Single source (press release or Crunchbase only)
- ❌ Guessed from domain registration (unreliable)

### Confidence Marker Usage

| Marker | Meaning | When to Use |
|--------|---------|-------------|
| ✅ | Verified | 2+ sources OR official company source + external validation |
| ⚠️ | Unverified | Single source OR estimated with methodology |
| ❌ | Invalid | Do not use - leave field blank instead |

### When to Estimate vs. Leave Blank

**OK to Estimate**:
- Revenue (from funding, employees, product catalog)
- Ship volume (from revenue ÷ AOV)
- Growth rate (year-over-year comparison)
- Service level pricing (typical DTC ranges)

**NEVER Estimate**:
- Contact names/emails
- Company legal name
- Website URL
- Specific carrier names (use "Unknown" if unsure)

---

## 🎯 Section-Specific Research Tactics

### Section 1: Snapshot (Metrics & Overview)

**Data Sources**:
1. Homepage hero/tagline → Elevator pitch
2. About page → Mission, value props
3. Product pages → AOV calculation
4. Crunchbase → Revenue, funding
5. Press releases → Growth metrics

**Quick AOV Calculation**:
```python
# Sample 10-15 products
products = [
  {"name": "Product A", "price": 29.99},
  {"name": "Product B", "price": 45.00},
  # ... more products
]

total_price = sum([p["price"] for p in products])
aov = total_price / len(products)
# Result: AOV = $XX.XX
```

**Volume Estimation**:
```python
# Method 1: From revenue
annual_revenue = 12_500_000  # $12.5M
aov = 85.00
annual_volume = annual_revenue / aov
# Result: ~147K units

# Method 2: From product catalog
products_count = 50
avg_monthly_sales_per_product = 250
annual_volume = products_count * avg_monthly_sales_per_product * 12
# Result: ~150K units
```

### Section 2: Shipping Intelligence (Deep Dive)

**5-Layer Investigation**:

1. **Policy Page** (2-3 min):
   - Navigate to /shipping or /delivery
   - Extract carrier names
   - Note service levels
   - Capture pricing tiers

2. **Checkout Flow** (2-3 min):
   - Add product to cart
   - Proceed to checkout
   - Screenshot shipping options
   - Extract costs and SLAs

3. **Tracking Page** (1 min):
   - Find order tracking link
   - Navigate to tracking page
   - Identify carrier URLs
   - Note tracking number format

4. **Review Sites** (2-3 min):
   - Trustpilot: Filter by "shipping" or "delivery"
   - Better Business Bureau: Check complaints
   - Extract pain points and percentages

5. **FAQ/Help** (1 min):
   - Check delivery-related FAQs
   - Note common issues
   - Identify 3PL mentions

### Section 3: Company Overview

**Essential Pages**:
1. Homepage footer → Legal name, address
2. About Us → Founding year, mission
3. Contact → HQ address, phone
4. Press → Milestones, announcements

**DTC/Wholesale Split**:
- Check "Wholesale" or "Retail Partners" page
- Search: "[BRAND] wholesale retailers"
- Estimate from business model description
- Mark as "Unknown" if not found

### Section 4: Stakeholders (High-Value)

**Contact Discovery Flow**:

1. **Website First** (2 min):
   - Team/Leadership page
   - About page (founder bios)
   - Contact page (general emails)

2. **LinkedIn Second** (3 min):
   - Search: `site:linkedin.com [BRAND] founder`
   - Search: `site:linkedin.com [BRAND] operations`
   - Search: `site:linkedin.com [BRAND] COO`
   - Navigate to profiles, extract names/titles

3. **Press Third** (2 min):
   - Search: "[BRAND] press release"
   - Extract names from quotes
   - Note titles and roles

4. **Crunchbase Fourth** (1 min):
   - Navigate to Crunchbase company page
   - Check "People" or "Leadership" tab
   - Cross-reference with LinkedIn

**Email Format Validation**:
```python
# Common patterns
patterns = [
  "firstname.lastname@domain.com",
  "firstname@domain.com",
  "flastname@domain.com",
  "initial+lastname@domain.com"
]

# Verify domain matches company website
email_domain = contact_email.split('@')[1]
company_domain = "brand.com"
is_valid = email_domain == company_domain
```

### Section 5: Observations & Competitors

**Complaint Analysis**:

1. **Trustpilot** (2 min):
   - Navigate to trustpilot.com
   - Search for brand
   - Filter by 1-2 star reviews
   - Search within reviews for "shipping", "delivery", "late"
   - Extract top 3 issues with rough percentages

2. **Better Business Bureau** (1 min):
   - Navigate to bbb.org
   - Search for brand
   - Check complaint categories
   - Note any shipping-related patterns

3. **Reddit** (1 min):
   - Search: `site:reddit.com [BRAND] shipping`
   - Search: `site:reddit.com [BRAND] delivery`
   - Note recurring themes

**Competitor Benchmarking**:

1. **Identify 2-3 Competitors** (1 min):
   - Search: "[BRAND] competitors"
   - Search: "brands like [BRAND]"

2. **Quick Shipping Comparison** (2 min):
   - Navigate to competitor shipping pages
   - Note delivery promises (e.g., "3-5 days")
   - Check pricing (if public)
   - Compare to target brand

---

## ⏱️ Time Management Strategies

### 35-Minute Hard Stop

**Phase Allocation**:
- Minutes 0-10: Initial discovery (homepage, about, revenue search)
- Minutes 10-25: Deep intelligence (shipping, contacts, validation)
- Minutes 25-30: Verification and cross-checks
- Minutes 30-35: Template fill and output generation

**Early Stop Criteria**:
- 80%+ mandatory fields complete → Stop at minute 25
- Diminishing returns (repeating searches) → Stop immediately
- Technical blocker (site down) → Stop, use fallbacks

**Time Savers**:
- Use scrape_tool for full page content vs. manual extraction
- Search generic emails (info@, hello@) if team page not found
- Estimate revenue from employees if no funding data (employees × $200K)
- Use "Unknown" for missing optional fields vs. spending 5+ min searching

---

## 🚨 Common Pitfalls & Solutions

### ❌ Problem: Website Blocks Automation

**✅ Solution**:
```python
# Try Wayback Machine
WebFetch("https://web.archive.org/web/20240101000000/brand.com")

# Or cached version
WebSearch("cache:brand.com")

# Or LinkedIn company page as backup
WebSearch("site:linkedin.com/company/brand")
```

### ❌ Problem: No Shipping Page Found

**✅ Solution**:
1. Check /shipping, /delivery, /shipping-policy
2. Navigate to FAQ → Search for "shipping"
3. Test checkout flow (most reliable)
4. Search: `"[BRAND] shipping policy"`
5. Last resort: Estimate based on typical DTC (USPS Ground Advantage)

### ❌ Problem: No Contact Info Anywhere

**✅ Solution**:
1. Try generic emails: `info@domain`, `hello@domain`, `support@domain`
2. LinkedIn company page → "See all employees"
3. Press releases → Extract names from quotes
4. Crunchbase → Leadership tab
5. Mark as ⚠️ Unverified, note in Section 9

### ❌ Problem: Revenue Completely Unavailable

**✅ Solution**:
```python
# Method 1: From funding
funding_total = 10_000_000  # $10M raised
arr_estimate = funding_total / 10  # Typical 10x multiple
# Result: Est. $1M revenue

# Method 2: From employees
employee_count = 50
revenue_per_employee = 200_000
revenue_estimate = employee_count * revenue_per_employee
# Result: Est. $10M revenue

# Method 3: From product catalog
products = 50
avg_price = 45
monthly_sales_per_product = 100
annual_revenue = products * avg_price * monthly_sales_per_product * 12
# Result: Est. $2.7M revenue
```

Always mark as "Est." in report.

### ❌ Problem: Checkout Requires Account Creation

**✅ Solution**:
1. Don't create account (time-consuming)
2. Use shipping policy page data instead
3. Search: `"[BRAND] checkout shipping options"`
4. Check Trustpilot reviews for shipping cost mentions
5. Mark shipping data as ⚠️ (policy only, not verified in checkout)

---

## 📊 Quality Assurance Checklist

**Before finalizing report, verify**:

### Data Integrity
- [ ] Company name matches website exactly
- [ ] Website URL is functional (not 404)
- [ ] At least 1 contact has ✅ verification
- [ ] Email domains match company domain
- [ ] Phone numbers in (XXX) XXX-XXXX format
- [ ] No [PLACEHOLDER] text remaining

### HubSpot Section
- [ ] All required fields populated
- [ ] Average Daily Volume = Annual Volume ÷ 365
- [ ] All dates set to today (YYYY-MM-DD)
- [ ] Contact Owner = "Brett Walker"
- [ ] Lead Pipeline = "Default"
- [ ] Lead Stage = "New"

### Calculations
- [ ] AOV calculated from product sampling
- [ ] Annual Volume = Revenue ÷ AOV (or alternative method)
- [ ] Growth rate from year-over-year comparison (if available)
- [ ] Tier A/B assignment: A if Rev >$10M OR Vol >100K

### Sources
- [ ] Minimum 3 sources documented
- [ ] Estimates marked with "Est."
- [ ] Single-source data marked with ⚠️
- [ ] Methodology noted in Section 9

---

## 🎓 Reference Tables

### Carrier Detection Quick Reference

| Tracking URL Pattern | Carrier |
|---------------------|---------|
| `tools.usps.com` | USPS |
| `track17.net` | USPS |
| `wwwapps.ups.com` | UPS |
| `fedex.com/tracking` | FedEx |
| `shipstation.com` | Multi-carrier (likely USPS) |
| `stamps.com` | USPS |
| `easypost.com` | Multi-carrier API |
| `pitneybowes.com` | Multi-carrier |

### Platform Detection Quick Reference

| Indicator | Platform |
|-----------|----------|
| `/cdn.shopify.com/` | Shopify |
| `myshopify.com` in HTML | Shopify |
| `/wp-content/` | WordPress/WooCommerce |
| `woocommerce` in HTML | WooCommerce |
| `/skin/frontend/` | Magento |
| `magento` in HTML | Magento |
| `bigcommerce.com` in scripts | BigCommerce |

### Contact Title Priority (Decision-Making Authority)

| Title | Priority | Outreach Value |
|-------|----------|----------------|
| Founder, CEO, President | **HIGH** | Primary contact |
| COO, VP Operations | **HIGH** | Primary contact |
| Director of Logistics, Head of Shipping | **HIGH** | Primary contact |
| Operations Manager | **MEDIUM** | Secondary contact |
| Marketing Director | **MEDIUM** | Influencer |
| Customer Service Manager | **LOW** | Info only |

---

## 🚀 Pro Tips

### Time-Saving Shortcuts

**Quick Company Intel**:
```
WebSearch: "[BRAND] about revenue founder headquarters"
```
(Combines multiple queries into one)

**Quick Shipping Intel**:
```python
# Try all common shipping URLs at once
urls = [
  "https://brand.com/shipping",
  "https://brand.com/delivery",
  "https://brand.com/shipping-policy"
]

for url in urls:
  try:
    mcp__chrome-devtools__navigate_page(url=url, timeout=5000)
    content = mcp__chrome-devtools__scrape_tool()
    if "carrier" in content.lower() or "usps" in content.lower():
      # Found shipping page, proceed
      break
  except:
    continue
```

**Quick Contact Intel**:
```python
# Check all common contact pages
urls = [
  "https://brand.com/contact",
  "https://brand.com/about",
  "https://brand.com/team",
  "https://brand.com/about-us"
]
```

### Pattern Recognition

**Revenue Proxies**:
- Employees × $200K = Rough revenue estimate
- Funding ÷ 10 = Typical ARR for startups
- Products × Price × 100 sales/month × 12 = Annual revenue

**Volume Proxies**:
- Revenue ÷ AOV = Annual units
- Daily shipments on social × 365 = Annual units

**Growth Indicators**:
- "Year-over-year" mentions in press
- Funding round progression (Seed → Series A = growth)
- Employee count increase (LinkedIn)

---

**Remember**: Speed is good, but accuracy is critical. A 28-minute report with 85% verified data beats a 15-minute report with 60% guesses.
