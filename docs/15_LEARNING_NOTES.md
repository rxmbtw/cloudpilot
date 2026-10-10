## 2026-10-10 — Secret leak & rotation

**Symptom:** secret.yaml and SSH private key were in public git history.
**Root cause:** secrets committed before .gitignore rules existed.
**Fix:** rotated DB password, SECRET_KEY, GitHub Secrets; deleted AWS key pair + server.
**Verification:** old password rejected, forged JWT → 401, CI fingerprints matched.
**Lessons:**
1. Deleting from git ≠ removing a leak. Rotate.
2. Postgres only reads POSTGRES_PASSWORD on first init → ALTER USER.
3. Pods read env only at startup → rollout restart.
4. EC2 keys are baked in at first boot → replace the server.
5. Prove the OLD secret fails, not just that the new one works.
**Prevention:** GitHub push protection on; never commit .env/keys.
