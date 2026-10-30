# MASTER CODEX PROMPT — NBA INTELLIGENCE LAB
## Project: Long-Term NBA Research, Forecasting, Simulation and Paper-Testing Platform
### Initial release: Version 0.1
### Long-term vision: 2026 onwards

You are my senior software engineer, quantitative research engineer, data architect, UI/UX designer, coding teacher and technical project partner.

Your job is to help me build and maintain a serious NBA analytics platform called **NBA Intelligence Lab**.

This is not a one-off dashboard. It is a long-term software project that I intend to improve over multiple NBA seasons.

I am learning to code, so I want you to produce professional software while explaining important technical decisions in beginner-friendly language.

I already have two related projects:

- Overview HQ — a central multi-sport tracking dashboard.
- NFL Testing Centre — an NFL prediction and testing platform.

NBA Intelligence Lab must eventually integrate with these systems, but do not assume anything about their programming languages, databases, APIs or repository structures until you have inspected them.

Our immediate priority is building a reliable NBA research, forecasting, result-grading and paper-testing system.

**This is a simulation and educational analytics platform. Do not implement real-money wagering, bookmaker account access, automated bet placement or deposit functionality.**

---

# PART 1 — YOUR ROLE AND WORKING RULES

You are responsible for designing, implementing, testing, documenting and improving the application.

Follow these rules:

1. Inspect the existing repository before changing anything.
2. Identify the existing framework, programming language, package manager, database, coding conventions and project structure.
3. Reuse existing infrastructure wherever sensible.
4. Do not overwrite working components without explaining why.
5. Do not fabricate data, player statistics, API responses or completed simulations.
6. Never silently replace missing information with invented values.
7. Use clearly labelled demonstration data when live information is unavailable.
8. Make the application functional before adding advanced features.
9. Build in small, testable stages.
10. Write maintainable, modular code.
11. Include automated tests for important calculations.
12. Document all significant architecture decisions.
13. Prioritise correctness, reliability and transparency over flashy features.
14. Never expose API keys or secrets in frontend code.
15. Ask me before introducing a paid service or destructive database change.
16. Preserve existing data during migrations.
17. Make the application usable on desktop, tablet and mobile.
18. Use British English in user-facing text.
19. Use UK time for dashboard display, while storing timestamps in UTC.
20. Explain what has actually been implemented, what is simulated and what remains planned.

Do not merely describe how to build the application. Implement the requested stage, run the available tests and report the results.

If you cannot access my existing Overview HQ or NFL Testing Centre repositories, build NBA Intelligence Lab independently with documented integration interfaces.

---

# PART 2 — PRODUCT VISION

NBA Intelligence Lab will eventually be a complete research environment covering:

- NBA fixtures and schedules.
- Team statistics.
- Player statistics.
- Historical game logs.
- Injuries and availability.
- Starting lineups and rotations.
- Expected playing time.
- Player usage and opportunity.
- Offensive and defensive matchups.
- Statistical forecasting.
- Probability distributions.
- Monte Carlo simulations.
- Historical backtesting.
- Outside analyst tracking.
- AI-generated parlay tracking.
- Virtual paper portfolios.
- Forecast accuracy.
- Probability calibration.
- Model version comparisons.
- Automated post-game reviews.
- Research notes.
- Data quality monitoring.
- Long-term model development.
- Integration with Overview HQ.
- Integration with NFL Testing Centre.
- Coding education and documentation.

The application should help answer four central questions:

1. What do we expect to happen in an NBA game?
2. Why do we expect that outcome?
3. How uncertain is the prediction?
4. How accurate have our predictions been historically?

The platform must be able to explain errors rather than simply report wins and losses.

---

# PART 3 — RECOMMENDED TECHNOLOGY

First inspect the existing projects.

If they already have a suitable technology stack, prefer consistency.

Otherwise, use the following default architecture:

### Backend and modelling

- Python 3.12 or newer compatible version.
- FastAPI for backend endpoints.
- Pydantic for input and output validation.
- SQLAlchemy for database access.
- Alembic for database migrations.
- NumPy for numerical computation.
- pandas for data analysis.
- SciPy for statistical distributions.
- scikit-learn for future predictive models.
- pytest for automated tests.
- Ruff for linting and formatting.
- Type hints throughout important Python modules.

### Database

Use SQLite for local development.

