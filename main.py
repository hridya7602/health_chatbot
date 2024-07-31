from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, AutoModelForSequenceClassification
from typing import List
import re

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Load models and tokenizers
rag_model = AutoModelForCausalLM.from_pretrained("EleutherAI/gpt-neo-125M")
rag_tokenizer = AutoTokenizer.from_pretrained("EleutherAI/gpt-neo-125M")

classification_model = AutoModelForSequenceClassification.from_pretrained("distilbert-base-uncased")
classification_tokenizer = AutoTokenizer.from_pretrained("distilbert-base-uncased")
# Define input models
class RAGInput(BaseModel):
    prompt: str

class ClassificationInput(BaseModel):
    text: str

# Define a simple in-memory database for articles
articles = [
    "Article 1: Dealing with Anxiety - Tips and Techniques",
    "Article 2: Understanding Depression and Its Symptoms",
    "Article 3: The Importance of Self-Care in Mental Health",
    "Article 4: Recognizing Signs of Stress and How to Manage It",
    "Article 5: Improving Sleep Habits for Better Mental Health",
    "Article 6: Mindfulness and Meditation: Practices for Mental Wellness",
    "Article 7: Building Resilience: Coping with Life's Challenges",
    "Article 8: Understanding and Managing Panic Attacks",
    "Article 9: The Connection Between Physical Exercise and Mental Health",
    "Article 10: Healthy Eating Habits to Support Mental Well-being",
    "Article 11: Recognizing and Addressing Burnout",
    "Article 12: Strategies for Improving Self-Esteem and Confidence",
    "Article 13: Understanding Bipolar Disorder: Symptoms and Management",
    "Article 14: The Impact of Social Media on Mental Health",
    "Article 15: Coping with Grief and Loss",
    "Article 16: Understanding and Managing Obsessive-Compulsive Disorder (OCD)",
    "Article 17: The Benefits of Cognitive Behavioral Therapy (CBT)",
    "Article 18: Managing Attention-Deficit/Hyperactivity Disorder (ADHD) in Adults",
    "Article 19: Overcoming Social Anxiety: Tips and Strategies",
    "Article 20: The Role of Support Groups in Mental Health Recovery"
]

@app.post("/rag")
async def rag_endpoint(input: RAGInput):
    try:
        # Tokenize the input prompt without padding
        prompt_tokens = rag_tokenizer.encode(input.prompt, return_tensors="pt")
        
        # Generate a response with adjusted parameters
        with torch.no_grad():
            output = rag_model.generate(
                prompt_tokens,
                max_length=150, 
                num_return_sequences=1,
                no_repeat_ngram_size=3,
                temperature=0.7,
                top_k=50,
                top_p=0.95,
            )
        
        # Decode the response
        response = rag_tokenizer.decode(output[0], skip_special_tokens=True)
        
        # Post-process the response
        response = re.sub(r'\s+', ' ', response)  # Remove extra whitespace
        response = re.sub(r'(\w+)( \1)+', r'\1', response)  # Remove immediate word repetitions
        
        # Simple retrieval mechanism
        relevant_articles = [article for article in articles if any(word in article.lower() for word in input.prompt.lower().split())]
        
        return {
            "response": response.strip(),
            "relevant_articles": relevant_articles[:3]  # Return top 3 relevant articles
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/classification")
async def classification_endpoint(input: ClassificationInput):
    try:
        # Tokenize the input text
        tokens = classification_tokenizer(input.text, truncation=True, padding=True, return_tensors="pt")
        
        # Perform classification
        with torch.no_grad():
            output = classification_model(**tokens)
        
        # Get the predicted class
        predicted_class = torch.argmax(output.logits, dim=1).item()
        
        # Map the predicted class to a category
        categories = ["Anxiety", "Depression", "Stress", "Other"]
        predicted_category = categories[predicted_class]
        
        return {"category": predicted_category}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
