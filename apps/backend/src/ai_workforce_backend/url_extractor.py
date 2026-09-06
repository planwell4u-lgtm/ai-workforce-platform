"""Website URL Knowledge Extractor for Instant Agent Setup."""

from __future__ import annotations

import html
import re
import urllib.error
import urllib.parse
import urllib.request
from typing import Any


class WebsiteKnowledgeExtractor:
    """Extracts business knowledge from public websites to auto-generate draft FAQ articles."""

    USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) PlanwellBot/1.0 (+https://planwell.online)"

    def __init__(self, timeout_seconds: int = 10) -> None:
        self._timeout = timeout_seconds

    def fetch_and_extract(self, url: str) -> list[dict[str, Any]]:
        """Fetches a URL and parses it into structured draft knowledge articles."""
        parsed = urllib.parse.urlparse(url)
        if not parsed.scheme or parsed.scheme not in ("http", "https") or not parsed.netloc:
            raise ValueError(f"Invalid web URL: '{url}'. Must start with http:// or https://")

        raw_html = self._fetch_html(url)
        return self.extract_from_html(raw_html, base_url=url)

    def extract_from_html(self, raw_html: str, base_url: str = "") -> list[dict[str, Any]]:
        """Parses HTML text and generates draft FAQ records."""
        # Clean HTML (remove scripts, styles, comments, SVG, nav)
        text_content = self._clean_html(raw_html)
        domain = urllib.parse.urlparse(base_url).netloc if base_url else "Company"

        articles: list[dict[str, Any]] = []

        # 1. Extract Business Name & General Overview
        title_match = re.search(r"<title>(.*?)</title>", raw_html, re.IGNORECASE | re.DOTALL)
        page_title = title_match.group(1).strip() if title_match else domain
        meta_desc = self._extract_meta_description(raw_html)

        if meta_desc or page_title:
            overview_text = meta_desc if meta_desc else f"{page_title} provides professional services to customers."
            articles.append({
                "topic": "Company Overview",
                "question": f"What is {domain} and what services do you offer?",
                "answer": overview_text,
                "category": "services",
                "published": False,
            })

        # 2. Extract Business Hours / Availability
        hours_patterns = [
            r"(?:hours|opening hours|business hours|open)[\s:]*([^\n\<\>]{10,120})",
            r"(?:monday|mon|tuesday|wednesday|thursday|friday|saturday|sunday)[^\n\<\>]{10,100}(?:am|pm|a\.m\.|p\.m\.)",
        ]
        found_hours = []
        for pat in hours_patterns:
            matches = re.findall(pat, text_content, re.IGNORECASE)
            for m in matches:
                clean_m = re.sub(r"\s+", " ", m).strip()
                if len(clean_m) > 10 and clean_m not in found_hours:
                    found_hours.append(clean_m)

        if found_hours:
            hours_answer = f"Our operating hours are: {'; '.join(found_hours[:3])}."
            articles.append({
                "topic": "Business Hours",
                "question": "What are your business and operating hours?",
                "answer": hours_answer,
                "category": "hours",
                "published": False,
            })

        # 3. Extract Contact / Location Info
        phone_match = re.search(r"(?:\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}", text_content)
        email_match = re.search(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", text_content)

        contact_details = []
        if phone_match:
            contact_details.append(f"Phone: {phone_match.group(0)}")
        if email_match:
            contact_details.append(f"Email: {email_match.group(0)}")

        if contact_details:
            articles.append({
                "topic": "Contact Information",
                "question": "How can I contact customer support or schedule an appointment?",
                "answer": f"You can reach our team directly via {', '.join(contact_details)}.",
                "category": "support",
                "published": False,
            })

        # 4. Extract Key Services from Headings (H2 / H3)
        heading_matches = re.findall(r"<h[23][^>]*>(.*?)</h[23]>", raw_html, re.IGNORECASE | re.DOTALL)
        for h in heading_matches:
            clean_h = re.sub(r"<[^>]+>", "", h).strip()
            clean_h = html.unescape(clean_h)
            # Filter meaningful service/feature headings
            if (
                len(clean_h) >= 6
                and len(clean_h) <= 80
                and not any(k in clean_h.lower() for k in ["menu", "navigation", "cookie", "privacy", "copyright", "terms", "login", "sign in", "all rights"])
            ):
                articles.append({
                    "topic": clean_h,
                    "question": f"Do you offer {clean_h}?",
                    "answer": f"Yes, we provide full support and services for {clean_h}. Please contact our front desk for scheduling and pricing details.",
                    "category": "services",
                    "published": False,
                })
                if len(articles) >= 8:  # Cap extracted sections per crawl
                    break

        # 5. Default General Support FAQ if list is sparse
        if len(articles) < 3:
            articles.append({
                "topic": "Customer Inquiries & Support",
                "question": "How do I get assistance with my account or service order?",
                "answer": f"You can speak with our live front-desk agents via web chat or by calling our customer line.",
                "category": "support",
                "published": False,
            })

        return articles

    def _fetch_html(self, url: str) -> str:
        req = urllib.request.Request(
            url,
            headers={
                "User-Agent": self.USER_AGENT,
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                "Accept-Language": "en-US,en;q=0.5",
            },
        )
        try:
            with urllib.request.urlopen(req, timeout=self._timeout) as resp:
                charset = resp.headers.get_content_charset() or "utf-8"
                content_bytes = resp.read(1024 * 1024)  # 1MB limit for safety
                return content_bytes.decode(charset, errors="replace")
        except urllib.error.HTTPError as err:
            raise RuntimeError(f"HTTP Error {err.code}: {err.reason} when accessing {url}") from err
        except urllib.error.URLError as err:
            raise RuntimeError(f"Network error accessing {url}: {err.reason}") from err
        except Exception as err:
            raise RuntimeError(f"Failed to crawl {url}: {err}") from err

    @staticmethod
    def _clean_html(raw_html: str) -> str:
        # Strip script, style, svg, header, nav, footer tags
        cleaned = re.sub(r"<(script|style|svg|nav|header|footer)\b[^>]*>.*?</\1>", " ", raw_html, flags=re.IGNORECASE | re.DOTALL)
        # Strip HTML tags
        text = re.sub(r"<[^>]+>", " ", cleaned)
        # Unescape entities
        text = html.unescape(text)
        # Collapse whitespace
        return re.sub(r"\s+", " ", text).strip()

    @staticmethod
    def _extract_meta_description(raw_html: str) -> str:
        desc_match = re.search(r'<meta\s+name=["\']description["\']\s+content=["\'](.*?)["\']', raw_html, re.IGNORECASE)
        if not desc_match:
            desc_match = re.search(r'<meta\s+content=["\'](.*?)["\']\s+name=["\']description["\']', raw_html, re.IGNORECASE)
        if desc_match:
            return html.unescape(desc_match.group(1).strip())
        return ""
