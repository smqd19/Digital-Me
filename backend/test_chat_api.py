"""
Test script for the Digital Avatar /chat API endpoint.
"""
import requests
import json

BASE_URL = "http://localhost:8000"

QUESTIONS = [
    "Tell me about yourself.",
    "What is your experience with LLMs and Generative AI?",
    "Tell me about the Bookify project.",
    "I'm looking for someone with experience in Python, FastAPI, and LLMs. Are you a good fit?",
    "What are your key achievements?",
]


def test_chat(question: str, conversation_history: list = None) -> dict:
    """Send a chat request and return the response."""
    if conversation_history is None:
        conversation_history = []
    
    payload = {
        "message": question,
        "conversation_history": conversation_history
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/chat",
            json=payload,
            timeout=120  # LLM can take a while
        )
        response.raise_for_status()
        return {"success": True, "data": response.json()}
    except requests.exceptions.RequestException as e:
        return {"success": False, "error": str(e)}


def main():
    print("=" * 60)
    print("Digital Avatar API - /chat Endpoint Tests")
    print("=" * 60)
    
    # Check if API is reachable
    try:
        health = requests.get(f"{BASE_URL}/health", timeout=5)
        print(f"\nAPI Health: {health.json()}")
    except Exception as e:
        print(f"\nERROR: Cannot reach API at {BASE_URL}")
        print(f"Make sure the server is running: uvicorn app.main:app --reload")
        print(f"Error: {e}")
        return
    
    results = []
    
    for i, question in enumerate(QUESTIONS, 1):
        print(f"\n--- Test {i}/{len(QUESTIONS)} ---")
        print(f"Question: {question}")
        
        result = test_chat(question)
        results.append({"question": question, "result": result})
        
        if result["success"]:
            data = result["data"]
            response_text = data.get("response", "")
            sources = data.get("sources", [])
            print(f"Response (first 500 chars): {response_text[:500]}...")
            if sources:
                print(f"Sources: {sources[:3]}...")
        else:
            print(f"ERROR: {result['error']}")
    
    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    
    for i, r in enumerate(results, 1):
        print(f"\n{i}. {r['question']}")
        if r["result"]["success"]:
            text = r["result"]["data"]["response"]
            summary = text[:300] + "..." if len(text) > 300 else text
            print(f"   Response: {summary}")
            first_person = any(w in text for w in ["I ", "I'm", "I am", "my ", "me "])
            print(f"   First person (I/me): {'Yes' if first_person else 'No'}")
        else:
            print(f"   ERROR: {r['result']['error']}")
    
    # Save full results for detailed analysis
    with open("test_results.json", "w") as f:
        json.dump(results, f, indent=2)
    print("\nFull results saved to test_results.json")


if __name__ == "__main__":
    main()
