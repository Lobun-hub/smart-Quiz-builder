import os

from ai_client import ai_available, get_client

SYSTEM_PROMPT = """You are an AZ-900 (Microsoft Azure Fundamentals) study buddy.
Explain cloud concepts in simple, friendly language for beginners.
Rules:
- Start with a one-sentence plain-English definition.
- Then give a short real-world analogy.
- Then add 2-3 bullet points on what the AZ-900 exam typically tests about it.
- Keep answers under 200 words unless the learner asks for more depth.
- If you are unsure about a recent Azure change (names, pricing, limits), say so and
  point the learner to Microsoft Learn rather than guessing.
- Politely steer off-topic questions back to Azure or cloud fundamentals."""

OFFLINE_EXPLANATIONS = (
    (
        ("iaas", "paas", "saas"),
        "**IaaS, PaaS, and SaaS** are cloud service models that offer "
        "different levels of management.\n\n"
        "Think of them as renting a kitchen: with IaaS you manage the "
        "appliances, with PaaS the kitchen is ready to cook in, and with "
        "SaaS you order a finished meal.\n\n"
        "- **IaaS** gives you virtual machines and networking to manage.\n"
        "- **PaaS** lets you deploy apps without managing the underlying OS.\n"
        "- **SaaS** is ready-to-use software managed by the provider.",
    ),
    (
        ("availability zone",),
        "**Availability Zones** are separate physical locations within an "
        "Azure region, each with independent power, cooling, and networking.\n\n"
        "They are like nearby branches of the same service that can keep "
        "operating if one location has a problem.\n\n"
        "- Use zone-redundant services to improve resilience to datacenter "
        "failures.\n"
        "- Zones are connected by a low-latency network.\n"
        "- A region may have multiple zones; not every service supports them.",
    ),
    (
        ("azure policy", "rbac", "role-based access"),
        "**Azure Policy** enforces rules about resource configuration, while "
        "**RBAC** controls who can perform actions on resources.\n\n"
        "Policy is like a building code; RBAC is like deciding who has a key "
        "to each room.\n\n"
        "- Policy can audit or deny non-compliant resource settings.\n"
        "- RBAC assigns roles to users, groups, or applications.\n"
        "- They solve different governance and access-control problems.",
    ),
    (
        ("shared responsibility",),
        "The **shared responsibility model** describes which security tasks "
        "belong to the cloud provider and which belong to the customer.\n\n"
        "It is like renting a secure building: the landlord maintains the "
        "structure, while you protect what you bring inside.\n\n"
        "- Azure manages physical datacenters and core infrastructure.\n"
        "- Customers always manage their data, identities, and access.\n"
        "- Customer responsibility generally increases from SaaS to IaaS.",
    ),
    (
        ("capex", "opex"),
        "**CapEx** is upfront spending on physical assets; **OpEx** is "
        "ongoing spending for services as you use them.\n\n"
        "Buying a car is like CapEx; paying for rides when needed is like OpEx.\n\n"
        "- Traditional datacenters often require upfront hardware investment.\n"
        "- Cloud services commonly use a consumption-based OpEx model.\n"
        "- The pricing calculator can help estimate Azure costs.",
    ),
)


def buddy_available() -> bool:
    return ai_available()


def offline_reply(question: str) -> str:
    """Answer common AZ-900 topics from built-in content without an API."""
    normalized_question = question.casefold()
    for keywords, explanation in OFFLINE_EXPLANATIONS:
        if any(keyword in normalized_question for keyword in keywords):
            return explanation

    return (
        "I’m in offline mode, so I can answer a set of built-in AZ-900 topics "
        "rather than generate a new response. Try **IaaS vs PaaS vs SaaS**, "
        "**Availability Zones**, **Azure Policy vs RBAC**, the **shared "
        "responsibility model**, or **CapEx vs OpEx**. "
        "For another topic, check Microsoft Learn."
    )


def ask_buddy(history: list[dict]) -> str:
    """history is a list of {"role": "user"|"assistant", "content": str}."""
    if not buddy_available():
        question = next(
            (
                message.get("content", "")
                for message in reversed(history)
                if message.get("role") == "user"
            ),
            "",
        )
        return offline_reply(question)

    client = get_client()
    model = os.getenv("ANTHROPIC_MODEL", "claude-sonnet-5-5")
    response = client.messages.create(
        model=model,
        max_tokens=800,
        system=SYSTEM_PROMPT,
        messages=history,
    )
    return response.content[0].text