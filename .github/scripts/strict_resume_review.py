#!/usr/bin/env python3
import argparse
import os
import re
from pathlib import Path

BANNED_SOFT_WORDS = [
    "열심히", "성실", "책임감", "최선을", "다양한 경험", "많은 경험",
    "문제 해결 능력", "커뮤니케이션 능력", "협업 능력", "성장", "도전"
]

ACTION_VERBS = [
    "개선", "최적화", "설계", "구축", "도입", "자동화", "리팩터링", "분석", "운영", "배포", "전환", "감소", "증가"
]

METRIC_PATTERN = re.compile(r"(\d+\s*%|\d+\s*(ms|초|분|시간|건|개|명|회|배|원)|[0-9]+\.[0-9]+)")


def read_files_from_list(file_path: Path):
    if not file_path.exists():
        return []
    return [line.strip() for line in file_path.read_text(encoding="utf-8").splitlines() if line.strip()]


def analyze_html(path: Path):
    text = path.read_text(encoding="utf-8", errors="ignore")
    lowered = text.lower()

    issues = []
    warnings = []
    score = 100

    # Basic SEO/structure checks
    if "<title" not in lowered:
        issues.append("`<title>` 태그 없음")
        score -= 12
    if "name=\"description\"" not in lowered and "name='description'" not in lowered:
        warnings.append("meta description 없음")
        score -= 5
    if "<h1" not in lowered:
        issues.append("`<h1>` 태그 없음")
        score -= 10

    # Accessibility checks
    img_count = len(re.findall(r"<img\b", lowered))
    alt_count = len(re.findall(r"<img\b[^>]*\balt=", lowered))
    if img_count > 0 and alt_count < img_count:
        missing = img_count - alt_count
        issues.append(f"이미지 alt 누락: {missing}개")
        score -= min(20, 4 * missing)

    if "<html" in lowered and "lang=" not in lowered:
        warnings.append("`<html lang=...>` 누락")
        score -= 5

    # Career-document quality checks
    metric_hits = METRIC_PATTERN.findall(text)
    metric_count = len(metric_hits)
    if metric_count == 0:
        issues.append("성과 수치(%, 시간, 건수 등) 근거가 없음")
        score -= 16
    elif metric_count < 3:
        warnings.append("성과 수치가 적음 (3개 미만)")
        score -= 6

    soft_hits = [w for w in BANNED_SOFT_WORDS if w in text]
    if soft_hits:
        warnings.append("모호/약한 표현 포함: " + ", ".join(sorted(set(soft_hits))[:6]))
        score -= min(12, len(set(soft_hits)) * 2)

    action_hits = sum(1 for v in ACTION_VERBS if v in text)
    if action_hits < 3:
        warnings.append("행동 중심 동사 비율 낮음 (개선/최적화/구축 등)")
        score -= 5

    # Link hygiene
    for m in re.finditer(r"<a\b[^>]*href=[\"']([^\"']+)[\"']", text, re.IGNORECASE):
        href = m.group(1).strip()
        if href.startswith("#") or href.startswith("mailto:") or href.startswith("tel:"):
            continue
        if href in {"", "javascript:void(0)", "javascript:;"}:
            issues.append("유효하지 않은 링크 href 발견")
            score -= 8
            break

    return max(score, 0), issues, warnings


def analyze_css(path: Path):
    text = path.read_text(encoding="utf-8", errors="ignore")
    issues = []
    warnings = []
    score = 100

    # Basic maintainability checks
    if "!important" in text:
        count = text.count("!important")
        warnings.append(f"`!important` 사용 {count}회")
        score -= min(10, count)

    if re.search(r"font-size\s*:\s*\d+px", text):
        warnings.append("px 고정 폰트 사이즈 사용 (반응형/접근성 약화 가능)")
        score -= 4

    if len(text.splitlines()) > 1200:
        warnings.append("CSS 파일 길이 큼: 분리/모듈화 검토 필요")
        score -= 4

    return max(score, 0), issues, warnings


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--files-file", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    files = read_files_from_list(Path(args.files_file))

    critical = 0
    total_score = 0
    reviewed = 0
    lines = ["# 🔎 Strict Content Review", ""]

    for rel in files:
        p = Path(rel)
        if not p.exists() or p.is_dir():
            continue

        ext = p.suffix.lower()
        if ext not in {".html", ".css"}:
            continue

        reviewed += 1
        if ext == ".html":
            score, issues, warnings = analyze_html(p)
        else:
            score, issues, warnings = analyze_css(p)

        total_score += score
        if score < 70 or len(issues) >= 2:
            critical += 1

        status = "❌ FAIL" if score < 70 else ("⚠️ WARN" if score < 85 else "✅ PASS")
        lines.append(f"## {status} `{rel}` — {score}/100")

        if issues:
            lines.append("**치명 이슈**")
            for i in issues:
                lines.append(f"- {i}")
        if warnings:
            lines.append("**개선 포인트**")
            for w in warnings:
                lines.append(f"- {w}")
        if not issues and not warnings:
            lines.append("- 점검 기준 통과")
        lines.append("")

    if reviewed == 0:
        lines.append("리뷰할 HTML/CSS 파일이 없음.")
        Path(args.output).write_text("\n".join(lines), encoding="utf-8")
        return

    avg = round(total_score / reviewed, 1)
    lines.append("---")
    lines.append(f"- 평균 점수: **{avg}/100**")
    lines.append(f"- 치명 상태 파일 수: **{critical}개**")
    lines.append("")
    lines.append("판정 기준: 70점 미만 또는 치명 이슈 다수면 실패 처리")

    Path(args.output).write_text("\n".join(lines), encoding="utf-8")

    # Fail the workflow when strict gate is not met
    if critical > 0 or avg < 80:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
