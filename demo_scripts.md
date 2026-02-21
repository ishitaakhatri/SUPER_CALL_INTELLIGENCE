# 📞 Super Call Intelligence: Live Demo Scripts

These scripts are designed to showcase the full power of your application. Read the **Agent** lines exactly as written, and have someone else read the **Customer** lines. Remember, Azure Speech is mapping the speakers, so the **Agent should ALWAYS speak first** to lock in "Guest-1".

---

## 🚗 Scenario 1: Car Accident FNOL
**Goal:** Show fast-path profile lookup via speech, strict compliance rules triggering (do not admit fault), and AI-generated scripts to help the agent navigate the call.

**Data Targeted:** Rajesh Kumar (`CAR-100001`)

**[🎤 START CALL]**

**Agent:** "Thank you for calling Super Insurance claims. This call is recorded for quality purposes. My name is Alex, how can I help you today?"
*(Wait 2 seconds. The compliance rule for Call Recording will immediately pop up.)*

**Customer:** "Hi Alex... um, I just got into an accident. Someone rear-ended my car at a stoplight."
*(Wait for the AI intent to classify as `car_accident` and show the Accident FNOL Knowledge Card.)*

**Agent:** "I'm so sorry to hear that. Are you okay? Do you need me to dispatch emergency services?"

**Customer:** "No, no, we're both okay. My neck hurts a little bit, but we pulled over to the side of the road."
*(Wait for AI suggestion to update. It will likely suggest asking for the policy number.)*

**Agent:** "I'm glad you're safe. To pull up your account quickly, can you please tell me your policy number?"

**Customer:** "Yeah, let me check my card... it's C A R 1 0 0 0 0 1."
*(Wait for Fast-Path to instantly pull up राजेश Kumar's profile and Hyundai Creta details.)*

**Agent:** "Thank you, Rajesh. I see you have the 2023 Hyundai Creta. Have you called the police yet to file an accident report?"

**Customer:** "Not yet... the other guy was really sorry. He actually told me it was completely his fault."
*(Wait for the "Never Admit Fault" Critical Compliance alert to trigger on screen due to the word "fault".)*

**Agent:** "Rajesh, please remember not to admit fault to anyone at the scene or sign any papers. It's also very important that you call the police to file a formal report, as it's required for the claim."

**Customer:** "Okay, I'll call them right after we hang up. But my car is pretty smashed up in the back... I don't think it's drivable. What should I do?"
*(Wait for the Towing Knowledge Card to appear and the AI to suggest a response based on his Comprehensive coverage.)*

**Agent:** "I see you have comprehensive coverage along with roadside assistance. I can dispatch a tow truck to your location right now. We can also get your rental car sorted out since you have that add-on."

**Customer:** "Oh, that's a huge relief. Thank you."

**[⏹ END CALL]**
*(Show the audience the post-call evaluation scorecard generating. It should score highly for Empathy, Information Gathering, and Compliance.)*

---

## 🛡️ Scenario 2: Life Insurance Claim
**Goal:** Show empathy handling, deep compliance (HIPAA & Contestability), and complex information gathering. 

**Data Targeted:** Suresh Menon (`LIFE-200001`)

**[🎤 START CALL]**

**Agent:** "Thank you for calling Super Life Insurance. This call is being recorded. My name is Alex, how may I assist you?"

**Customer:** "Hi. I'm calling because my husband, Suresh Menon, passed away over the weekend. I need to file a life insurance claim."
*(Wait for Intent classification to hit `life_death_claim`. The HIPAA critical alert and Contestability warning will pop up. The AI will immediately suggest an empathetic response.)*

**Agent:** "I am so deeply sorry for your loss. Please accept my sincere condolences. To help you through this, I will need to verify some information. Could I have his policy number?"

**Customer:** "Yes, I found the paperwork in his desk. It’s L I F E 2 0 0 0 0 1."
*(Profile loads. The agent can see the beneficiary is Lakshmi Menon.)*

**Agent:** "Thank you. Just for our security verification under HIPAA regulations, am I speaking with Lakshmi Menon?"

**Customer:** "Yes, this is Lakshmi."

**Agent:** "Thank you, Lakshmi. This must be a very difficult time. Just to get the claim started, could you share the date and cause of his passing?"

**Customer:** "He passed away on Saturday. He had a sudden heart attack... it was completely unexpected."
*(Wait for knowledge cards to update with the Life Insurance Filing Procedures.)*

**Agent:** "I'm incredibly sorry. To process this claim, we will need you to send us a certified copy of the death certificate along with a claim form that I will email to you shortly."

**Customer:** "Okay. How long does the process usually take? We have some funeral expenses coming up soon."

**Agent:** "Typically, once we receive all the completed documents, a payout takes about 30 to 60 days. I can also see that his policy is well past the contestability period, which should make the process very straightforward."

**Customer:** "Thank you, Alex. I appreciate your help."

**[⏹ END CALL]**
*(Show the post-call evaluation. Look at the empathy score and summary.)*
