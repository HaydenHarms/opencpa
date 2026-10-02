# Plan: exam-day mode and the practice split

Hayden's direction (2026-10-02): build a timed mock exam modeled on the real FAR exam, and put a practice session's multiple-choice questions and simulations on separate tabs, as the exam puts them in separate testlets. No calculator: students have their own. Two or three mock exams' worth of distinct simulations is enough to start (Becker offers two).

Three phases, each shippable on its own: **A** the practice tabs, **B** exam mode, **C** the literature panel and research tasks.

## Phase A: questions and simulations on separate tabs

**Done 2026-10-02.** One practice session per section, as before, with its questions and simulations on separate tabs inside it, as the exam puts them in separate testlets. A single simulation is in the Library.

- **Session order:** questions first, then simulations (`spreadThrough` is gone). The diagnostic includes simulations again.
- **Tabs** show "Questions · answered of total" and "Simulations · answered of total". Switching tabs opens that kind's first unanswered item. "Next" goes to the next unanswered item on the same tab, then the other tab, then the results.
- **Library topic sessions** use the same runner, so they get the tabs too.
- **History:** the first version (migration `0007_session_modes`) split Practice into separate question and simulation sessions. Hayden meant tabs inside one session, so `0008_drop_session_modes` removed the column and ended any simulation-only sessions.

## Phase B: exam mode

**Done 2026-10-02.** As designed below, with one change: exams live in their own `exams` table (migration `0009_exams`) instead of `practice_sessions` plus `exam_state`, so practice queries didn't need an exam filter. Pages: `/exam/:section` (intro, the exam) and `/exam/:section/:id` (the report). Code: `packages/engine/src/exam.ts`, `apps/api/src/exams.ts`, `apps/web/src/pages/Exam.tsx`. Items from earlier mock exams are used only once fresh ones run out, even across areas, so the 21 FAR simulations give three exams with no repeat. The connector withholds every item of an unfinished exam, including ones answered earlier in Practice.

### What the student gets

