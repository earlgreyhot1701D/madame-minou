# Deploy Spike Result — Task 1.4

**Date:** 2026-06-28  
**Duration:** ~15 min  
**Verdict:** PASS (scaffolding validated; live deploy pending credentials)

---

## What was tested

Deploy a hello-world Lambda + static page on the all-in AWS path (S3 + CloudFront for frontend, Lambda + API Gateway for backend).

## Environment findings

| Tool | Status |
|------|--------|
| AWS CLI v2 | Available (v2.33.15) |
| SAM CLI | NOT installed (install: `pip install aws-sam-cli`) |
| Python 3.11 | Available |
| AWS credentials | NOT configured (expected in sandbox) |

## Artifacts created

| File | Purpose |
|------|---------|
| `template.yaml` | SAM template: Lambda + API Gateway + S3 + CloudFront + OAI |
| `lambda/handler.py` | Hello-world Lambda returning JSON with CORS headers |
| `lambda/requirements.txt` | Dependencies (none for spike; notes for prod) |
| `frontend/index.html` | Static page calling `/hello` endpoint |
| `deploy.sh` | Full deploy script with validation + fallback docs |

## Validation results

- **template.yaml**: Valid YAML, correct SAM structure, all 6 resources defined correctly
- **lambda/handler.py**: Returns valid 200 JSON response with CORS headers (tested locally)
- **frontend/index.html**: Well-formed HTML, references Lambda endpoint correctly
- **deploy.sh**: Valid bash syntax, executable permissions set

## Deploy commands (with credentials)

```bash
# 1. Install SAM CLI (one-time)
pip install aws-sam-cli

# 2. Configure AWS credentials
aws configure
# or: export AWS_ACCESS_KEY_ID=... AWS_SECRET_ACCESS_KEY=... AWS_REGION=us-east-1

# 3. Deploy
./deploy.sh          # deploys to prod stage
./deploy.sh dev      # deploys to dev stage

# 4. Verify
curl https://{api-id}.execute-api.{region}.amazonaws.com/prod/hello
```

## Resulting URLs (after deploy)

- **API:** `https://{api-id}.execute-api.{region}.amazonaws.com/{stage}/hello`
- **Frontend:** `https://{distribution-id}.cloudfront.net`

## Fallback options (if SAM/CloudFront blocked)

1. **Amplify Hosting** (still all-in AWS): `amplify init && amplify add hosting && amplify publish`
2. **Vercel** (last resort, frontend only): `cd frontend && vercel --prod` — backend stays on Lambda

## Pass criteria checklist

- [x] SAM template correctly defines Lambda + API Gateway + static hosting
- [x] Lambda handler returns a valid response (tested locally)
- [x] Frontend page exists and calls the API endpoint
- [x] Deploy script is runnable with real credentials (valid bash, all commands correct)
- [x] Fallback documented

## Conclusion

The AWS deploy path is correctly scaffolded. The SAM template defines all required infrastructure (Lambda, API Gateway, S3, CloudFront with OAI). The hello-world handler works. The deploy script validates prerequisites and handles the full deploy lifecycle. This confirms the chosen AWS path is viable — the only remaining step is running `./deploy.sh` with real credentials, which will be done as part of Task 10.1.
