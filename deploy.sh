#!/usr/bin/env bash
# ─────────────────────────────────────────────────────────────────────────────
# Madame Minou — Deploy Script (Block 0 spike → full deploy)
#
# Usage:
#   ./deploy.sh                # deploy with defaults (prod stage)
#   ./deploy.sh dev            # deploy to dev stage
#
# Prerequisites:
#   1. AWS CLI v2 configured with credentials (aws configure / IAM role)
#   2. AWS SAM CLI installed (pip install aws-sam-cli)
#   3. S3 bucket for SAM artifacts (auto-created by sam deploy --guided first run)
# ─────────────────────────────────────────────────────────────────────────────
set -euo pipefail

STAGE="${1:-prod}"
STACK_NAME="madame-minou-${STAGE}"
REGION="${AWS_REGION:-us-east-1}"

# ─── Colors ───────────────────────────────────────────────────────────────────
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
NC='\033[0m'

info()  { echo -e "${GREEN}[INFO]${NC} $*"; }
warn()  { echo -e "${YELLOW}[WARN]${NC} $*"; }
error() { echo -e "${RED}[ERROR]${NC} $*"; exit 1; }

# ─── Step 0: Validate prerequisites ──────────────────────────────────────────
info "Checking prerequisites..."

if ! command -v aws &>/dev/null; then
  error "AWS CLI not found. Install: https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2.html"
fi

if ! command -v sam &>/dev/null; then
  error "SAM CLI not found. Install: pip install aws-sam-cli"
fi

# Check credentials
if ! aws sts get-caller-identity &>/dev/null; then
  error "No valid AWS credentials found. Run 'aws configure' or set AWS_ACCESS_KEY_ID + AWS_SECRET_ACCESS_KEY."
fi

ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
info "Deploying as account: ${ACCOUNT_ID} in region: ${REGION}"

# ─── Step 0.5: Package server module with Lambda ─────────────────────────────
info "Packaging server/ module into lambda/ for deployment..."
rm -rf lambda/server
cp -r server lambda/server

# ─── Step 1: SAM build ───────────────────────────────────────────────────────
info "Building SAM application..."
sam build --template-file template.yaml

# ─── Step 2: SAM deploy ──────────────────────────────────────────────────────
info "Deploying stack: ${STACK_NAME} to ${REGION}..."
sam deploy \
  --stack-name "${STACK_NAME}" \
  --region "${REGION}" \
  --capabilities CAPABILITY_IAM \
  --resolve-s3 \
  --parameter-overrides "Stage=${STAGE}" \
  --no-confirm-changeset \
  --no-fail-on-empty-changeset

# ─── Step 3: Upload frontend to S3 ───────────────────────────────────────────
info "Fetching stack outputs..."
API_URL=$(aws cloudformation describe-stacks \
  --stack-name "${STACK_NAME}" \
  --region "${REGION}" \
  --query "Stacks[0].Outputs[?OutputKey=='ApiUrl'].OutputValue" \
  --output text)

FRONTEND_BUCKET=$(aws cloudformation describe-stacks \
  --stack-name "${STACK_NAME}" \
  --region "${REGION}" \
  --query "Stacks[0].Outputs[?OutputKey=='FrontendBucketName'].OutputValue" \
  --output text)

FRONTEND_URL=$(aws cloudformation describe-stacks \
  --stack-name "${STACK_NAME}" \
  --region "${REGION}" \
  --query "Stacks[0].Outputs[?OutputKey=='FrontendUrl'].OutputValue" \
  --output text)

# Inject the API URL into the frontend before uploading
info "Injecting API URL into frontend..."
sed "s|window.__MINOU_API_URL__ || ''|'${API_URL%/hello}'|" frontend/index.html > /tmp/index.html

info "Uploading frontend to S3..."
aws s3 sync frontend/ "s3://${FRONTEND_BUCKET}/" --region "${REGION}" --delete
aws s3 cp /tmp/index.html "s3://${FRONTEND_BUCKET}/index.html" --region "${REGION}"

# ─── Step 4: Report results ──────────────────────────────────────────────────
echo ""
echo "═══════════════════════════════════════════════════════════════════"
info "Deploy complete!"
echo ""
echo "  API endpoint:  ${API_URL}"
echo "  Frontend URL:  ${FRONTEND_URL}"
echo "  S3 bucket:     ${FRONTEND_BUCKET}"
echo ""
echo "  Test: curl ${API_URL}"
echo "═══════════════════════════════════════════════════════════════════"

# ─── Step 5: Clean up deploy artifacts ────────────────────────────────────────
info "Cleaning up lambda/server/ copy..."
rm -rf lambda/server

# ─── Fallback note ────────────────────────────────────────────────────────────
cat <<'EOF'

─── FALLBACK (if SAM/CloudFront is blocked) ───────────────────────────────────
If this deploy path is blocked (IAM permissions, org SCPs, etc.), fall back to:

  Option A: Amplify Hosting (still AWS)
    npm install -g @aws-amplify/cli
    amplify init
    amplify add hosting
    amplify publish

  Option B: Vercel (last resort, non-AWS)
    npm install -g vercel
    cd frontend && vercel --prod
    (Keep Lambda on AWS for the backend; only frontend moves to Vercel)
────────────────────────────────────────────────────────────────────────────────
EOF
