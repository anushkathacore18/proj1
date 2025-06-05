def evaluate_output(response, expected_quality=4):
    print("\n📊 Evaluating output quality...")
    length = len(response.split())

    if length < 5:
        print("❌ Response too short: Poor quality.")
    elif length > 30 and expected_quality >= 4:
        print("✅ High quality response.")
    else:
        print("⚠️ Medium quality. Needs improvement.")