A **Mock exam** entry on the Practice page, with a short page on what to expect, then the exam (the intro doesn't mention a calculator; Hayden had a line about it removed):

- **FAR format:** 5 testlets. Testlets 1 and 2: 25 multiple-choice questions each. Testlets 3, 4 and 5: 2, 3 and 2 simulations. The real exam scores multiple choice and simulations 50/50.
- **Clock:** 4 hours, counting down, run by the server so a refresh or a different device can't reset it. Leaving the page doesn't stop it (as on the real exam), but the student can come back and resume.
- **Pause** (Hayden, 2026-10-02), for studying at home: stops the clock and hides the items until resumed, so it can't be used to work on a question off the clock. The report shows how long and how often the exam was paused, so a student can tell a real-conditions run from a paused one.
- **Optional 15-minute break after testlet 3**, which doesn't count against the clock. Time past 15 minutes does.
- **Within a testlet:** move freely, change answers, flag items for review, strike out choices, and see a navigator showing answered, unanswered and flagged items. Nothing is graded or revealed until the end.
- **Submitting a testlet locks it.** A warning lists unanswered and flagged items first. No going back.
- **Out of time:** the open testlet is submitted as it stands; later testlets score zero.
- **Exam view:** the site's header and nav are hidden; a top bar shows the timer, testlet n of 5 and item n of 25. Simulations use the existing player in a "no feedback" mode.

### The score report

Once the exam ends:

- **Headline:** percent of multiple-choice questions right, percent of simulation points earned, and the two combined 50/50.
- **No 0–99 score.** The AICPA's scaling isn't public, so any scaled number would be invented. The report says so in one line.
- **Breakdowns:** by blueprint area (with the area's blueprint weight), by topic, by skill level, and time used per testlet.
- **Review:** step through every item with its key, rationales and explanation, the same views Practice uses, with the student's flags shown.
- **History:** past mock exams and their scores on the Progress page.

### How items are picked

- **Questions:** 50 by blueprint area weight, spread across topics, preferring items never seen in a mock exam and then never seen at all. No leaning toward weak topics: a mock exam should measure, not drill. Multiple-choice items rotate to new-number versions as Practice does.
- **Simulations:** 7 by area weight, preferring ones not used in an earlier mock exam. With 21 today, the first three mock exams have no repeated simulation; the fourth starts reusing them (the student is told).
- **Testlet difficulty:** the real exam makes testlet 2 harder or easier based on testlet 1. We have no calibrated difficulty, so both testlets are drawn the same way; the intro page says so.

### Answers stay hidden until the end

Today `POST /me/attempts` grades and reveals at once. Exam mode can't use it, or the key would be in the browser mid-exam. So:

- **New routes** under `/me/exams`: start, get the current exam (public items, saved responses, clock), save responses for the open testlet (debounced, so a refresh loses nothing), submit a testlet, start and end the break, pause and resume, and get a finished exam's report. While paused, the current-exam route returns the clock but no items.
- **Submitting a testlet** grades every item on the server and writes the `attempts` rows (tagged with the exam's session id, so mastery and review scheduling count them), but the response holds only "received". Keys come back only from the report route, once the exam is finished.
- **Unanswered items** count as wrong in the exam score but write no attempt, so they stay "unseen" for Practice.
- **The connector:** `get_last_attempt` must not reveal an item from an unfinished exam, and `get_current_question` doesn't serve exam items. Otherwise Claude could be asked for the key mid-exam.
- **Deadline:** every exam route checks the clock first; past it, it submits whatever is saved and ends the exam. A 30-second grace absorbs network lag.

### Data

Migration `0009_exams` (as built; the first draft extended `practice_sessions`):

- A new `exams` table, one row per exam: the testlet layout (item ids per testlet), the current testlet, the start time, break start and end, pause start and total paused time (with a pause count), and the saved responses and flags per item as JSON. Time used is the time since starting, less the break (up to 15 minutes) and pauses.
- Starting a new exam abandons an unfinished one (after a confirmation in the UI); its submitted testlets still count toward mastery.

### Size

About 2–3 working sessions: API and tests first (clock, locking, hidden keys, deadline, connector), then the exam UI, then the report and history. The engine gets a pure `buildExam(pool, history)` with tests, like `selection.ts`.

## Phase C: the literature panel and research tasks

The real exam's simulations include research tasks: find the paragraph of the Codification that answers a question, using a search panel. We have none yet, because a research task needs a literature source.

**The constraint:** FASB's Codification is copyrighted by the Financial Accounting Foundation. Its free Basic View (asc.fasb.org, free registration) doesn't permit copying paragraphs, and the AICPA licenses the full text for the exam. We can't put paragraphs into an open-source, CC BY-SA repo.

**What we can do:**

- **An index of the paragraphs our content cites:** each entry has the paragraph number, the topic and subtopic titles, and an original plain-English summary we write ourselves (not a paraphrase of FASB's wording), plus a link to that paragraph in FASB's free Basic View.
- **The literature panel** searches that index by keyword, in the browser like the Library search, and is available in every simulation testlet and in Practice.
- **Research tasks** ask for the paragraph that answers a question. The student finds it through our index, or in the Basic View if they have an account.
- **Verification:** the blind verifier can't log in to the Basic View, so every paragraph number is checked against two public firm guides (PwC Viewpoint, Deloitte DART, KPMG or EY handbooks quote paragraph numbers). Anything that can't be confirmed twice is left out.
- **Scope:** start with the paragraphs FAR's existing explanations already cite (about 150–250), then write one research simulation per blueprint area as a content batch (far-tbs-research-01) through the usual pipeline. GASB has the same copyright issue and comes after FASB.

**Size:** the panel is about a day. The index and research tasks are content work: about two batches.

## Not doing (for now)

- **The calculator** (students have their own).
- **Adaptive testlet difficulty** (needs calibrated item difficulty).
- **A scaled score.**
- **Other sections:** exam mode is built from a per-section layout config, so BAR, AUD and REG are a config entry once they have enough content.
- **A half-length exam:** easy to add later from the same layout config if students ask.

## Order

1. Phase A (practice tabs).
2. Phase B (exam mode).
3. Phase C (literature panel and research tasks), after or alongside far-tbs-05.

Update `CLAUDE.md` (roadmap step 9), `README.md`, `docs/history.md`, and the Privacy page if the data stored changes, as each phase ships.
