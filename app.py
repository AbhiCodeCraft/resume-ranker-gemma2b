from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
model_id = "google/gemma-2b"

tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForCausalLM.from_pretrained(model_id, device_map="auto")

generator = pipeline("text-generation", model=model, tokenizer=tokenizer)

def rank_resumes(job_desc, resume1, resume2, resume3):
    prompt = f"""
You are an expert recruiter. Here's a job description:

{job_desc}

Three resumes have been submitted:
Resume A: {resume1}
Resume B: {resume2}
Resume C: {resume3}

Please rank the resumes from most to least suitable. Briefly explain your reasoning.
"""

    result = generator(prompt, max_new_tokens=200, do_sample=False)[0]["generated_text"]

    # Only show the result after the prompt
    return result[len(prompt):].strip()

import gradio as gr
import gradio as gr

demo = gr.Interface(
    fn=rank_resumes,
    inputs=[
        gr.Textbox(lines=5, label="Job Description"),
        gr.Textbox(lines=5, label="Resume A"),
        gr.Textbox(lines=5, label="Resume B"),
        gr.Textbox(lines=5, label="Resume C")
    ],
    outputs=gr.Textbox(label="Ranked Resumes + Explanation"),
    title="🧠 Resume Ranker (Open-Source LLM)",
    description="Uses Google Gemma-2B model. Paste job description + resumes. It ranks them with an explanation."
)