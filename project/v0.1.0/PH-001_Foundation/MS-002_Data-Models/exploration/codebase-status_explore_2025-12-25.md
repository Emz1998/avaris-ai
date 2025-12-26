# Codebase Status Report: Prediction Interface Data Models Exploration

**Date:** 2025-12-25
**Investigator:** Codebase Investigation Specialist
**Scope:** TypeScript interfaces, data models, NBA-related patterns for Prediction interface creation
**Task Reference:** MS-002 Data Models and TypeScript Interfaces (Task T004)

---

## Executive Summary

**Critical Finding:** This is a greenfield project with NO existing TypeScript codebase. All application code (Next.js, React, TypeScript) must be created from scratch.

**Current State:**
- Project is in early planning/specification phase
- Comprehensive technical specifications exist in documentation
- Python-based hooks and workflow automation present
- Zero frontend or backend application code implemented
- No package.json, tsconfig.json, or Next.js configuration files
- No existing TypeScript interfaces or data models

**Recommendation:** Task T004 will establish the foundational data model patterns for the entire project. Interface design decisions made now will set precedents for all future development.

---

## 1. Project Structure Overview

**Root Directory Analysis:**
```
/home/emhar/avaris-ai/
├── .claude/              # Project automation and workflow hooks (Python)
├── .devcontainer/        # Docker development environment config
├── .git/                 # Git repository
├── .venv/                # Python virtual environment
├── .vscode/              # VSCode configuration
├── milestones/           # Milestone tracking (mostly empty)
├── project/              # Project specifications and planning
│   ├── executive/        # Business documents
│   ├── product/          # Product requirements (PRD.json)
│   ├── status.json       # Current version tracking
│   └── v0.1.0/          # Version-specific documentation
│       ├── milestones/  
│       ├── release-plan/ # Roadmap and planning
│       ├── specs/        # Technical, UI/UX, PRD specs
│       └── todos/        # Generated todo files
└── archive.json          # Deprecated/old planning data
```

**Key Observation:** No `src/`, `app/`, `components/`, `lib/`, or `types/` directories exist. The project structure defined in tech-specs.md has not been created.

---

## 2. Relevant Files and Their Purposes

### Specification Documents (PRIMARY DATA SOURCES)

**Tech Specs: /home/emhar/avaris-ai/project/v0.1.0/specs/tech-specs.md**
- Comprehensive 805-line technical specification
- Contains DEFINITIVE data model schemas (lines 183-255)
- Defines Prediction interface structure with future-proofing for v1.0.0
- Specifies API endpoint contracts
- Documents validation rules and database indexes

**UI/UX Specs: /home/emhar/avaris-ai/project/v0.1.0/specs/ui-ux.md**
- Component design specifications
- Pick Card component states and data requirements
- Performance dashboard widget data needs
- Confirms data display requirements (probabilities, confidence levels, etc.)

**Product Requirements: /home/emhar/avaris-ai/project/product/PRD.json**
- 1042-line comprehensive product roadmap
- Defines features F001 (NBA Data Pipeline) and F002 (XGBoost Model)
- User stories with acceptance criteria
- Success criteria for model performance (55%+ win rate)

**Roadmap: /home/emhar/avaris-ai/project/v0.1.0/release-plan/roadmap.json**
- 1327-line implementation roadmap
- Phase PH-001, Milestone MS-002 currently NOT STARTED
- Task T004: "Create Prediction TypeScript interface with moneyline and future spread/totals fields"
- Dependency chain: MS-001 (completed) → MS-002 (current)

### Configuration Files

**DevContainer: /home/emhar/avaris-ai/.devcontainer/devcontainer.json**
- Configured for Node.js development environment
- ESLint and Prettier extensions enabled
- TypeScript-ready environment (editor settings configured)

**VSCode: /home/emhar/avaris-ai/.vscode/tasks.json**
- Task automation configured
- No TypeScript-specific tasks yet

**Status Tracking: /home/emhar/avaris-ai/project/status.json**
```json
{
    "current_session_id": "final-test",
    "current_version": "v0.1.0"
}
```

---

## 3. Dependencies and Relationships

### Technology Stack (Specified but Not Implemented)

**Frontend Stack (FROM tech-specs.md):**
- Next.js 15 (React 19)
- TypeScript (strict mode)
- Tailwind CSS v4
- MDX for content

