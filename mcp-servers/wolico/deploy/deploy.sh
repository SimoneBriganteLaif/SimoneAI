#!/bin/bash
set -euo pipefail

# ============================================================================
# Deploy MCP Wolico su AWS Lambda
# ============================================================================
#
# Crea tutta l'infrastruttura:
#   ECR repository + Docker image + IAM role + Lambda function + Function URL
#   + Secrets Manager (per credenziali per-utente)
#
# Prerequisiti:
#   - AWS CLI v2
#   - Docker Desktop
#   - SSO login attivo: aws sso login --profile LaifDev
#
# Uso:
#   ./deploy.sh              — deploy completo
#   ./deploy.sh add-user EMAIL PASSWORD  — aggiunge utente a Secrets Manager
#   ./deploy.sh update       — rebuilda e aggiorna solo l'immagine Lambda
#
# ============================================================================

PROFILE="LaifDev"
REGION="eu-west-1"
FUNCTION_NAME="wolico-mcp"
ROLE_NAME="wolico-mcp-role"
ECR_REPO="wolico-mcp"
SECRET_NAME="wolico-mcp/credentials"
ACCOUNT_ID="596438087297"
ECR_URI="${ACCOUNT_ID}.dkr.ecr.${REGION}.amazonaws.com/${ECR_REPO}"
# Lambda Web Adapter layer ARN (ARM64, eu-west-1)
LWA_LAYER="arn:aws:lambda:${REGION}:753240598075:layer:LambdaAdapterLayerArm64:25"

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

AWS="aws --profile $PROFILE --region $REGION"

# Colori
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

log()  { echo -e "${GREEN}[+]${NC} $1"; }
warn() { echo -e "${YELLOW}[!]${NC} $1"; }
err()  { echo -e "${RED}[x]${NC} $1" >&2; exit 1; }

# ---------------------------------------------------------------------------
# Comando: add-user
# ---------------------------------------------------------------------------
if [[ "${1:-}" == "add-user" ]]; then
    EMAIL="${2:-}"
    PASS="${3:-}"
    [[ -z "$EMAIL" || -z "$PASS" ]] && err "Uso: ./deploy.sh add-user EMAIL PASSWORD"

    log "Aggiunta utente $EMAIL a Secrets Manager..."

    # Leggi secret attuale
    CURRENT=$($AWS secretsmanager get-secret-value \
        --secret-id "$SECRET_NAME" \
        --query 'SecretString' --output text 2>/dev/null || echo '{}')

    # Aggiungi/aggiorna email
    UPDATED=$(echo "$CURRENT" | python3 -c "
import sys, json
d = json.loads(sys.stdin.read())
d['$EMAIL'] = '$PASS'
print(json.dumps(d))
")

    $AWS secretsmanager update-secret \
        --secret-id "$SECRET_NAME" \
        --secret-string "$UPDATED" > /dev/null

    log "Utente $EMAIL aggiunto/aggiornato."
    exit 0
fi

# ---------------------------------------------------------------------------
# Comando: update (solo rebuild immagine)
# ---------------------------------------------------------------------------
if [[ "${1:-}" == "update" ]]; then
    log "Aggiornamento immagine Lambda..."

    # Login ECR
    $AWS ecr get-login-password | docker login --username AWS --password-stdin "${ACCOUNT_ID}.dkr.ecr.${REGION}.amazonaws.com" 2>/dev/null

    # Build e push
    log "Build Docker image (ARM64)..."
    docker buildx build --platform linux/arm64 -t "${ECR_URI}:latest" -f "$SCRIPT_DIR/Dockerfile.lambda" "$PROJECT_DIR" --push

    # Aggiorna Lambda
    log "Aggiornamento Lambda function..."
    $AWS lambda update-function-code \
        --function-name "$FUNCTION_NAME" \
        --image-uri "${ECR_URI}:latest" > /dev/null

    log "Attesa deploy Lambda..."
    $AWS lambda wait function-updated --function-name "$FUNCTION_NAME"

    FUNC_URL=$($AWS lambda get-function-url-config --function-name "$FUNCTION_NAME" --query 'FunctionUrl' --output text 2>/dev/null || echo "N/D")
    log "Lambda aggiornata: ${FUNC_URL}mcp"
    exit 0
fi

# ---------------------------------------------------------------------------
# Deploy completo
# ---------------------------------------------------------------------------
log "Deploy MCP Wolico su AWS Lambda ($REGION)"
echo ""

# 1. ECR Repository
log "1/6 — Creazione ECR repository..."
$AWS ecr describe-repositories --repository-names "$ECR_REPO" > /dev/null 2>&1 || \
    $AWS ecr create-repository --repository-name "$ECR_REPO" --image-scanning-configuration scanOnPush=true > /dev/null
log "     ECR: $ECR_URI"

# 2. Build e push Docker image
log "2/6 — Build e push Docker image (ARM64)..."
$AWS ecr get-login-password | docker login --username AWS --password-stdin "${ACCOUNT_ID}.dkr.ecr.${REGION}.amazonaws.com" 2>/dev/null
docker buildx build --platform linux/arm64 -t "${ECR_URI}:latest" -f "$SCRIPT_DIR/Dockerfile.lambda" "$PROJECT_DIR" --push
log "     Image pushed: ${ECR_URI}:latest"

# 3. IAM Role
log "3/6 — Creazione IAM role..."
ROLE_ARN=$($AWS iam get-role --role-name "$ROLE_NAME" --query 'Role.Arn' --output text 2>/dev/null || echo "")

if [[ -z "$ROLE_ARN" ]]; then
    TRUST_POLICY='{
        "Version": "2012-10-17",
        "Statement": [{
            "Effect": "Allow",
            "Principal": {"Service": "lambda.amazonaws.com"},
            "Action": "sts:AssumeRole"
        }]
    }'

    ROLE_ARN=$($AWS iam create-role \
        --role-name "$ROLE_NAME" \
        --assume-role-policy-document "$TRUST_POLICY" \
        --query 'Role.Arn' --output text)

    # Policy: CloudWatch Logs + Secrets Manager
    POLICY='{
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Action": [
                    "logs:CreateLogGroup",
                    "logs:CreateLogStream",
                    "logs:PutLogEvents"
                ],
                "Resource": "arn:aws:logs:*:*:*"
            },
            {
                "Effect": "Allow",
                "Action": "secretsmanager:GetSecretValue",
                "Resource": "arn:aws:secretsmanager:'"$REGION"':'"$ACCOUNT_ID"':secret:'"$SECRET_NAME"'*"
            }
        ]
    }'

    $AWS iam put-role-policy \
        --role-name "$ROLE_NAME" \
        --policy-name "${FUNCTION_NAME}-policy" \
        --policy-document "$POLICY"

    log "     Role creato: $ROLE_ARN"
    log "     Attesa propagazione IAM (10s)..."
    sleep 10
