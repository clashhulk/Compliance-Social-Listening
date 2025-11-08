# Deployment Checklist

Use this checklist to ensure smooth deployment of the India Compliance Pain Tracker.

## Pre-Deployment

### Local Setup
- [ ] Python 3.8+ installed
- [ ] Dependencies installed: `pip install -r requirements.txt`
- [ ] `.env` file created with Reddit credentials
- [ ] Verification script passed: `python verify_setup.py`
- [ ] Test collection successful: `python collect.py`
- [ ] Dashboard loads locally: `streamlit run app.py`
- [ ] Data appears in dashboard correctly

### Reddit API
- [ ] Reddit account created
- [ ] App created at https://www.reddit.com/prefs/apps
- [ ] Client ID noted
- [ ] Client Secret noted
- [ ] Credentials tested and working

### Git Repository
- [ ] Git repository initialized: `git init`
- [ ] All files added: `git add .`
- [ ] Initial commit: `git commit -m "Initial commit"`
- [ ] GitHub repository created
- [ ] Remote added: `git remote add origin <url>`
- [ ] Pushed to GitHub: `git push -u origin main`

## Streamlit Cloud Deployment

### Account Setup
- [ ] Streamlit Cloud account created at https://share.streamlit.io/
- [ ] GitHub connected to Streamlit Cloud
- [ ] Repository access granted

### App Configuration
- [ ] New app created in Streamlit Cloud
- [ ] Repository selected
- [ ] Branch: `main`
- [ ] Main file: `app.py`
- [ ] Secrets configured:
  ```toml
  REDDIT_CLIENT_ID = "your_client_id"
  REDDIT_CLIENT_SECRET = "your_client_secret"
  REDDIT_USER_AGENT = "IndiaCompliancePainTracker/1.0"
  ```
- [ ] App deployed successfully
- [ ] Public URL noted

### Testing
- [ ] Dashboard loads on public URL
- [ ] Data appears (may need to wait for first collection)
- [ ] Filters work correctly
- [ ] CSV export works
- [ ] Charts render properly
- [ ] Mobile view tested

## GitHub Actions Setup

### Secrets Configuration
- [ ] Navigate to repo Settings → Secrets and variables → Actions
- [ ] Add `REDDIT_CLIENT_ID`
- [ ] Add `REDDIT_CLIENT_SECRET`
- [ ] Test workflow manually: Actions tab → Collect Compliance Data → Run workflow

### Workflow Verification
- [ ] Workflow runs successfully
- [ ] Database artifact uploaded
- [ ] Check logs for errors
- [ ] Wait 6 hours for automatic run
- [ ] Verify automated collection works

## Post-Deployment

### Monitoring
- [ ] GitHub Actions email notifications enabled
- [ ] Streamlit Cloud app status bookmarked
- [ ] Dashboard URL shared with team
- [ ] First week monitoring plan set

### Data Validation
- [ ] Wait 24 hours for initial data collection
- [ ] Check dashboard for posts (target: ≥10/day)
- [ ] Verify pain signal % (target: ≥40%)
- [ ] Check trend chart for activity
- [ ] Review top tags for relevance

### Documentation
- [ ] README updated with public URL
- [ ] Team trained on dashboard usage
- [ ] Feedback collection method set up
- [ ] Success metrics tracking started

## Success Criteria

After 1 week, verify:

- [ ] **≥150 posts collected** (14-day window)
- [ ] **≥40% pain signals** (PortalIssues, Deadlines, Negative)
- [ ] **Visible spikes** near compliance deadlines
- [ ] **GitHub Actions** running every 6 hours without errors
- [ ] **Dashboard** loading in <5 seconds
- [ ] **Team** actively using dashboard

## Troubleshooting Quick Reference

| Issue | Check | Fix |
|-------|-------|-----|
| Streamlit app won't start | Logs in Streamlit Cloud | Check secrets, review error logs |
| GitHub Actions failing | Actions tab logs | Verify secrets, check Reddit API |
| No data appearing | Database artifact | Run manual collection, check workflow |
| Dashboard is slow | Data volume | Normal for first load, caches after |
| CSV export broken | Browser console | Clear cache, try different browser |

## Rollback Plan

If deployment fails:

1. **Streamlit Cloud Issues**
   - Reboot app in Streamlit Cloud dashboard
   - Check and re-enter secrets
   - Redeploy from GitHub

2. **GitHub Actions Issues**
   - Disable workflow temporarily
   - Run collection manually: `python collect.py`
   - Commit database to repo
   - Re-enable workflow

3. **Complete Failure**
   - Run locally: `streamlit run app.py`
   - Share via ngrok: `ngrok http 8501`
   - Fix issues offline, redeploy when ready

## Maintenance Schedule

### Daily (Automated)
- Data collection (4x/day via GitHub Actions)
- Database backups (via artifacts)

### Weekly (Manual)
- Check GitHub Actions logs
- Review dashboard metrics
- Verify success criteria
- Share insights with team

### Monthly (Manual)
- Update dependencies: `pip list --outdated`
- Review and update keyword list
- Check Reddit API status
- Analyze trend patterns

## Next Steps After Deployment

Once deployed successfully:

1. **Week 1**: Monitor and validate
   - Watch for errors
   - Ensure data collection works
   - Verify metrics meet targets

2. **Week 2**: Gather feedback
   - Share with stakeholders
   - Collect usage feedback
   - Note feature requests

3. **Week 3-4**: Iterate
   - Add requested features
   - Improve tagging accuracy
   - Optimize performance

4. **Month 2+**: Scale
   - Add more data sources
   - Implement alerts
   - Build API access

## Sign-Off

Deployment completed by: ___________________

Date: ___________________

Verified by: ___________________

Public dashboard URL: ___________________

GitHub repo: ___________________

Notes:
_____________________________________________________
_____________________________________________________
_____________________________________________________

---

**Deployment Status**: ⬜ Not Started | ⬜ In Progress | ⬜ Complete | ⬜ Failed

**Next review date**: ___________________