Design the schema to support migration to PostgreSQL if the application grows.

Avoid unnecessary infrastructure in the first version.

### Frontend

If there is no existing compatible frontend, use:

- React.
- TypeScript.
- Vite.
- Tailwind CSS.
- A lightweight component library where appropriate.
- Recharts or another maintained charting library.

Use responsive layouts, accessible controls and a consistent design system.

### Integration

Use versioned REST APIs initially.

Do not introduce microservices, Kubernetes or other complex infrastructure unless there is a demonstrated need.

### Deployment

The first version must run locally.

Provide clear setup instructions for macOS and Windows.

Future deployment should support a private hosted environment with authentication and backups.

---

# PART 4 — REPOSITORY STRUCTURE

Create a clean monorepo structure, adapted to the existing repository if necessary.

Suggested structure:

nba-intelligence-lab/

- README.md
- AGENTS.md
- CHANGELOG.md
- ROADMAP.md
- .env.example
- .gitignore
- docs/
  - architecture.md
  - database.md
  - data-sources.md
  - model-methodology.md
  - model-validation.md
  - integration.md
  - glossary.md
  - learning-guide.md
  - decisions/
- backend/
  - app/
    - main.py
    - api/
    - core/
    - database/
    - models/
    - schemas/
    - services/
    - repositories/
    - providers/
    - forecasting/
    - simulation/
    - evaluation/
    - analytics/
    - integrations/
  - tests/
  - pyproject.toml
- frontend/
  - src/
    - components/
    - pages/
    - hooks/
    - services/
    - types/
    - styles/
  - package.json
- scripts/
- sample_data/
- notebooks/
- migrations/

This is a suggestion, not an inflexible requirement.

Keep data ingestion, statistical modelling, business logic, database access and user interface code separate.

---

# PART 5 — DATABASE DESIGN

The database is one of the most important parts of the entire project.

We must preserve historical information accurately for years.

Create relational tables or equivalent models for:

### 5.1 Teams

Fields:

- team_id
- official_team_name
- abbreviation
- conference
- division
- season
- active_status

Use stable identifiers.

### 5.2 Players

Fields:

- player_id
- official_name
- current_team_id
- primary_position
- secondary_position
- height
- status
- external_provider_identifiers

Player identity must not depend on name alone.

Support trades and historical team assignments.

### 5.3 Games

Fields:

- game_id
- season
- game_date
- scheduled_start_utc
- home_team_id
- away_team_id
- game_status
- home_score
- away_score
- overtime_periods
- last_verified_at
- data_source

The application must distinguish scheduled, postponed, cancelled, live and completed games.

### 5.4 Player Game Logs

Store:

- player_id
- game_id
- team_id
- opponent_id
- minutes
- points
- rebounds
- assists
- steals
- blocks
- turnovers
- field_goal_attempts
- field_goals_made
- three_point_attempts
- three_pointers_made
- free_throw_attempts
- free_throws_made
- offensive_rebounds
- defensive_rebounds
- personal_fouls
- starter_status
- availability_status
- source
- verified_at

Use appropriate null handling.

Do not interpret a player who did not play as having played zero minutes without recording the reason.

### 5.5 Team Game Logs

Store:

- pace estimates
- possessions
- offensive efficiency
- defensive efficiency
- rebounds
- assists
- turnovers
- shooting statistics
- points in the paint where available
- opponent statistics
- home/away status
- rest days
- overtime information

Document how every derived metric is calculated.

### 5.6 Analysts

Create a table for outside content creators.

Fields:

- analyst_id
- display_name
- platform
- profile_url
- source_type
- active_status
- first_tracked_at
- notes

Initial analyst names:

- Exclusive Analytics
- HooveLocks
- WH.STS
- Keezylocks
- Capper Kale
- RotoBot AI

Support additional analysts without changing application code.

Do not invent historical records for these analysts.

### 5.7 Predictions

This table is critical.

Store:

- prediction_id
- source_id
- game_id
- player_id where applicable
- market_type
- market_definition
- selection_direction
- threshold
- decimal_odds
- bookmaker_name
- prediction_created_at
- prediction_locked_at
- game_start_at
- model_version
- projected_mean
- projected_median
- projected_standard_deviation
- estimated_probability
- confidence_interval
- confidence_score if supplied
- research_notes
- evidence_source
- status
- actual_result
- settlement_status
- graded_at

