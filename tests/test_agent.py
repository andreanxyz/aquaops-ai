import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_parse_whatsapp_message():
    from app.services.whatsapp.client import parse_incoming_message
    payload = {
        "entry": [{"changes": [{"value": {
            "messages": [{"from": "6281234567891", "id": "msg_001", "type": "text",
                          "text": {"body": "Kolam A beres pak"}, "timestamp": "1700000000"}],
            "contacts": [{"profile": {"name": "Asep"}}],
        }}]}]
    }
    result = parse_incoming_message(payload)
    assert result is not None
    assert result["from"] == "6281234567891"
    assert result["text"] == "Kolam A beres pak"
    assert result["name"] == "Asep"
    print("test_parse_whatsapp_message PASSED")

def test_knowledge_base():
    from app.services.agent.knowledge_base import load_documents, query_knowledge
    load_documents()
    result = query_knowledge("ikan nila kekurangan oksigen")
    assert len(result) > 0
    print("test_knowledge_base PASSED")

if __name__ == "__main__":
    test_parse_whatsapp_message()
    test_knowledge_base()
    print("All tests passed!")