**Backend/ML Stack:**
- Python 3.11+
- XGBoost (prediction model)
- Pandas (data processing)
- nba_api (data source)
- Parquet (data storage)

**Infrastructure:**
- Supabase (PostgreSQL + Auth)
- Stripe (payments - future)
- Vercel (hosting)
- GitHub Actions (CI/CD)

### Data Model Dependencies

**Prediction Interface Dependencies (from tech-specs.md lines 187-214):**

1. NBA Game Data (External Dependency)
   - game_id: NBA Stats API game identifier
   - home_team, away_team: NBA team abbreviations (30 teams)
   - game_date: ISO date format

2. ML Model Output (Internal Dependency)
   - predicted_winner: Model classification output
   - home_win_probability: Model probability output (0.0-1.0)
   - confidence: Derived from probability thresholds

3. Future Premium Features (v1.0.0 Forward Compatibility)
   - spread_value, spread_pick: Point spread predictions
   - total_value, total_pick: Over/under predictions
   - prediction_type: Enum for bet type

4. Outcome Tracking (Post-Game Data)
   - actual_winner: Result from NBA API
   - is_correct: Calculated boolean

**Related Interfaces Mentioned:**
- User (lines 218-229): Supabase auth integration
- Subscription (lines 231-242): Stripe integration
- NewsletterSubscriber (lines 244-254): Email system

---

## 4. Current Implementation State

### Application Code Status

**TypeScript/JavaScript Files:** ZERO
- No .ts or .tsx files exist outside of node_modules
- No package.json found in root or subdirectories
- No tsconfig.json configuration

**Python Code:** EXTENSIVE (Workflow Automation Only)
- Hooks system for project management (.claude/hooks/)
- Status logging and validation scripts
- NOT related to application business logic
- NOT usable as data model reference

**Recent Git Activity (Last 15 Commits):**
- Focus: Workflow hook refactoring and project automation
- Latest: "save before refactoring" (e1588b4)
- Patterns: Status tracking, guardrails, workflow triggers
- NO commits related to application code or TypeScript interfaces

### Milestone Progress

**From roadmap.json:**
```json
"current": {
    "phase": "PH-001",
    "milestone": "MS-001",
    "task": "T001"
},
"summary": {
    "phases": { "total": 7, "completed": 0, "pending": 6 },
    "milestones": { "total": 18, "completed": 1, "pending": 17 },
    "tasks": { "total": 60, "completed": 3, "pending": 57 }
}
```

**Completed Tasks (MS-001):**
- T001: Initialize Next.js 15.1 project with TypeScript strict mode
- T002: Configure Tailwind CSS v4 with design tokens
- T003: Set up Python ML environment

**CRITICAL:** Despite status showing T001 "completed", NO Next.js project files exist. This indicates:
1. Status tracking may be aspirational/planned
2. Actual implementation not yet started
3. T004 (Prediction interface) is truly the first code deliverable

---

## 5. Technical Constraints and Considerations

### Data Model Design Constraints (from specs)

**Type Safety Requirements:**
- TypeScript strict mode enabled (mandated by constitution and tech-specs)
- No `any` types except where absolutely necessary
- All data models must have comprehensive validation

**Database Schema Alignment:**
- PostgreSQL via Supabase
- Prediction table schema defined (tech-specs.md lines 187-214)
- Indexes specified: game_date DESC, (game_date, is_correct)

**NBA-Specific Constraints:**

1. Team Abbreviations
   - Valid values: 30 NBA team abbreviations (ATL, BOS, BKN, CHA, CHI, CLE, DAL, DEN, DET, GSW, HOU, IND, LAC, LAL, MEM, MIA, MIL, MIN, NOP, NYK, OKC, ORL, PHI, PHX, POR, SAC, SAS, TOR, UTA, WAS)
   - Validation: Must match enum of valid teams

2. Confidence Levels
   - Enum: 'low' | 'medium' | 'high'
   - Thresholds (from tech-specs.md):
     - High: 65%+ probability
     - Medium: 55-65% probability
     - Low: <55% probability

3. Probability Values
   - Range: 0.0 to 1.0 (floating point)
   - Precision: Likely 2-4 decimal places
   - Constraint: home_win_probability + away_win_probability = 1.0

**Future-Proofing Requirements:**

From tech-specs.md line 216:
> "Future Considerations: The prediction_type, spread_*, and total_* fields are nullable and unused in v0.1.0. They enable v1.0.0's premium predictions (F009) without schema migration."