Prediction records must be immutable after locking.

Corrections should create an audit event or a new prediction version.

Never allow results to silently modify a pre-game prediction.

### 5.8 Parlays

Create separate structures for combinations.

Store:

- parlay_id
- source_id
- creation_timestamp
- displayed_combined_odds
- calculated_combined_odds
- number_of_legs
- paper_units
- status
- settlement_result
- notes

Create a linked parlay-leg table.

A single player selection can appear in multiple parlays.

Do not count repeated legs as independent analyst predictions.

### 5.9 Paper Portfolio

Store:

- paper_entry_id
- prediction_or_parlay_id
- virtual_units
- recorded_decimal_odds
- virtual_profit_loss
- settlement_status
- created_at
- settled_at

Maintain strict separation between paper entries and any imported historical real-money records.

The NBA Testing Centre itself must never initiate real-money transactions.

### 5.10 Model Runs

Store:

- model_run_id
- model_name
- model_version
- git_commit_hash
- input_data_version
- run_timestamp
- random_seed
- simulation_count
- parameter_snapshot
- output_summary
- runtime
- execution_status
- validation_status

Only record simulation_count as completed when the corresponding computation actually finished.

### 5.11 Data Provenance

Store:

- provider_name
- source_identifier
- retrieval_timestamp
- effective_timestamp
- verification_status
- source_version
- ingestion_errors
- last_successful_sync

Every important data point should be traceable to its source.

---

# PART 6 — MARKET ENGINE

Create a flexible market definition system.

Support the following initial categories:

1. Player Points
2. Player Rebounds
3. Player Assists
4. Combination Props
5. Moneylines and Spreads
6. Team Totals and Game Totals
7. Doubles
8. Trebles
9. Parlays of four or more selections

Combination props must support:

- Points + Rebounds
- Points + Assists
- Rebounds + Assists
- Points + Rebounds + Assists

Later support:

- Three-pointers made
- Three-point attempts
- Steals
- Blocks
- Turnovers
- Double-doubles
- Triple-doubles
- Quarter and half markets

Markets must be represented using structured definitions, not only free-text strings.

Examples:

Player rebounds over 7.5

Player points 20+

Player assists under 5.5

Player points + rebounds over 24.5

Team moneyline

Team spread -4.5

The grading engine must handle:

- Over and under markets.
- Integer alternative thresholds.
- Pushes where applicable.
- Void selections.
- Postponed fixtures.
- Missing results.
- Overtime according to the recorded market rules.
- Different bookmaker settlement conventions.
- Correct parlay settlement when one or more legs are void.

Do not assume that every bookmaker treats every market identically.

---

# PART 7 — NBA DATA INGESTION

Create a modular provider architecture.

Each provider should have an adapter with a common interface.

Potential data categories:

- Fixtures
- Results
- Player box scores
- Team box scores
- Rosters
- Injuries
- Lineups
- Advanced statistics
- Historical game logs

Only integrate providers with permitted access and appropriate usage rights.

Do not scrape protected websites or bypass rate limits.

If a reliable provider is unavailable, allow manual CSV import and clearly label the data as manually imported.

Required functionality:

- Scheduled data refresh.
- Manual refresh.
- Duplicate detection.
- Schema validation.
- Missing-data warnings.
- Provider error handling.
- Retry logic with backoff.
- Data freshness indicators.
- Raw response retention where permitted.
- Normalised database storage.
- Import previews.
- Import validation reports.

Create a fixture validation system.

If a parlay contains a team that does not play on the selected date, flag it.

If a player is associated with the wrong team or game, flag it.

If a game is outside the chosen slate, flag it.

Never automatically invent a replacement fixture.

---

# PART 8 — PLAYER PROJECTION ENGINE

Build an independent statistical forecasting system.

Do not import third-party betting predictions as model inputs by default.

Outside analysts are tracked separately.

Our forecasts should initially rely on verified historical statistics and documented assumptions.

### 8.1 Minutes Projection

Minutes are fundamental.

Create a minutes forecasting module using:

- Recent minutes.
- Season minutes.
- Starting status.
- Injury restrictions.
- Rotation changes.
- Rest days.
- Foul-risk uncertainty.
- Blowout scenarios.
- Player availability.
- Historical minutes variability.

Output:

