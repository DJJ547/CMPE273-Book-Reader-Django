import argparse
from transformers import pipeline

# Load the summarization pipeline
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

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

    # Generate summaries for each chunk
    summaries = []
    for chunk in chunks:
        summary = summarizer(chunk, max_length=150, min_length=50, do_sample=False)[0]['summary_text']
        summaries.append(summary)

    # Combine individual summaries and then re-summarize for final concise summary
    combined_summary = " ".join(summaries)
    final_summary = summarizer(combined_summary, max_length=50, min_length=25, do_sample=False)[0]['summary_text']
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
