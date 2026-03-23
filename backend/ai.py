import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

my_api_key = os.getenv("GOOGLE_API_KEY")

genai.configure(api_key=my_api_key)

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def buildSystemPrompt(profile: dict) -> str:
    """
    Constructs a personalized system prompt based on the learner's dynamic profile data.
    """
    name = profile.get("name", "Student")
    grade = profile.get("grade", "their grade")
    board = profile.get("board", "their board")
    scores = profile.get("subject_scores", {})
    hobbies = profile.get("hobbies", [])
    style = profile.get("learning_style", "visual")
    dependency = profile.get("dependency_level", "main")

    weak_subjects = [subj for subj, score in scores.items() if score <= 2]
    strong_subjects = [subj for subj, score in scores.items() if score >= 4]

    prompt = (
        f"You are StudyAI, an expert, encouraging, and highly personalized digital learning assistant for {name}, "
        f"who is a {grade} student studying under the {board} curriculum.\n\n"
    )

    prompt += "CORE BEHAVIOR:\n"
    prompt += "- Never just give direct answers to homework or questions. Guide the student to discover the answer themselves.\n"
    prompt += "- Break down complex topics into bite-sized, easy-to-understand pieces.\n"
    prompt += "- Use the Socratic method: ask probing questions to check their understanding.\n"

    prompt += "\nPERSONALIZATION INSTRUCTIONS:\n"
    
    if style:
        prompt += f"- Learning Style: The student prefers a '{style}' approach. Adapt your explanations to fit this. (e.g., if visual, use rich descriptive imagery or clear text layouts; if reading, provide well-structured notes; if doing, suggest micro-experiments).\n"
    
    if hobbies:
        hobbies_str = ", ".join(hobbies)
        prompt += f"- Interests: Actively use analogies related to their hobbies ({hobbies_str}) to make difficult academic concepts relatable and engaging.\n"
    
    if weak_subjects:
        weak_str = ", ".join(weak_subjects)
        prompt += f"- Weak Subjects: Be exceptionally patient, encouraging, and step-by-step when discussing {weak_str}.\n"
    
    if strong_subjects:
        strong_str = ", ".join(strong_subjects)
        prompt += f"- Strong Subjects: Challenge them with advanced critical thinking and application questions in {strong_str}.\n"
    
    if dependency:
        prompt += f"- Support Level: The student's dependency level is '{dependency}'. Adjust your level of hand-holding accordingly.\n"

    return prompt

async def ask_ai(user_message: str, chat_history: list, profile: dict) -> str:
    """
    Initializes Gemini with the personalized system prompt, passes the chat history, 
    and streams or returns the generated response.
    """
    system_instruction = buildSystemPrompt(profile)

    model = genai.GenerativeModel(
        model_name="gemini-2.5-flash",
        system_instruction=system_instruction
    )

    formatted_history = []
    for msg in chat_history:
        # Convert frontend 'assistant' role to Gemini's 'model' role
        role = "model" if msg.get("role") == "assistant" else "user"
        formatted_history.append({
            "role": role,
            "parts": [msg.get("content", "")]
        })

    chat = model.start_chat(history=formatted_history)

    response = chat.send_message(user_message)
    
    return response.text
