import study_buddy


def test_offline_iaas_paas_saas_explanation():
    response = study_buddy.offline_reply("Explain IaaS vs PaaS vs SaaS")

    assert "IaaS, PaaS, and SaaS" in response
    assert "**IaaS**" in response
    assert "**PaaS**" in response
    assert "**SaaS**" in response


def test_offline_availability_zone_explanation():
    response = study_buddy.offline_reply("What are Availability Zones?")

    assert "separate physical locations" in response
    assert "low-latency" in response


def test_offline_reply_uses_latest_user_question(monkeypatch):
    monkeypatch.setattr(study_buddy, "buddy_available", lambda: False)

    response = study_buddy.ask_buddy(
        [
            {"role": "user", "content": "What is CapEx?"},
            {"role": "assistant", "content": "An earlier answer."},
            {"role": "user", "content": "What is RBAC?"},
        ]
    )

    assert "Azure Policy" in response
    assert "CapEx" not in response


def test_offline_unknown_topic_suggests_supported_topics():
    response = study_buddy.offline_reply("How do Azure savings plans work?")

    assert "in offline mode" in response
    assert "Availability Zones" in response
    assert "Microsoft Learn" in response


def test_online_mode_uses_anthropic_client(monkeypatch):
    expected_response = "Generated answer."

    class FakeMessages:
        def create(self, **kwargs):
            return type(
                "FakeResponse",
                (),
                {"content": [type("Text", (), {"text": expected_response})()]},
            )()

    class FakeClient:
        messages = FakeMessages()

    monkeypatch.setattr(study_buddy, "buddy_available", lambda: True)
    monkeypatch.setattr(study_buddy, "get_client", lambda: FakeClient())

    response = study_buddy.ask_buddy(
        [{"role": "user", "content": "Explain Azure Policy"}]
    )

    assert response == expected_response