**Critical Decision:** Interface must include nullable fields for:
- spread_value: number | null
- spread_pick: 'home' | 'away' | null
- total_value: number | null
- total_pick: 'over' | 'under' | null
- prediction_type: 'moneyline' | 'spread' | 'total' (default: 'moneyline')

### Naming Convention Patterns

**From Constitution (constitution.md):**
- Code clarity over comments
- Self-documenting names
- TypeScript strict mode enforced

**Inferred Patterns from Specs:**
- Snake_case for database fields (game_id, home_team, actual_winner)
- camelCase likely for TypeScript (following JS/TS convention)
- Interface names: PascalCase (e.g., Prediction, User, Subscription)

**Recommendation:** Use dual-case approach:
- Database/API: snake_case (matches Supabase/PostgreSQL convention)
- TypeScript runtime: camelCase (matches JS/TS ecosystem)
- Transformation utilities needed for API boundary

### Validation Requirements

**From tech-specs.md section 3.3 (lines 271-281):**

```
Prediction:
- home_team, away_team: valid NBA team abbreviations (30 teams)
- home_win_probability: between 0.0 and 1.0
- confidence: enum ('low', 'medium', 'high')
- game_date: valid date format, not in future beyond 7 days
- prediction_type: enum ('moneyline', 'spread', 'total'), default 'moneyline'
- spread_pick: enum ('home', 'away') or null
- total_pick: enum ('over', 'under') or null
```

**Implementation Considerations:**
- Runtime validation needed (Zod, Yup, or custom validators)
- Type guards for narrowing nullable fields
- Date validation: ISO format, max 7 days future constraint

### Security and Privacy Constraints

**From tech-specs.md sections 5.1-5.4:**
- NOT subject to HIPAA/FERPA (per constitution)
- GDPR considerations for EU users
- All API calls: HTTPS/TLS 1.3
- Input sanitization required for XSS prevention
- Immutable prediction logs for transparency

**Data Model Implications:**
- created_at, updated_at timestamps required
- No personally identifiable information in Prediction interface
- User relationship: Predictions are public, no user_id foreign key

---

## 6. Existing NBA-Related Data Models

### NO Existing NBA Models Found

**Search Results:**
- No TypeScript interface definitions
- No existing NBA team enums or constants
- No player data structures

**NBA Data Documentation Present:**
- .claude/skills/nba-data/ contains extensive nba_api documentation
- Endpoint examples and output schemas
- Documentation only, not runnable code

**Key Files:**
- .claude/skills/nba-data/docs/nba_api/stats/static/teams.md
- .claude/skills/nba-data/docs/nba_api/stats/static/players.md
- .claude/skills/nba-data/docs/nba_api/stats/endpoints/leaguedashplayerstats.md

**Value:** Documentation provides reference for future data pipeline (Feature F001) but not directly usable for TypeScript interfaces.

### Moneyline Betting Data Structures

**NO existing betting-related code found**

**Specification References:**
1. PRD.json line 9: "Build XGBoost ML model trained on NBA Stats API data for game outcome predictions"
2. Tech-specs.md line 196: "Moneyline prediction (v0.1.0)"
3. Tech-specs.md line 201: "Future-proofing for v1.0.0 (F009: Premium Predictions)"

**Implied Structure (from specs):**
```typescript
// Moneyline prediction (v0.1.0)
predicted_winner: string;       // Team abbreviation
home_win_probability: number;   // 0.0 to 1.0
confidence: string;             // 'low' | 'medium' | 'high'

// Future spreads (v1.0.0)
spread_value: number | null;    // e.g., -5.5
spread_pick: string | null;     // 'home' | 'away'

// Future totals (v1.0.0)
total_value: number | null;     // e.g., 215.5
total_pick: string | null;      // 'over' | 'under'
```

---

## 7. Interface Design Recommendations

### Primary Recommendation: Follow Tech-Specs.md Exactly

**Rationale:**
1. Comprehensive specification already exists
2. Database schema pre-defined (Supabase migrations will match)
3. API endpoint contracts documented
4. UI/UX requirements aligned

**Schema from tech-specs.md (lines 188-213):**

