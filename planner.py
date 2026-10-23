from datetime import date, timedelta

import pandas as pd

from quiz_engine import DOMAINS

# Simple study topics per domain, used to label each day's focus.
TOPICS = {
    "Cloud Concepts": [
        "Cloud benefits: scalability, elasticity, high availability",
        "CapEx vs OpEx and the consumption-based model",
        "IaaS, PaaS and SaaS",
        "Shared responsibility model",
        "Public, private and hybrid cloud",
    ],
    "Azure Architecture and Services": [
        "Regions, region pairs and Availability Zones",
        "Compute: VMs, containers, App Service, Functions",
        "Networking: VNet, VPN Gateway, ExpressRoute, DNS",
        "Storage: Blob, Files, Queue, Table, redundancy options",
        "Identity: Microsoft Entra ID, MFA, Conditional Access",
    ],
    "Azure Management and Governance": [
        "Pricing calculator, TCO calculator and Cost Management",
        "Azure Policy, resource locks, tags",
        "RBAC and management groups",
        "Azure Monitor, Advisor and Service Health",
        "Resource Manager, ARM templates, CLI, PowerShell, Arc",
    ],
}


def _weights(accuracy: dict[str, float]) -> dict[str, float]:
    """Weaker domains get more study time. Unpracticed domains count as 50%."""
    gaps = {d: max(5.0, 100 - accuracy.get(d, 50.0)) for d in DOMAINS}
    total = sum(gaps.values())
    return {d: gaps[d] / total for d in DOMAINS}


def build_plan(exam_date: date, minutes_per_day: int, accuracy: dict[str, float],
               start: date | None = None) -> pd.DataFrame:
    start = start or date.today()
    days = (exam_date - start).days
    if days <= 0:
        return pd.DataFrame()

    weights = _weights(accuracy)
    # Hand out study days to domains in proportion to weakness (largest remainder).
    study_days = max(days - 1, 1)  # keep the final day for a light review
    raw = {d: weights[d] * study_days for d in DOMAINS}
    alloc = {d: int(raw[d]) for d in DOMAINS}
    leftover = study_days - sum(alloc.values())
    for d in sorted(DOMAINS, key=lambda x: raw[x] - alloc[x], reverse=True)[:leftover]:
        alloc[d] += 1

    # Interleave domains so the plan is not one long block per domain.
    queue = []
    remaining = dict(alloc)
    while any(remaining.values()):
        for d in sorted(DOMAINS, key=lambda x: remaining[x], reverse=True):
            if remaining[d] > 0:
                queue.append(d)
                remaining[d] -= 1

    rows, counters = [], {d: 0 for d in DOMAINS}
    for n in range(study_days):
        d = queue[n]
        topic = TOPICS[d][counters[d] % len(TOPICS[d])]
        counters[d] += 1
        rows.append({
            "Date": (start + timedelta(days=n)).isoformat(),
            "Focus domain": d,
            "Topic": topic,
            "Activity": f"Read Microsoft Learn on this topic, then 10 flashcards and a short quiz "
                        f"({minutes_per_day} min)",
        })

    # Every 4th study day becomes a mixed review day.
    for n in range(3, len(rows), 4):
        rows[n]["Topic"] = "Mixed review of the last 3 days"
        rows[n]["Activity"] = f"Full mixed quiz, then revisit every missed question ({minutes_per_day} min)"

    rows.append({
        "Date": exam_date.isoformat(),
        "Focus domain": "All domains",
        "Topic": "Exam day: light review only",
        "Activity": "Skim your flagged questions, rest, then sit the exam",
    })
    return pd.DataFrame(rows)