else
    log "     Role esistente: $ROLE_ARN"
fi

# 4. Secrets Manager
log "4/6 — Creazione Secrets Manager..."
$AWS secretsmanager describe-secret --secret-id "$SECRET_NAME" > /dev/null 2>&1 || \
    $AWS secretsmanager create-secret \
        --name "$SECRET_NAME" \
        --description "Credenziali Wolico per-utente (email -> password)" \
        --secret-string '{}' > /dev/null
log "     Secret: $SECRET_NAME"

# 5. Lambda Function
log "5/6 — Creazione Lambda function..."
EXISTING=$($AWS lambda get-function --function-name "$FUNCTION_NAME" 2>/dev/null || echo "")

if [[ -z "$EXISTING" ]]; then
    $AWS lambda create-function \
        --function-name "$FUNCTION_NAME" \
        --package-type Image \
        --code "ImageUri=${ECR_URI}:latest" \
        --role "$ROLE_ARN" \
        --architectures arm64 \
        --memory-size 256 \
        --timeout 30 \
        --layers "$LWA_LAYER" \
        --environment "Variables={MCP_TRANSPORT=http,PORT=8080,WOLICO_BASE_URL=https://wolico.app.laifgroup.com/api/,WOLICO_SECRET_NAME=$SECRET_NAME,AWS_LWA_PORT=8080}" \
        > /dev/null

    log "     Lambda creata. Attesa attivazione..."
    $AWS lambda wait function-active-v2 --function-name "$FUNCTION_NAME"
else
    # Aggiorna immagine
    $AWS lambda update-function-code \
        --function-name "$FUNCTION_NAME" \
        --image-uri "${ECR_URI}:latest" > /dev/null
    $AWS lambda wait function-updated --function-name "$FUNCTION_NAME"
    log "     Lambda aggiornata."
fi

# 6. Function URL
log "6/6 — Configurazione Function URL..."
FUNC_URL=$($AWS lambda get-function-url-config --function-name "$FUNCTION_NAME" --query 'FunctionUrl' --output text 2>/dev/null || echo "")

if [[ -z "$FUNC_URL" ]]; then
    FUNC_URL=$($AWS lambda create-function-url-config \
        --function-name "$FUNCTION_NAME" \
        --auth-type NONE \
        --invoke-mode RESPONSE_STREAM \
        --query 'FunctionUrl' --output text)

    # Permesso pubblico per Function URL
    $AWS lambda add-permission \
        --function-name "$FUNCTION_NAME" \
        --statement-id "FunctionURLAllowPublicAccess" \
        --action "lambda:InvokeFunctionUrl" \
        --principal "*" \
        --function-url-auth-type NONE > /dev/null
fi

echo ""
log "Deploy completato!"
echo ""
echo "  URL MCP: ${FUNC_URL}mcp"
echo ""
echo "  Prossimi passi:"
echo "  1. Aggiungi utenti:"
echo "     ./deploy.sh add-user nome.cognome@laifgroup.com 'password'"
echo ""
echo "  2. Colleghi configurano Claude Code:"
echo "     claude mcp add wolico \\"
echo "       --transport streamablehttp \\"
echo "       --header \"X-Wolico-Email:nome.cognome@laifgroup.com\" \\"
echo "       ${FUNC_URL}mcp"
echo ""
echo "  3. Colleghi configurano Notion AI Custom Agent:"
echo "     URL MCP: ${FUNC_URL}mcp"
echo "     Header: X-Wolico-Email: nome.cognome@laifgroup.com"