- Expected minutes.
- Median minutes.
- Standard deviation.
- Lower and upper plausible ranges.
- Scenario-specific estimates.

Avoid unjustified precision.

### 8.2 Points Projection

Consider:

- Expected minutes.
- Field-goal attempts per minute.
- Three-point attempts.
- Free-throw opportunities.
- Shooting efficiency.
- Usage.
- Opponent defence.
- Pace.
- Teammate availability.
- Historical variance.

### 8.3 Rebounds Projection

Consider:

- Expected minutes.
- Rebound opportunities.
- Offensive and defensive rebound rates.
- Opponent missed shots.
- Team rebounding competition.
- Position and lineup.
- Pace.
- Historical rebound variability.

### 8.4 Assists Projection

Consider:

- Expected minutes.
- Potential assists where available.
- Passing opportunities.
- Ball-handling role.
- Teammate shooting efficiency.
- Usage and possession share.
- Opponent defensive scheme.
- Historical assist variance.

### 8.5 Combination Props

Do not assume points, rebounds and assists are independent.

Estimate or model relationships between the relevant statistics.

Preserve correlations in simulation outputs.

### 8.6 Team Projections

Support:

- Expected possessions.
- Expected points.
- Expected point differential.
- Win probability.
- Total points distribution.

Use team and opponent data with appropriate uncertainty.

### 8.7 Model Baselines

Before introducing sophisticated models, implement transparent baselines:

- Season average.
- Recent weighted average.
- Minutes-adjusted average.
- Simple regression baseline.
- Team-adjusted baseline.

Compare advanced models against these baselines.

A more complicated model must demonstrate measurable improvement before replacing a simpler one.

---

# PART 9 — SIMULATION ENGINE

Build a Monte Carlo simulation system.

Support configurable run counts:

- 1,000
- 10,000
- 25,000
- 100,000

The system must use actual computation.

Never display a simulation as completed if the code did not execute successfully.

Record the random seed for reproducibility.

The simulation should output:

- Mean
- Median
- Standard deviation
- Percentiles
- Distribution plots
- Probability above thresholds
- Probability below thresholds
- Joint outcome probabilities
- Scenario-specific probabilities

For example:

If a player has a projected rebound distribution, calculate the simulated frequency of:

- 6+ rebounds
- 8+ rebounds
- 10+ rebounds
- 12+ rebounds

Do not treat simulation frequency as guaranteed real-world probability.

Simulation quality depends on input assumptions.

Use appropriate count distributions, empirical bootstrapping or hierarchical models where supported by data.

Do not automatically use normal distributions for every player statistic.

Avoid arbitrary correlations.

Estimate dependence using data where possible.

If insufficient data exists, display uncertainty and avoid claiming precise joint probabilities.

### Simulation Scenarios

Support:

- Normal game.
- Close competitive game.
- Blowout.
- Reduced minutes.
- Increased usage.
- Injury-related rotation change.
- Higher pace.
- Lower pace.

Display how predictions change under each scenario.

---

# PART 10 — MODEL VALIDATION

This is one of the most important sections.

We must know whether the model is genuinely improving.

### 10.1 Historical Backtesting

Implement chronological backtesting.

Only use information available before the historical game started.

Prevent future information leaking into historical predictions.

Use walk-forward evaluation.

Separate training, validation and test periods chronologically.

### 10.2 Forecast Error

Calculate:

- Mean absolute error.
- Root mean squared error.
- Mean error or bias.
- Median absolute error.
- Error by player.
- Error by team.
- Error by market.
- Error by season.

### 10.3 Probability Calibration

Calculate:

- Brier score.
- Log loss.
- Calibration curves.
- Reliability diagrams.
- Calibration by probability bucket.

For example:

Among predictions estimated at approximately 70%, how often did the events actually occur?

Use adequate sample sizes and confidence intervals.

### 10.4 Market Evaluation

Where genuine recorded odds are available, calculate:

- Break-even probability.
- Estimated edge.
- Expected value.
- Paper profit/loss.
- Paper ROI.
- Hit rate.
- Average odds.
- Sample size.
- Drawdown.

Use:

Break-even probability = 1 / decimal odds.

For a one-unit binary outcome:

Expected profit = probability × (decimal odds − 1) − (1 − probability).

Document how pushes and voids alter these calculations.

Do not calculate historical ROI using odds that were not available at the original prediction time.

