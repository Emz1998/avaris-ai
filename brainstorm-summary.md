# Brainstorming Session Summary

## Topic

**NBA Game Winner Prediction App with XGBoost Model**

Building an XGBoost-powered prediction service for NBA game outcomes, starting with moneyline predictions and expanding to spreads, totals, and other bet types. Monetization through ad revenue initially, transitioning to subscriptions and a "prediction bot" product once the model is proven.

---

## Key Decisions

### Target Audience
- **Mixed audience approach**: Tiered service serving casual bettors with basic picks and serious bettors with advanced analytics
- **Key differentiator**: Track record transparency and accountability - publicly display historical performance with no cherry-picking

### Product Vision

#### MVP Phase (Ad-Supported Blog)
- Daily picks website styled as a blog with SEO-optimized articles
- Format: "Lakers vs Celtics Prediction - Jan 15" style posts for search traffic
- Today's picks front and center on homepage with probability percentages
- Performance dashboard showing win rate, ROI, recent results
- Monetization: Google AdSense initially → affiliate links → programmatic ad networks as traffic grows

#### Growth Phase (Subscriptions + Bot)
- Transition trigger: **55%+ win rate over 100+ picks** (proven performance milestone)
- Premium features:
  - Spread & totals predictions (moneyline stays free)
  - API access for power users
  - Early access to picks before line movements
  - **"Prediction Bot"** - Desktop app/CLI tool users download and run locally (like sneaker bots)
- Pricing: Monthly subscription model for recurring revenue

### Tech Stack

| Component | Choice | Rationale |
|-----------|--------|-----------|
| Frontend | Next.js + React 19 + TypeScript + Tailwind v4 | Aligned with existing expertise and constitution |
| CMS | MDX files in Next.js | Version controlled, auto-generated daily posts |
| Auth | Supabase | PostgreSQL for complex queries on performance data |
| Payments | Stripe | Industry standard for subscriptions |
| ML Pipeline | Hybrid approach | Train locally/batch, deploy lightweight inference API |
| Data Storage | Parquet files initially | Scale to database when data grows |
| Orchestration | Cron jobs / GitHub Actions | Simple scheduled pipeline for daily predictions |
| Experiment Tracking | Defer MLflow/W&B | Add later when running many experiments or collaborating |

### Data Strategy
- **Primary source**: NBA Stats API (free, rate-limited)
- **Supplementary**: Custom web scraping for injuries, contextual data
- **No paid data providers initially** - start lean, upgrade if needed

---

## XGBoost Model Strategy

### Feature Categories (All Prioritized)
1. **Team performance metrics**: Win rates, point differentials, offensive/defensive ratings, recent form (L5, L10)
2. **Player-level statistics**: Key player stats, injury reports, rest days, usage rates, plus/minus
3. **Situational factors**: Home/away splits, back-to-backs, travel distance, division/conference matchups
4. **Advanced analytics**: Pace, true shooting %, effective FG%, four factors

### Training Approach
- **Daily retraining**: Model updates nightly with latest results to capture current season dynamics
- **Rolling window**: Focus on current season data to reflect team strengths now

### Validation Strategy
1. **Backtesting**: Test on 2022-23, 2023-24 seasons to check for overfitting
2. **Paper trading**: Run predictions privately for several weeks before publishing
3. **Cross-validation**: Time-series CV, track accuracy, log loss, calibration metrics

### Launch Criteria
- **55%+ win rate** over 50+ predictions (beats ~52.4% break-even accounting for vig)

---

## Growth & Marketing Strategy

### Traffic Acquisition
1. **SEO optimization** (primary): Target keywords like "[Team A] vs [Team B] prediction [date]"
2. **Social media**: Twitter/X and Reddit presence in NBA betting communities
3. **Email newsletter**: Daily picks digest, build owned audience for future subscription conversion

### Content Pipeline
- **Automated daily posts**: Model runs nightly → generates MDX blog post → review and publish each morning
- **SEO-optimized format**: Rich content for each matchup to rank in search

---

## Roadmap

### Phase 1: MVP (Ad-Supported Blog)
- [ ] Build XGBoost model with core features
- [ ] Backtest on historical seasons
- [ ] Paper trade current season
- [ ] Build Next.js blog with daily picks pages
- [ ] Implement performance tracking dashboard
- [ ] Set up automated prediction pipeline (cron/GitHub Actions)
- [ ] Integrate Google AdSense
- [ ] Launch when 55%+ win rate achieved

### Phase 2: Growth (Prove & Scale)
- [ ] SEO optimization for game prediction keywords
- [ ] Build social media presence
- [ ] Launch email newsletter
- [ ] Track and display public performance record
- [ ] Transition to affiliate links
- [ ] Upgrade to programmatic ad networks at 10k+ monthly visitors

### Phase 3: Monetization (Subscriptions + Bot)
- [ ] Build subscription tiers with Stripe
- [ ] Add spread & totals predictions (premium)
- [ ] Develop prediction API
- [ ] Build desktop "prediction bot" application
- [ ] Launch premium subscription tiers
- [ ] Early access feature for premium users

### Deferred (Future Phases)
- Mobile apps & push notifications
- Advanced analytics UI (feature importance, explainability)
- Multi-sport expansion (NFL, MLB, NHL)
- Social features & leaderboards
- Educational content

---

## 12-Month Goal

**Profitable NBA picks service** with:
- Proven model (55%+ win rate)
- 5k+ monthly visitors
- $1k-5k MRR from ads + early subscribers

---

## Session Notes

- **Start simple, scale when needed**: Parquet over databases, cron over Airflow, AdSense over affiliate networks initially
- **Prove before monetizing**: Ad-supported model first to build track record, then transition to subscriptions with credibility
- **"Prediction bot" is unique positioning**: Desktop app model similar to sneaker bots creates exclusivity and perceived value
- **Transparency is the moat**: In a market full of tout services with questionable track records, verifiable public performance is the differentiator

---

**Session Date**: 2025-12-13
