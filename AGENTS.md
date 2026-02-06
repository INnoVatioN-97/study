# Repository Guidelines

## Repository Purpose
This repository serves two goals: a study archive for seminars/educational content and a portfolio showcase of technical achievements. Keep changes aligned with both purposes, and prioritize presentation quality.

## Project Structure & Module Organization
This repo is a collection of static, presentation-style assets and portfolio pages. Key locations:
- `portfolio/`: HTML/CSS portfolio pages and config (`portfolio-config.js`).
- `careerDetail/`: Resume-style pages (`index.html`, `v2.html`) and stylesheets.
- `seminar/`: Seminar materials, e.g. `seminar/apacheKafka/` with HTML slides and `README.md`.
- `archive/`: Older or experimental portfolio versions.
- `images/` and `references/`: Media assets and reference documents (many filenames are Korean—preserve them).

## Build, Test, and Development Commands
There is no build system or package manager. Files are static and can be opened directly.
- `python3 -m http.server` (from repo root) serves pages locally for quick preview.
- Open a specific page in the browser, e.g. `portfolio/portfolio-ppt2.html` or `careerDetail/index.html`.

## Coding Style & Naming Conventions
- Indentation: 2 spaces in HTML/CSS/JS for consistency with existing files.
- Keep HTML single-page structure and inline scripts minimal; prefer linking CSS files when styles grow.
- Naming: Use kebab-case for new asset filenames and CSS classes (e.g. `portfolio-theme-ref.css`).
- Do not rename or normalize Korean filenames unless explicitly required; many files are referenced by name.

## Testing Guidelines
No automated tests are configured. Validate changes by opening relevant HTML files in a browser and checking layout, responsiveness, and asset loading. If you add scripts or dynamic behavior, document the manual verification steps here.

## Content & Language Notes
- Many documents are in Korean; preserve existing language and terminology unless the request is to translate.
- Portfolio and seminar content highlight performance optimization, real-time systems, and Kafka-related topics. Maintain consistency with those themes when editing related pages.
- Avoid altering reference PDFs and images; update links or HTML instead.

## Commit & Pull Request Guidelines
Recent history uses lightweight Conventional Commit prefixes: `fix:`, `refactor:`, `wip:` with short Korean descriptions. Follow the same pattern for new commits.
- Example: `fix: 여백이슈 수정`
Pull requests should include:
- A short summary of changed pages and directories.
- Screenshots for visual changes (desktop and mobile if layout changes).
- Notes about any renamed/moved assets and updated references.

## Configuration & Assets
Large binaries live under `images/` and `references/`. Avoid duplicating assets; reuse existing files when possible and keep file sizes reasonable for web delivery.
