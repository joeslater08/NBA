# Synthetic examples

Every team, player, fixture, price and result in `scripts/seed.py` is fictional.
The six requested real analyst names are registry entries only: no invented predictions or results are attached to them.

The deterministic example outcomes are one win (+0.90 units), one loss (−1 unit), and one push (0 units). Total −0.10 units on 3 settled units: ROI −3.333…%. Times are anchored to first seed execution (one past and one future fixture). Re-running seed preserves all existing data and timestamps. If the future fixture becomes stale, create a new synthetic fixture in the UI; do not rewrite the old one.

Preview `teams.csv` in Data centre with Synthetic demonstration selected. It is separate from the seeded teams so the import can be exercised without duplicates.