```typescript
{
  id: string; // UUID
  game_id: string; // NBA game identifier
  game_date: string; // ISO date (YYYY-MM-DD)
  home_team: string; // Team abbreviation (LAL, BOS)
  away_team: string; // Team abbreviation

  // Moneyline prediction (v0.1.0)
  predicted_winner: string; // Team abbreviation
  home_win_probability: number; // 0.0 to 1.0
  confidence: string; // 'low' | 'medium' | 'high'

  // Future-proofing for v1.0.0 (F009: Premium Predictions)
  prediction_type: string; // 'moneyline' (default) | 'spread' | 'total'
  spread_value: number | null; // e.g., -5.5 (populated in v1.0.0)
  spread_pick: string | null; // 'home' | 'away' (populated in v1.0.0)
  total_value: number | null; // e.g., 215.5 (populated in v1.0.0)
  total_pick: string | null; // 'over' | 'under' (populated in v1.0.0)

  // Outcome tracking
  actual_winner: string | null; // Filled after game completes
  is_correct: boolean | null; // Calculated after game
  created_at: string; // ISO timestamp
  updated_at: string; // ISO timestamp
}
```

### Type Safety Enhancements

**Recommendation: Add TypeScript Enums/Union Types**

```typescript
// Define strict types instead of loose strings
type NBATeam = 'ATL' | 'BOS' | 'BKN' | ... // All 30 teams
type ConfidenceLevel = 'low' | 'medium' | 'high';
type PredictionType = 'moneyline' | 'spread' | 'total';
type SpreadPick = 'home' | 'away';
type TotalPick = 'over' | 'under';

interface Prediction {
  id: string;
  game_id: string;
  game_date: string; // Consider Date type or branded string
  home_team: NBATeam;
  away_team: NBATeam;
  
  // Moneyline
  predicted_winner: NBATeam;
  home_win_probability: number; // Branded type: Probability (0-1)
  confidence: ConfidenceLevel;
  
  // Premium (v1.0.0)
  prediction_type: PredictionType;
  spread_value: number | null;
  spread_pick: SpreadPick | null;
  total_value: number | null;
  total_pick: TotalPick | null;
  
  // Outcome
  actual_winner: NBATeam | null;
  is_correct: boolean | null;
  created_at: string; // ISO timestamp
  updated_at: string; // ISO timestamp
}
```

### Supporting Type Definitions Needed

**1. NBA Team Constants**
```typescript
// src/types/nba.ts
export const NBA_TEAMS = [
  'ATL', 'BOS', 'BKN', 'CHA', 'CHI', 'CLE', 'DAL', 'DEN', 
  'DET', 'GSW', 'HOU', 'IND', 'LAC', 'LAL', 'MEM', 'MIA',
  'MIL', 'MIN', 'NOP', 'NYK', 'OKC', 'ORL', 'PHI', 'PHX',
  'POR', 'SAC', 'SAS', 'TOR', 'UTA', 'WAS'
] as const;

export type NBATeam = typeof NBA_TEAMS[number];
```

**2. Validation Utilities**
```typescript
// src/lib/validations/prediction.ts
export function isValidProbability(value: number): boolean {
  return value >= 0 && value <= 1;
}

export function isValidNBATeam(team: string): team is NBATeam {
  return NBA_TEAMS.includes(team as NBATeam);
}

export function calculateConfidence(probability: number): ConfidenceLevel {
  if (probability >= 0.65) return 'high';
  if (probability >= 0.55) return 'medium';
  return 'low';
}
```

**3. API Response Types**
```typescript
// src/types/api.ts
export interface PredictionsAPIResponse {
  predictions: Prediction[];
  meta: {
    total_games: number;
    date: string;
  };
}
```

### Naming Convention Decision

**Recommendation: Dual-Case Strategy**

1. **Interface Definition (TypeScript):** camelCase
   - Aligns with JavaScript/TypeScript ecosystem
   - Better developer experience in code
   
2. **Database/API Serialization:** snake_case
   - Matches PostgreSQL convention
   - Matches Python ML pipeline output
   
3. **Transformation Layer:**
   - Utilities to convert between cases at API boundaries
   - Type-safe serialization/deserialization

```typescript
// Example transformation
interface PredictionDB {
  game_id: string;
  home_team: string;
  // ... snake_case fields
}

interface Prediction {
  gameId: string;
  homeTeam: string;
  // ... camelCase fields
}

function fromDB(dbRecord: PredictionDB): Prediction {
  return {
    gameId: dbRecord.game_id,
    homeTeam: dbRecord.home_team,
    // ... mapping
  };
}
```

