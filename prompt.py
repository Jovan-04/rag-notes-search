from transformers import pipeline, AutoModelForCausalLM, AutoTokenizer, TextIteratorStreamer

MODEL_NAME = 'Qwen/Qwen2.5-1.5B-Instruct'
chatbot = pipeline('text-generation', model=MODEL_NAME, dtype='auto', device_map='auto')
# tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
# model = AutoModelForCausalLM.from_pretrained(MODEL_NAME, torch_dtype='auto', device_map='auto')

def prompt(query: str) -> str:
    with open('/home/evan/evan-drake/cs-195/creative-synthesis/rag-notes-search/Notes/world_music/India.md') as notes:
        retrieved = notes.read()
    
    query = "what is raga?"

    print(f"received query {query}, generating response...")

    prompt = [
        {
            'role': 'system',
            'content': (
                'You are a study partner for a student. '
                "Answer using only the retrieved information from the student's notes when possible. "
                'If the answer is not supported by the retrieved context, say that you do not know based on the provided notes. '
            ),
        },
        {
            'role': 'user',
            'content': (
                f"Query: {query}\n\n"
                f"Retrieved course information:\n{retrieved}\n\n"
                'Please answer the question using the retrieved notes information.'
            ),
        },
    ]

    # text = tokenizer.apply_chat_template(prompt, tokenize=False, add_generation_prompt=False)

    # streamer = TextIteratorStreamer(tokenizer, skip_prompt=True, skip_special_tokens=True)
    # model_inputs = tokenizer([text])

    rag_response = chatbot(prompt)
    return rag_response[0]['generated_text'][-1]['content']