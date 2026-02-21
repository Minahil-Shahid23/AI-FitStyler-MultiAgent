  
import random 

current_trends = [
    "Oversized jackets and hoodies for casual",
    "Sustainable fabrics and high-waist jeans for slim bodies",
    "Floral prints and A-line dresses for party/curvy",
    "Neutral colors like beige for office/male"
]

def critique_trends(suggestions, occasion, body_type, gender):
    """
    Suggestions pe trends check kar, score de (1-10).
    Returns: List with trend score and comment (with variation, no LLM).
    """
    critiqued = []
    scores = ["7/10", "8/10", "9/10", "10/10"]
    comment_templates = [
        f"Totally trending for {occasion} – love the {body_type} fit! 😎",
        f"Perfect match for {occasion} vibe, suits {body_type} body type! ✨",
        f"Hot trend alert for {occasion} – {body_type} friendly and stylish! 🔥",
        f"Spot on for {occasion} – enhances your {body_type} shape beautifully! 💫"
    ]
    
    for sug in suggestions:
        content = sug.get('content', '')
        score = random.choice(scores)  
        comment = random.choice(comment_templates) 
        
        critiqued.append({**sug, 'trend_score': score, 'trend_comment': comment})
    
    return critiqued





















    
    
    
    
    
    
    
    
    
    
    
    
# from langchain_ollama import OllamaLLM 
# llm = OllamaLLM(model="llama3.2")


# current_trends = [
#     "Oversized jackets and hoodies for casual",
#     "Sustainable fabrics and high-waist jeans for slim bodies",
#     "Floral prints and A-line dresses for party/curvy",
#     "Neutral colors like beige for office/male"
# ]

# def critique_trends(suggestions, occasion, body_type, gender):
   
#     critiqued = []
#     for sug in suggestions:
#         content = sug.get('content', '')
#         prompt = f"""
#         Current trends: {', '.join(current_trends)}.
#         Rate this outfit {sug['name']} for {gender} {body_type} body, {occasion} occasion.
#         Give a score 1-10 and why (e.g., '9/10 – Totally trending!').
#         Keep it short and exciting.
#         """
#         critique = llm.invoke(prompt)
        
#         # Simple parse (assume "8/10 - Comment")
#         if '/10' in critique:
#             score = critique.split('/10')[0].strip() + '/10'
#             comment = critique.split('-')[1].strip() if '-' in critique else critique
#         else:
#             score = "7/10"
#             comment = critique[:100]
        
#         critiqued.append({**sug, 'trend_score': score, 'trend_comment': comment})
    
#     return critiqued