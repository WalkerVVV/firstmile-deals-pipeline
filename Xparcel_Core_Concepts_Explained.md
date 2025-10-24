# Xparcel Core Concepts Explained

**Source:** FirstMile Internal Documentation

---

Core Concepts Explained

1. What is Xparcel?

Definition: A ship method offered by FirstMile.

Goal: Simplify and optimize shipping by dynamically selecting the best carrier option per package at the time of label generation.

2. Value Proposition

Dynamic Optimization: Each package is evaluated in real-time across multiple carriers based on weight, dimensions, destination, and cost factors.

Smart Routing vs. Rate Shopping: Avoids “rate shop” terminology; positioned as smart routing to find the best price + service combination.

Single Interface: Consolidates multi-carrier complexities into:

One pickup

One invoice

One tracking system

One claims department

Control: Customers can apply zip code limits to exclude slower carriers if their buyers demand faster service (e.g., 95% delivered within 5 days).

3. Service Levels (Ship Methods)

Xparcel Priority: ~2–3 day service.

Xparcel Expedited: 3–5 days.

Xparcel Ground: 3–8 days.

Additional Buckets (via API): “FirstMile Second Day” and “FirstMile Three Day” exist but depend on partner integration.

Returns Handling: Xparcel Returns available.

International Services: Xparcel International allows optimization between carriers (e.g., DHL Parcel Standard vs. Asendia) based on destination, weight, and zone.

4. Routing Mechanics

Step 1: Package details entered (weight, dimensions, service level).

Step 2: Rate engine queries eligible last-mile carriers (typically 4–6 options).

Step 3: Eligibility filtered by service area (e.g., ACI, VHO, UNI may not cover all zips).

Step 4: Cost layers applied:

Base rate

Fuel surcharge

Dimensional/NQD fees

Step 5: System selects carrier with lowest total landed cost while meeting service level.

Step 6: Winning label prints → applied to package → consolidated pickup → delivered via FirstMile network.

5. Error Prevention & Past Issues

Recent billing mismatch was in invoicing, not the rate selection engine.

Assurance provided: rate quotes were correct, labels printed were the right winners.

6. Competitive Differentiators

Network Access: FirstMile provides access to regional, gig, and local carriers that small/medium businesses typically can’t contract directly.

Leverage of Linehaul Network: FirstMile’s linehaul operations allow aggregation of volume → enabling broader carrier participation.

Customer Benefit: Even SMB shippers can access nationwide + regional coverage through a single contract.

Key Insights & Observations

Xparcel is not just a “cheaper rate engine” but a strategic optimization layer offering control, speed, and flexibility.

The ability to selectively zip-limit carriers adds a customizable service-quality safeguard.

International optimization (DHL vs. Asendia) highlights FirstMile’s ability to extend beyond domestic shipments.

Ensuring billing systems align with quoting logic is critical to maintaining credibility.

Decisions Made

None formalized during training.

Agreement to use this framework and explanation for customer-facing conversations.

Follow-Ups & Action Items

Reps to incorporate Xparcel explanation (smart routing, network access, customer control) into prospect and client discussions.

Align billing processes to prevent mismatch between rate selection vs. invoice charges (Ops/Finance responsibility).

Sales enablement to ensure training deck / grid is distributed for future reference.

Open Questions

Extent of partner integration with API buckets (“Second Day,” “Three Day”).

Future roadmap for expanding gig/local carrier participation internationally.

Additional Notes

Phil emphasized that FirstMile’s unique advantage is connecting networks customers wouldn’t normally access.

Reps should highlight both cost savings and expanded carrier access when pitching Xparcel.

Customers value not just pricing but consolidation, simplicity, and control.