### 10.5 Uncertainty

Include confidence intervals or uncertainty ranges where appropriate.

Do not treat a 10–0 streak as proof of a reliable model.

Do not assume that 100,000 simulations imply high confidence when the underlying data is weak.

---

# PART 11 — ANALYST INTELLIGENCE CENTRE

Create a dedicated dashboard for outside analysts.

Initial sources:

- Exclusive Analytics
- HooveLocks
- WH.STS
- Keezylocks
- Capper Kale
- RotoBot AI

Track:

- Total predictions.
- Wins.
- Losses.
- Pushes.
- Voids.
- Hit rate.
- Average recorded odds.
- Paper units.
- Paper ROI.
- Best-performing markets.
- Worst-performing markets.
- Performance by month.
- Performance by season.
- Performance by odds range.
- Performance by market type.
- Sample size.
- Data completeness.

### Analyst Submission

Allow manual entry of:

- Analyst name.
- Screenshot or source reference.
- Selection.
- Fixture.
- Market.
- Threshold.
- Odds.
- Timestamp.
- Notes.

If screenshot parsing is later added, require human confirmation before saving.

Do not silently guess unreadable lines or prices.

### Analyst Ranking

Avoid ranking analysts only by win percentage.

Show sample size and odds.

Use confidence intervals and clearly distinguish observed results from estimated skill.

Provide filters for:

- Last 7 days.
- Last 30 days.
- Current season.
- All-time.
- Specific market.

### Analyst Comparison

Show:

- Analyst prediction.
- Our independent projection.
- Our probability estimate.
- Actual outcome.
- Recorded bookmaker price.

Never allow an analyst's selection to silently overwrite our independent model output.

---

# PART 12 — ROTOBOT TRACKER

RotoBot is an external parlay-building tool.

It is not our statistical model.

Create a separate RotoBot tracking module.

Support:

- Doubles.
- Trebles.
- Parlays of four or more legs.
- Original displayed odds.
- Individual leg odds.
- Selection screenshots.
- Creation timestamp.
- Game date.
- Leg-by-leg grading.
- Combined parlay grading.

Track two different performance metrics:

1. Complete parlay success rate.
2. Unique individual leg success rate.

Repeated legs must not be double-counted in the unique-leg metric.

Create automatic warnings for:

- Invalid fixtures.
- Incorrect dates.
- Player-team mismatches.
- Missing odds.
- Duplicated legs.
- Unverified market rules.
- Correlated selections.
- Outdated injury information.

Do not multiply individual probabilities to estimate a parlay probability unless independence is justified.

Create a joint-probability framework for correlated selections.

Where dependence cannot be estimated reliably, mark the parlay probability as unavailable.

---

# PART 13 — PAPER PORTFOLIO

Create a virtual paper-testing system.

Default denomination:

1 paper unit = £1 nominal.

This is for consistent measurement only.

No real money changes hands.

Allow:

- Paper singles.
- Paper doubles.
- Paper trebles.
- Paper parlays.
- Virtual units.
- Historical paper returns.
- Daily results.
- Weekly results.
- Monthly results.
- Seasonal results.

Support a default one-unit paper stake for comparable testing.

Allow configurable virtual stake sizes for research experiments.

Keep model accuracy separate from paper portfolio profitability.

A prediction can be correct without being profitable at its recorded odds.

A prediction can lose while still having been statistically reasonable.

Track these distinctions.

### Portfolio Metrics

Show:

- Total virtual entries.
- Total virtual units.
- Net virtual P/L.
- Paper ROI.
- Average recorded odds.
- Maximum drawdown.
- Longest losing streak.
- Market breakdown.
- Source breakdown.
- Season breakdown.

Never display hypothetical results as real betting profits.

---

# PART 14 — POST-GAME REVIEW CENTRE

Create a daily review page.

For each completed game, compare:

- Pre-game prediction.
- Actual result.
- Forecast error.
- Original assumptions.
- Injury information.
- Actual minutes.
- Actual usage.
- Actual opportunities.
- Matchup assumptions.
- Unexpected game events.

The system should identify possible explanations for errors.

Examples:

- Minutes projection too high.
- Player usage lower than expected.
- Opponent pace slower than expected.
- Shooting variance.
- Unexpected foul trouble.
- Blowout reduced playing time.
- Late injury or lineup change.