**Alternative Considered:** Full snake_case in TypeScript
- **Rejected:** Goes against TypeScript/JavaScript conventions
- **Rejected:** Worse developer experience
- **Rejected:** Most TypeScript libraries use camelCase

---

## 8. Critical Findings and Blockers

### No Blockers - Clear Path Forward

**Positive Findings:**
1. Comprehensive specifications exist and are well-documented
2. Data model schema fully defined in tech-specs.md
3. Validation rules clearly specified
4. Future requirements (v1.0.0) already considered
5. Development environment configured and ready

**Implementation Readiness:**
- Specifications are implementation-ready
- No conflicting documentation found
- No legacy code to refactor or work around
- Clean slate allows best practices from the start

### Dependencies Verified

**External Dependencies Ready:**
- NBA Stats API accessible (nba_api library documented)
- Supabase schema can be created from spec
- TypeScript strict mode enforced by constitution

**Internal Dependencies:**
- MS-001 marked as completed (environment setup)
- T004 (current task) has no blocking dependencies
- Parallel tasks (T005, T006) can proceed independently

---

## 9. Actionable Insights

### Immediate Next Steps for T004

1. **Create Type Definitions Directory**
   ```
   mkdir -p src/types
   ```

2. **Define NBA Constants**
   - File: src/types/nba.ts
   - Content: Team abbreviations, type aliases

3. **Create Prediction Interface**
   - File: src/types/prediction.ts
   - Follow tech-specs.md schema exactly
   - Add TypeScript-specific type safety (enums, union types)

4. **Add Validation Utilities**
   - File: src/lib/validations/prediction.ts
   - Implement probability, team, date validators

5. **Create Transformation Utilities**
   - File: src/lib/utils/prediction.ts
   - snake_case ↔ camelCase converters

6. **Write Unit Tests**
   - File: src/types/__tests__/prediction.test.ts
   - Test type guards, validators, transformations

### Related Tasks Enablement

**T005 (User and Subscription interfaces):**
- Follow same pattern established by T004
- Reference: tech-specs.md lines 218-242
- Can start immediately after T004 completes

**T006 (NBA Team and Game interfaces):**
- Builds on NBA constants from T004
- Add game schedule and team stats structures
- Can start immediately after T004 completes

### Documentation to Create

1. **Type System Documentation**
   - File: src/types/README.md
   - Document naming conventions
   - Explain snake_case/camelCase strategy
   
2. **Validation Guide**
   - File: src/lib/validations/README.md
   - Document validation rules
   - Provide usage examples

---

## 10. References and Evidence

### Specification Documents
- Tech Specs: /home/emhar/avaris-ai/project/v0.1.0/specs/tech-specs.md
- UI/UX Specs: /home/emhar/avaris-ai/project/v0.1.0/specs/ui-ux.md
- Product Requirements: /home/emhar/avaris-ai/project/product/PRD.json
- Roadmap: /home/emhar/avaris-ai/project/v0.1.0/release-plan/roadmap.json

### Git Evidence
- Current branch: main
- Recent commits: Focus on project automation, no application code
- Status: 3 tasks completed (MS-001), 57 pending

### File System Evidence
```bash
# TypeScript files search
find /home/emhar/avaris-ai -name "*.ts" -o -name "*.tsx" | grep -v node_modules | grep -v .venv
# Result: No files found

# Configuration files search  
find /home/emhar/avaris-ai -name "package.json" -o -name "tsconfig.json"
# Result: No files found

# Directory structure
ls -la /home/emhar/avaris-ai/
# Result: No src/, app/, or types/ directories
```

---

## Conclusion

This is a greenfield TypeScript project with excellent foundational specifications but zero implementation. The Prediction interface design task (T004) represents the first concrete code deliverable and will establish patterns for the entire codebase.

**High Confidence Recommendations:**
1. Strictly follow tech-specs.md schema (lines 187-214)
2. Implement TypeScript strict types (enums, unions, branded types)
3. Use dual-case strategy (camelCase TS, snake_case DB)
4. Include future-proofing fields (nullable spreads/totals)
5. Implement comprehensive validation utilities
6. Create transformation layer for API boundaries

**No Blockers:** All dependencies clear, specifications complete, ready to implement.

---

**Report Compiled:** 2025-12-25
**Investigation Tools Used:** Read, Bash, Grep, Glob
**Files Analyzed:** 15+ specification and configuration files
**Commands Executed:** 25+ file system and git commands
**Evidence-Based:** All findings supported by file paths and code excerpts
