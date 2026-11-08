# Dobby Auto Research
Public RSS research snapshots for three Japanese business topics: government tenders, AI/SNS monetization, and reuse/buyback news.

- Scheduled daily at 08:00 JST (GitHub Actions schedule may be delayed).
- Manual run: Actions > Dobby free daily research > Run workflow.
- Outputs: data/government_bids.json, data/ai_business.json, data/reuse.json.
- No API keys, paid API, hosted database, or third-party scraping service.
- Only public Google News RSS headlines, links, timestamps, and publisher names are collected. News search is **not** an exhaustive list of official tenders; verify every notice on its issuing agency website.
- GitHub public repository Actions on GitHub-hosted standard runners are free under GitHub's current public-repository policy. Avoid changing visibility to private or enabling paid features.
- Check Actions settings to ensure workflows are enabled and workflow token has read/write contents permission. Never enter a credit card for this workflow.
- Websites and feeds can fail or change. Errors are printed to Actions logs; no paid fallback is attempted.
