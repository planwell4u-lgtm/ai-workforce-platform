"""Unit tests for Website URL Knowledge Extractor."""

from __future__ import annotations

import unittest
from unittest.mock import MagicMock, patch

from ai_workforce_backend.url_extractor import WebsiteKnowledgeExtractor


SAMPLE_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Bright Smile Dental | Premier Family Dentistry</title>
    <meta name="description" content="Bright Smile Dental provides comprehensive family and cosmetic dental care in Austin, TX.">
</head>
<body>
    <header><nav><a href="/">Home</a><a href="/about">About</a></nav></header>
    <main>
        <h1>Welcome to Bright Smile Dental</h1>
        <p>We are dedicated to providing the highest quality dental care for patients of all ages.</p>
        
        <h2>Teeth Whitening & Cleaning</h2>
        <p>Our professional teeth whitening treatments remove stubborn stains and brighten your smile in under an hour.</p>
        
        <h2>Emergency Dental Care</h2>
        <p>Same-day emergency dental appointments for severe toothaches, chipped teeth, and trauma.</p>

        <h2>Dental Implants</h2>
        <p>Permanent, natural-looking replacement teeth designed to restore your full bite and smile confidence.</p>

        <section class="hours">
            <h3>Operating Hours</h3>
            <p>Monday - Friday: 8:00 AM - 5:00 PM</p>
            <p>Saturday: 9:00 AM - 1:00 PM (By Appointment)</p>
        </section>

        <section class="contact">
            <h3>Contact Us</h3>
            <p>Phone: (512) 555-0199</p>
            <p>Email: appointments@brightsmiledental.com</p>
            <p>Location: 100 Main St, Suite 400, Austin, TX</p>
        </section>
    </main>
    <footer><p>&copy; 2026 Bright Smile Dental. All rights reserved.</p></footer>
</body>
</html>
"""


class TestWebsiteKnowledgeExtractor(unittest.TestCase):
    def setUp(self) -> None:
        self.extractor = WebsiteKnowledgeExtractor(timeout_seconds=5)

    def test_extract_from_html_structure(self) -> None:
        articles = self.extractor.extract_from_html(SAMPLE_HTML, base_url="https://brightsmiledental.com")
        self.assertGreaterEqual(len(articles), 4)

        # Overview
        overview = next((a for a in articles if a["topic"] == "Company Overview"), None)
        self.assertIsNotNone(overview)
        self.assertIn("Bright Smile Dental", overview["answer"])
        self.assertFalse(overview["published"])

        # Hours
        hours = next((a for a in articles if a["category"] == "hours"), None)
        self.assertIsNotNone(hours)
        self.assertIn("8:00 AM", hours["answer"])

        # Contact
        contact = next((a for a in articles if a["topic"] == "Contact Information"), None)
        self.assertIsNotNone(contact)
        self.assertIn("512) 555-0199", contact["answer"])

        # Service Headings
        whitening = next((a for a in articles if "Teeth Whitening" in a["topic"]), None)
        self.assertIsNotNone(whitening)
        self.assertEqual(whitening["category"], "services")

    def test_invalid_url_scheme(self) -> None:
        with self.assertRaises(ValueError):
            self.extractor.fetch_and_extract("ftp://example.com")
        with self.assertRaises(ValueError):
            self.extractor.fetch_and_extract("invalid-url-string")

    @patch.object(WebsiteKnowledgeExtractor, "_fetch_html")
    def test_fetch_and_extract_mocked(self, mock_fetch: MagicMock) -> None:
        mock_fetch.return_value = SAMPLE_HTML
        articles = self.extractor.fetch_and_extract("https://brightsmiledental.com")
        mock_fetch.assert_called_once_with("https://brightsmiledental.com")
        self.assertTrue(len(articles) >= 4)
