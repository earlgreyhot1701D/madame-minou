"""
Madame Minou — AI Reading Layer (Block 2).

Endpoints:
  GET  /health   — health check (was /hello in Block 0 spike)
  POST /reading  — receive chart facts, call AnthropicAWS, return reading_text

Requirements validated:
  R4.2  - AI layer called with persona system prompt + facts as user content
  R4.3  - Model never alters facts; facts go in as user content, reading comes out
  R4.5  - In-voice error state on AI failure (never a blank screen or stack trace)
  R11.2 - Model called from server-side only (Lambda)
  R11.5 - try/catch with meaningful error state on every external call
"""

import json
import os
import sys

# Add project root to path so we can import server.prompts
# In Lambda, server/ is copied alongside handler.py by deploy.sh.
# Locally, sys.path.insert handles the import from the project root.
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from server.prompts.madame_minou import (
    MADAME_MINOU_SYSTEM_PROMPT,
    format_facts_message,
)

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

# Region MUST match the Claude Platform on AWS workspace region (us-east-1)
AWS_REGION = os.environ.get("AWS_REGION", "us-east-1")

# Model selection: claude-sonnet-4-6 for marquee quality natal/behavior reads
# Allow override via env var for testing or cost control
MINOU_MODEL = os.environ.get("MINOU_MODEL", "claude-sonnet-4-6")

# Mock mode: skip real API call, return a mock reading (for frontend dev)
MINOU_MOCK_AI = os.environ.get("MINOU_MOCK_AI", "false").lower() == "true"

# AI call timeout (seconds)
# API Gateway REST API caps at ~29s; keep AI call well under that ceiling
AI_TIMEOUT_SECONDS = 25.0

# In-voice error message — NEVER return a stack trace or blank screen
IN_VOICE_ERROR = (
    "Ah, ma chérie... Madame Minou's crystal ball has gone cloudy. "
    "The stars are shy today — perhaps try again in a moment, non?"
)

# CORS headers (applied to all responses)
CORS_HEADERS = {
    "Content-Type": "application/json",
    "Access-Control-Allow-Origin": os.environ.get("ALLOWED_ORIGIN", "*"),
    "Access-Control-Allow-Methods": "GET,POST,OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type",
}


# ---------------------------------------------------------------------------
# Input validation / sanitization (R9.5, R11.3)
# Full implementation in Block 5; basic caps here to prevent abuse
# ---------------------------------------------------------------------------

MAX_CAT_NAME_LENGTH = 100
MAX_BEHAVIOR_LENGTH = 1000  # Block 5 will enforce tighter + server-side validation
MAX_FIELD_LENGTH = 200  # For sun, moon, rising, transit fields


def _sanitize_facts(facts: dict) -> dict:
    """
    Sanitize and length-cap incoming facts fields.

    Keeps system-prompt isolation intact: behavior text stays in user-content
    slot only, never concatenated into system prompt.
    """
    sanitized = {}

    # String fields with length caps
    sanitized["cat_name"] = str(facts.get("cat_name", ""))[:MAX_CAT_NAME_LENGTH].strip()
    sanitized["chart_tier"] = str(facts.get("chart_tier", "mystery"))[:50]
    sanitized["sun"] = str(facts.get("sun", ""))[:MAX_FIELD_LENGTH].strip() or None
    sanitized["moon"] = str(facts.get("moon", ""))[:MAX_FIELD_LENGTH].strip() or None
    sanitized["rising"] = str(facts.get("rising", ""))[:MAX_FIELD_LENGTH].strip() or None
    sanitized["notable_transit"] = str(facts.get("notable_transit", ""))[:MAX_FIELD_LENGTH].strip() or None
    sanitized["tz_assumption"] = str(facts.get("tz_assumption", ""))[:MAX_FIELD_LENGTH].strip() or None

    # Boolean
    sanitized["moon_cusp"] = bool(facts.get("moon_cusp", False))

    # Behavior: length-capped, stays in user-content slot only (R11.3)
    behavior = facts.get("behavior")
    if behavior:
        sanitized["behavior"] = str(behavior)[:MAX_BEHAVIOR_LENGTH].strip() or None
    else:
        sanitized["behavior"] = None

    return sanitized


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _build_response(status_code: int, body: dict) -> dict:
    """Build a Lambda proxy response with CORS headers."""
    return {
        "statusCode": status_code,
        "headers": CORS_HEADERS,
        "body": json.dumps(body),
    }