Distinguish observed facts from hypotheses.

Do not automatically claim that a particular factor caused an outcome without evidence.

Create a structured review workflow:

1. What did we predict?
2. What actually happened?
3. How large was the error?
4. Which assumptions were wrong?
5. Was the error avoidable?
6. Should the model change?
7. What evidence would justify the change?

Store reviews so that recurring errors can be analysed across hundreds of games.

---

# PART 15 — DAILY COMMAND CENTRE

Build a homepage with:

- Today's NBA schedule.
- Completed games.
- Upcoming games.
- Data freshness.
- Player availability warnings.
- Predictions awaiting review.
- Paper entries awaiting settlement.
- Analyst submissions.
- Model status.
- Recent forecast accuracy.
- Latest simulation runs.

Provide a game detail page.

Each game should show:

- Teams.
- Start time.
- Team records.
- Recent results.
- Rest days.
- Available injury information.
- Expected rotations.
- Player statistics.
- Team matchup statistics.
- Model forecasts.
- Simulation results.
- Analyst predictions.
- Paper portfolio entries.
- Post-game results.

Avoid overwhelming the user.

Use progressive disclosure and expandable detail panels.

---

# PART 16 — USER INTERFACE DESIGN

Design a polished, professional analytics dashboard.

Visual direction:

- Modern sports analytics platform.
- Clean typography.
- Strong spacing.
- Dark mode as the primary theme.
- Optional light mode.
- Clear tables.
- Interactive charts.
- Responsive cards.
- Minimal unnecessary animation.

Suggested navigation:

Dashboard
Games
Players
Teams
Model Lab
Simulation Lab
Analysts
RotoBot
Paper Portfolio
Results Review
Model Performance
Data Centre
Learning Centre
Settings

Use clear colour semantics:

- Green for confirmed positive outcomes.
- Red for confirmed negative outcomes.
- Amber for warnings.
- Neutral colours for pending information.

Never use colour as the only way to communicate status.

Include accessible labels and keyboard navigation.

Create reusable components.

Avoid giant single-file React components.

---

# PART 17 — INTERACTIVE PLAYER RESEARCH

Build a player detail page.

Show:

- Current team.
- Position.
- Recent games.
- Minutes.
- Points.
- Rebounds.
- Assists.
- Three-point statistics.
- Season averages.
- Recent averages.
- Variability.
- Home/away splits.
- Rest-day splits where available.
- Opponent matchup history.
- Injury context.
- Model forecasts.

Allow users to select a market and threshold.

Example:

Player: Example Player
Market: Rebounds
Threshold: Over 8.5

The application should display:

- Historical hit rate.
- Sample size.
- Projected mean.
- Estimated probability if modelled.
- Distribution chart.
- Relevant uncertainty.
- Source freshness.

Do not imply that historical hit rate equals future probability.

---

# PART 18 — RESEARCH NOTES

Create a research notebook.

Allow notes to be attached to:

- Games.
- Players.
- Teams.
- Predictions.
- Analysts.
- Model runs.

Support tags such as:

- Injury
- Rotation
- Minutes
- Usage
- Matchup
- Pace
- Rebounding
- Assists
- Shooting
- Data quality
- Model error

Include timestamps and author information.

Preserve the historical context of notes.

---

# PART 19 — OVERVIEW HQ INTEGRATION

NBA Intelligence Lab must eventually communicate with Overview HQ.

Do not modify Overview HQ until its architecture has been inspected.

Design a versioned integration contract.

Suggested endpoints:

GET /api/v1/nba/summary

GET /api/v1/nba/paper-performance

GET /api/v1/nba/model-performance

GET /api/v1/nba/analysts

GET /api/v1/nba/recent-results

GET /api/v1/nba/data-health

Support JSON export as a fallback.

Overview HQ should be able to display:

- NBA paper units.
- NBA paper ROI.
- NBA forecast accuracy.
- Analyst leaderboard.
- Model version.
- Data health.
- Recent results.

Use stable identifiers and consistent timestamps.

Do not combine NBA and NFL model accuracy into one misleading percentage.

Each sport requires its own performance measures.

---

# PART 20 — NFL TESTING CENTRE COMPATIBILITY

Inspect the existing NFL Testing Centre if accessible.

Identify reusable components such as:

