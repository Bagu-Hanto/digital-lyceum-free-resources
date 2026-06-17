# Digital Lyceum — Free Resources

Practical tools for studying and working with AI. Each file is free to download and use.

---

## Resources

### AI Tutor Workflow
A drop-in study system for any certification or exam. Hand this file to your AI (Claude, ChatGPT, Gemini — any of them), upload or paste it, and type `begin`. The AI walks you through onboarding and then runs a daily study workflow built around spaced repetition, block-gate progression, and cross-resource coordination.

**Who it's for:** Anyone studying for a cert, license, or exam who wants structure without paying for a course or coach.

- `ai-tutor-workflow.md` — paste into any AI chat
- `ai-tutor-workflow.pdf` — formatted download

### tomd — Document to Token-Lean Markdown
A command-line tool that converts `.pdf`, `.docx`, `.pptx`, and `.xlsx` files into token-efficient Markdown optimized for LLM input. Every conversion produces a faithful render and a stripped-down `_lean.md` version that costs a fraction of the tokens to process. Works on Linux and macOS.

Originally created by [Ari Evergreen](https://www.skool.com/@ari-evergreen?g=cliefnotes). Cross-platform port by Joseph Kemp — swapped Apple Vision OCR for Tesseract + pdf2image so it runs on Linux.

- `tomd/` — full source, README, and install instructions

### AIOS — AI Operating System Framework — *COMING SOON*
A personal AI operating system built on one principle: structure does the work that code usually does. Instead of prompt chains or multi-agent frameworks, you organize your context as a filesystem hierarchy — numbered folders for life domains, plain markdown files for prompts and memory, local scripts for the mechanical work. One AI agent reading the right files at the right moment does what most people think requires a complex system to pull off.

Includes the full 3-layer architecture (OS layer, content layer, infrastructure layer), the intent translation framework for closing the gap between what you want and what AI can execute, and a starter kit based on a real implementation that has been running daily since early 2026.

---

## Coming Soon

### Inbox Capture and Processing — *COMING SOON*
A daily capture system for AI-heavy workflows. One inbox for everything — notes, links, code snippets, dropped files, half-formed ideas. At the end of each day, you run a triage pass with your AI: each item gets routed to its real home, queued as a task, or deleted. Nothing falls through the cracks, and nothing stays in the inbox longer than it should.

### System / Project Maintenance Queue — *COMING SOON*
A recurring task tracker for ongoing projects and system upkeep. Keeps maintenance work, low-urgency housekeeping, and standing tasks visible in one place without letting them crowd your active project list. Work it on a schedule with your AI — review, prioritize, execute, and close out items one at a time.

### Session Wrap Up — *COMING SOON*
An end-of-session protocol for AI-assisted work. Sweeps the inbox, writes a session log entry, refreshes your next action, and updates the status on any project touched that session. Leaves you with a clean, documented pick-up point so the next session starts in 30 seconds instead of 10 minutes of re-orienting.

### Session Checkpoint — *COMING SOON*
A mid-session save for long AI work sessions. Logs what was worked on, captures any decisions made, and refreshes your next concrete action — without a full close-out. Useful when you need to pause mid-task, hand off context, or just make sure progress is recorded before a long stretch of deep work. Pairs naturally with Session Wrap Up at end of day.

---

*Built by [Joseph Kemp](https://digitallyceum.netlify.app) — practical AI education for people who learn by doing.*
