"""
payout_skill 1.0

Agent skill: splits a payout across a list of recipients by basis points.
Used by agent deployments that pay contributors from a shared wallet.
"""

SKILL_NAME = "payout_skill"
SKILL_VERSION = "1.0"
BPS_DENOMINATOR = 10_000


def validate_splits(splits):
    if not splits:
        raise ValueError("splits must not be empty")
    total = 0
    for recipient, bps in splits:
        if not isinstance(recipient, str) or not recipient.startswith("0x") or len(recipient) != 42:
            raise ValueError("invalid recipient address")
        if bps <= 0:
            raise ValueError("bps must be positive")
        total += bps
    if total != BPS_DENOMINATOR:
        raise ValueError("splits must sum to 10000 bps")


def plan_payout(amount, splits):
    """Return a list of (recipient, amount) transfers that sum exactly to amount."""
    if amount <= 0:
        raise ValueError("amount must be positive")
    validate_splits(splits)
    transfers = []
    allocated = 0
    for recipient, bps in splits:
        share = amount * bps // BPS_DENOMINATOR
        transfers.append((recipient.lower(), share))
        allocated += share
    dust = amount - allocated
    if dust:
        first_recipient, first_share = transfers[0]
        transfers[0] = (first_recipient, first_share + dust)
    return transfers


def run(amount, splits):
    """Skill entrypoint called by the agent runtime."""
    return {
        "skill": SKILL_NAME,
        "version": SKILL_VERSION,
        "transfers": plan_payout(amount, splits),
    }