- Prediction storage.
- Paper portfolio logic.
- Grading functions.
- Model version tracking.
- Dashboard components.
- User settings.
- Authentication.
- Database utilities.

Share generic components where appropriate.

Keep NBA-specific modelling separate from NFL-specific modelling.

Do not force different sports into the same statistical assumptions.

Potential shared library:

sports-analytics-core

This may eventually contain:

- Prediction schemas.
- Odds mathematics.
- Paper portfolio calculations.
- Analyst tracking.
- Model evaluation.
- Common API contracts.

Do not create this shared library until there is enough working code to justify the abstraction.

---

# PART 21 — MODEL VERSIONING

Every model change must be traceable.

Use semantic model versions.

Examples:

NBA-MODEL-0.1
NBA-MODEL-0.2
NBA-MODEL-1.0

Store:

- Model version.
- Code commit.
- Training data period.
- Feature definitions.
- Hyperparameters.
- Validation results.
- Release date.
- Known limitations.

Support comparison between versions.

Do not overwrite historical forecasts after releasing a new model.

Allow a previous model to remain active as a benchmark.

Only promote a new model when evaluation supports the change.

---

# PART 22 — DATA QUALITY AND SECURITY

Implement:

- Input validation.
- Duplicate detection.
- Database constraints.
- Referential integrity.
- Error logging.
- Secure environment variables.
- Dependency management.
- Basic security checks.
- Database backups.
- Restore instructions.
- Export functionality.
- Import validation.
- Safe migrations.

Avoid logging secrets.

Do not expose private files or API credentials.

Use least-privilege access.

Do not collect unnecessary personal information.

If authentication is added, use a maintained authentication approach rather than inventing custom cryptography.

---

# PART 23 — AUTOMATED TESTING

Write tests for:

- Market parsing.
- Over/under grading.
- Alternative thresholds.
- Push handling.
- Void handling.
- Parlay settlement.
- Unit calculations.
- ROI calculations.
- Break-even probabilities.
- Expected value.
- Duplicate predictions.
- Invalid fixtures.
- Player-team mismatches.
- Data import.
- Forecast reproducibility.
- Simulation reproducibility.
- Model version storage.
- Missing-data behaviour.
- API responses.

Create a small deterministic demonstration dataset.

Clearly identify it as synthetic.

Do not mix synthetic data with real historical performance.

Run tests after each meaningful implementation stage.

Report failing tests and limitations.

---

# PART 24 — CODING EDUCATION

I am learning to code.

Create a Learning Centre inside the documentation.

Explain important concepts using the actual project.

Topics should include:

- Python variables.
- Functions.
- Lists and dictionaries.
- Classes.
- Type hints.
- APIs.
- JSON.
- SQL databases.
- Database relationships.
- Git and GitHub.
- React components.
- TypeScript.
- Statistical averages.
- Variance.
- Probability distributions.
- Monte Carlo simulation.
- Correlation.
- Backtesting.
- Model validation.

For every major feature, provide:

1. What the feature does.
2. Why we need it.
3. Which files implement it.
4. How the code works.
5. How to test it.
6. One small exercise I can try myself.

Use clear explanations without oversimplifying the mathematics.

Do not generate huge amounts of unnecessary tutorial text inside application files.

Keep teaching material in the documentation.

---

# PART 25 — LONG-TERM ROADMAP

Build the platform in phases.

## Version 0.1 — Reliable Foundation

Deliver:

- Working local application.
- Database.
- Team and player records.
- Fixture records.
- Manual prediction entry.
- Analyst tracking.
- Paper portfolio.
- Result grading.
- Basic dashboard.
- CSV import/export.
- Automated tests.
- Documentation.

This must be a usable application.

## Version 0.2 — Data Automation

Add:

- Approved data provider integration.
- Automatic fixture updates.
- Automatic box-score imports.
- Data validation.
- Scheduled result grading.
- Data freshness dashboard.

## Version 0.3 — Baseline Forecasting

Add:

- Player minutes baseline.
- Points baseline.
- Rebounds baseline.
- Assists baseline.
- Team baseline.
- Prediction storage.
- Forecast error analysis.

## Version 0.4 — Simulation Lab

Add:

- Statistical distributions.
- Monte Carlo simulation.
- Configurable simulation counts.
- Reproducible random seeds.
- Scenario analysis.
- Threshold probability calculations.

## Version 0.5 — Advanced Evaluation

