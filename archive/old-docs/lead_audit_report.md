Read segment_a_buyers_final.csv and segment_b_suppliers_final.csv and clean them:

SEGMENT A — Remove these leads:
1. All Sysco leads (foodservice-only operator, excluded per ICP)
2. All Amazon leads (vertically integrated, non-grocery titles like robotics/beauty/aviation)
3. All Walgreens leads (pharmacy chain, not grocery retailer)
4. All leads with titles containing "Directeur de Magasin", "Directeur Magasin", 
   "Manager de Magasin", "Store Manager", or "Store Director" — these are individual 
   store managers, not corporate procurement

SEGMENT B — Remove these leads:
1. All Southern Glazer's Wine & Spirits leads (alcohol distributor, not grocery)
2. All HEINEKEN leads (alcohol manufacturer)
3. All AB InBev leads (alcohol manufacturer)
4. All Nestlé Purina North America leads (pet food, not human food/confectionery)

Save cleaned files as:
- segment_a_buyers_cleaned.csv
- segment_b_suppliers_cleaned.csv

Also update config/exclusions.json to add these company and title exclusions 
so future Apollo pulls automatically filter them out.

Report the before/after counts for each segment.