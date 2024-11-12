import argparse
from transformers import pipeline

# Load the text generation pipeline with GPT-2
generator = pipeline("text-generation", model="gpt2")

# Function to split text into manageable chunks
def chunk_text(text, max_chunk_length=500):
    sentences = text.split(". ")
    current_chunk = ""
    chunks = []
    
    for sentence in sentences:
        if len(current_chunk) + len(sentence) <= max_chunk_length:
            current_chunk += sentence + ". "
        else:
            chunks.append(current_chunk.strip())
            current_chunk = sentence + ". "
    if current_chunk:
        chunks.append(current_chunk.strip())
    
    return chunks

def summarize_large_text(text):
    # Split the large text into chunks
    chunks = chunk_text(text)

    # Generate summaries for each chunk by instructing GPT-2 to "summarize"
    summaries = []
    for chunk in chunks:
        prompt = f"Summarize the following text: {chunk}\nSummary:"
        summary = generator(prompt, max_new_tokens=50, num_return_sequences=1, do_sample=False)[0]['generated_text']
        
        # Extract the summary portion by splitting at "Summary:"
        summary_text = summary.split("Summary:")[-1].strip()
        summaries.append(summary_text)

    # Combine individual summaries and then re-summarize for final concise summary
    combined_summary = " ".join(summaries)
    final_prompt = f"Summarize the following text into a short paragraph: {combined_summary}\nSummary:"
    final_summary = generator(final_prompt, max_new_tokens=30, num_return_sequences=1, do_sample=False)[0]['generated_text'].split("Summary:")[-1].strip()
    return final_summary

if __name__ == "__main__":
    # Set up command-line argument parsing
    parser = argparse.ArgumentParser(description="Summarize large text input into a concise 5-7 sentence summary.")
    parser.add_argument("text", type=str, help="The text to summarize")
    args = parser.parse_args()
    
    # Generate and print the summary
    summary = summarize_large_text(args.text)
    print("Final Summary:")
    print(summary)