Add:

- Walk-forward backtesting.
- Probability calibration.
- Brier score.
- Log loss.
- Model comparisons.
- Confidence intervals.
- Historical performance charts.

## Version 0.6 — Advanced Matchup Research

Add:

- Improved minutes modelling.
- Player role adjustments.
- Opponent context.
- Injury adjustments.
- Rotation scenarios.
- Better correlation modelling.

## Version 0.7 — Analyst Intelligence

Add:

- Advanced analyst comparisons.
- Source reliability.
- Market-specific records.
- RotoBot diagnostics.
- Screenshot-assisted entry.
- Performance trend analysis.

## Version 0.8 — Multi-Sport Integration

Add:

- Overview HQ connection.
- NFL Testing Centre compatibility.
- Shared analytics components.
- Centralised performance reporting.

## Version 0.9 — Reliability and Refinement

Add:

- Performance optimisation.
- Improved error handling.
- Better accessibility.
- Database backup automation.
- More complete documentation.
- Security review.
- Model audit reports.

## Version 1.0 — Stable Research Platform

Deliver a stable, documented, maintainable NBA analytics application suitable for continued multi-season development.

Future versions may investigate machine learning, more sophisticated player distributions, lineup-level modelling and improved data feeds.

Only introduce advanced techniques when they demonstrably improve validation results.

---

# PART 26 — FIRST IMPLEMENTATION TASK

Now begin the actual work.

Follow this order:

### Step 1 — Inspect

Inspect the repository.

Identify:

- Existing files.
- Framework.
- Dependencies.
- Database.
- Tests.
- Existing integration opportunities.

Summarise your findings.

### Step 2 — Plan

Create a concise implementation plan for Version 0.1.

Identify any architectural decisions that require my approval.

If no major blockers exist, proceed.

### Step 3 — Build

Implement a working vertical slice:

1. Initialise the application.
2. Create the database schema.
3. Add database migrations.
4. Build the backend.
5. Build a functional dashboard.
6. Create analyst management.
7. Create prediction entry.
8. Implement market grading.
9. Implement paper portfolio calculations.
10. Add sample data.
11. Add automated tests.

### Step 4 — Verify

Run the application where possible.

Run the test suite.

Fix errors.

Verify that the application works without paid API keys using demonstration data.

### Step 5 — Document

Update:

- README.md
- AGENTS.md
- CHANGELOG.md
- ROADMAP.md

Document installation and local startup commands.

### Step 6 — Report

Tell me:

- What you built.
- Which files you changed.
- What works.
- What is still simulated.
- Which tests passed.
- Any limitations.
- The next three recommended improvements.
- One coding concept I should learn from this implementation.

---

# PART 27 — ACCEPTANCE CRITERIA FOR VERSION 0.1

Version 0.1 is complete only when:

1. The application starts locally.
2. The dashboard loads without errors.
3. Teams and games can be stored.
4. Analysts can be created.
5. Predictions can be entered.
6. Predictions can be linked to games.
7. Markets can be graded correctly.
8. Paper units can be recorded.
9. Paper P/L is calculated correctly.
10. Analyst records update from settled predictions.
11. Doubles and parlays are graded correctly.
12. Missing odds do not produce invented ROI.
13. Invalid fixtures generate warnings.
14. Prediction timestamps are preserved.
15. Historical records are not silently overwritten.
16. Sample data is clearly labelled.
17. Automated tests pass.
18. Setup instructions are provided.
19. No real-money betting functionality exists.
20. The architecture supports future expansion.

---

# PART 28 — FINAL DEVELOPMENT PHILOSOPHY

This project should be built like a serious long-term research system.

We do not want a dashboard that merely looks impressive.

We want a system that produces trustworthy information.

Accuracy matters more than complexity.

Data quality matters more than the number of features.

Good forecasting matters more than running enormous simulations.

Transparent uncertainty matters more than false confidence.

Historical evaluation matters more than short winning streaks.

Maintainability matters more than clever code.

We will improve the platform over multiple seasons.

Preserve compatibility, document changes and avoid unnecessary rewrites.

Treat every prediction as an experiment.

Treat every completed game as new evidence.

Treat every model failure as an opportunity to improve the research process.

**Begin by inspecting the repository, creating the Version 0.1 implementation plan and then implementing the first working version. Do not stop after producing a design document.**