def _mock_reading(facts: dict) -> str:
    """
    Generate a mock reading for frontend development (MINOU_MOCK_AI=true).

    The mock still passes the specificity test: mentions cat name and sun sign.
    """
    cat_name = facts.get("cat_name", "mysterious one")
    sun_sign = facts.get("sun", "unknown star")
    moon_sign = facts.get("moon", "hidden moon")
    chart_tier = facts.get("chart_tier", "mystery")

    return (
        f"Ah, {cat_name}! Madame Minou sees you clearly, ma chérie. "
        f"A {sun_sign} sun — bien sûr, I should have known from the way "
        f"you hold your tail just so. "
        f"And that {moon_sign} moon gives you a certain... gravitas, non? "
        f"You are a cat of depth and contradictions, mon petit. "
        f"This is {'your full chart' if chart_tier == 'full' else 'an estimated reading'}, "
        f"and it tells Madame Minou everything she needs to know about {cat_name}."
    )


def _call_anthropic_aws(facts: dict, reading_type: str = "natal") -> str:
    """
    Call AnthropicAWS with the Madame Minou system prompt + formatted facts.

    The determinism contract (R4.3):
      - System prompt = Madame Minou persona (constant)
      - User content = formatted facts message (varies per request)
      - Model output = the flavored reading text (returned as-is)
      - We NEVER pass user-generated free text into the system prompt

    Raises:
        Exception: Any error from the AnthropicAWS client (timeout, auth, rate limit)
    """
    from anthropic import AnthropicAWS

    # Region MUST match the Claude Platform on AWS workspace region
    client = AnthropicAWS()

    user_content = format_facts_message(facts, reading_type=reading_type)

    message = client.messages.create(
        model=MINOU_MODEL,
        max_tokens=1024,
        system=MADAME_MINOU_SYSTEM_PROMPT,
        messages=[{"role": "user", "content": user_content}],
        timeout=AI_TIMEOUT_SECONDS,
    )

    return message.content[0].text


# ---------------------------------------------------------------------------
# Route handlers
# ---------------------------------------------------------------------------


def _handle_health():
    """GET /health — simple health check (was GET /hello in Block 0 spike)."""
    return _build_response(200, {
        "status": "healthy",
        "version": "0.2.0",
        "mock_mode": MINOU_MOCK_AI,
    })


def _handle_reading(event):
    """
    POST /reading — the main reading endpoint.

    Accepts JSON body with chart facts, returns reading_text + facts.
    On ANY error, returns 200 with in-voice error (never a 500 or stack trace).
    """
    # Parse request body
    try:
        body = json.loads(event.get("body", "{}") or "{}")
    except (json.JSONDecodeError, TypeError):
        return _build_response(400, {
            "reading_text": IN_VOICE_ERROR,
            "error": True,
            "error_detail": "Invalid JSON in request body",
            "facts": {},
        })

    facts = body.get("facts", body)  # Accept {facts: {...}} or flat facts object
    reading_type = body.get("reading_type", "natal")

    # Sanitize inputs (length caps, type coercion) — R9.5, R11.3
    facts = _sanitize_facts(facts)

    # Validate minimum required fields
    if not facts.get("cat_name"):
        return _build_response(400, {
            "reading_text": IN_VOICE_ERROR,
            "error": True,
            "error_detail": "Missing cat_name in facts",
            "facts": facts,
        })

    # --- Mock path (R4.2: validate data flow without real credentials) ---
    if MINOU_MOCK_AI:
        reading_text = _mock_reading(facts)
        return _build_response(200, {
            "reading_text": reading_text,
            "facts": facts,
            "mock": True,
        })

    # --- Real AI path ---
    try:
        reading_text = _call_anthropic_aws(facts, reading_type=reading_type)
        return _build_response(200, {
            "reading_text": reading_text,
            "facts": facts,
        })
    except Exception as e:
        # R4.5, R11.5: In-voice error on ANY failure (timeout, auth, rate limit, network)
        # Log to CloudWatch for debugging, but NEVER expose to client
        print(f"[ERROR] AnthropicAWS call failed: {type(e).__name__}: {e}")
        return _build_response(200, {
            "reading_text": IN_VOICE_ERROR,
            "error": True,
            "facts": facts,
        })


# ---------------------------------------------------------------------------
# Lambda entrypoint
# ---------------------------------------------------------------------------


def lambda_handler(event, context):
    """
    AWS Lambda handler — routes to health check or reading endpoint.

    Supports API Gateway proxy integration (event has httpMethod + path).
    """
    http_method = event.get("httpMethod", "GET")
    path = event.get("path", "/health")

    # Handle CORS preflight
    if http_method == "OPTIONS":
        return _build_response(200, {})

    # Route
    if path == "/health" and http_method == "GET":
        return _handle_health()
    elif path == "/reading" and http_method == "POST":
        return _handle_reading(event)
    else:
        # Fallback: treat GET on any path as health check (backward compat)
        if http_method == "GET":
            return _handle_health()
        return _build_response(404, {"error": "Not found"})
