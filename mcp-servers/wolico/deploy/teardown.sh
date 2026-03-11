#!/bin/bash
set -euo pipefail

# ============================================================================
# Teardown MCP Wolico — Rimuove TUTTA l'infrastruttura AWS
# ============================================================================
#
# Elimina: Function URL, Lambda, IAM role + policy, ECR repo + immagini,
#          Secrets Manager secret
#
# Uso: ./teardown.sh
#
# ============================================================================

PROFILE="LaifDev"
REGION="eu-west-1"
FUNCTION_NAME="wolico-mcp"
ROLE_NAME="wolico-mcp-role"
ECR_REPO="wolico-mcp"
SECRET_NAME="wolico-mcp/credentials"
ACCOUNT_ID="596438087297"

AWS="aws --profile $PROFILE --region $REGION"

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

log()  { echo -e "${GREEN}[-]${NC} $1"; }
warn() { echo -e "${YELLOW}[!]${NC} $1"; }

echo ""
echo -e "${RED}╔═══════════════════════════════════════════╗${NC}"
echo -e "${RED}║  TEARDOWN: elimina TUTTA l'infra Wolico   ║${NC}"
echo -e "${RED}╚═══════════════════════════════════════════╝${NC}"
echo ""
read -p "Confermi? (y/N) " -n 1 -r
echo ""
[[ ! "$REPLY" =~ ^[Yy]$ ]] && { echo "Annullato."; exit 0; }
echo ""

# 1. Function URL
log "1/5 — Rimozione Function URL..."
$AWS lambda delete-function-url-config --function-name "$FUNCTION_NAME" 2>/dev/null && log "     Function URL eliminata." || warn "     Function URL non trovata."

# 2. Lambda Function
log "2/5 — Eliminazione Lambda function..."
$AWS lambda delete-function --function-name "$FUNCTION_NAME" 2>/dev/null && log "     Lambda eliminata." || warn "     Lambda non trovata."

# 3. IAM Role + Policy
log "3/5 — Eliminazione IAM role..."
$AWS iam delete-role-policy --role-name "$ROLE_NAME" --policy-name "${FUNCTION_NAME}-policy" 2>/dev/null || true
$AWS iam delete-role --role-name "$ROLE_NAME" 2>/dev/null && log "     Role eliminato." || warn "     Role non trovato."

# 4. ECR Repository + immagini
log "4/5 — Eliminazione ECR repository..."
$AWS ecr delete-repository --repository-name "$ECR_REPO" --force 2>/dev/null && log "     ECR repo eliminato (con tutte le immagini)." || warn "     ECR repo non trovato."

# 5. Secrets Manager
log "5/5 — Eliminazione Secrets Manager..."
$AWS secretsmanager delete-secret \
    --secret-id "$SECRET_NAME" \
    --force-delete-without-recovery 2>/dev/null && log "     Secret eliminato." || warn "     Secret non trovato."

echo ""
log "Teardown completato. Tutta l'infrastruttura Wolico MCP è stata rimossa."
