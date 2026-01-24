"""
15. Hugging Face & Instruction-Tuned Models
============================================
Demonstrates how to use Hugging Face Transformers library to run
instruction-tuned models locally.

Key Concepts:
- Loading models from Hugging Face Hub
- Instruction-tuned vs base models
- Tokenization and generation
- Model quantization for efficiency
- Popular instruction-tuned models

Prerequisites:
pip install transformers torch accelerate bitsandbytes sentencepiece
"""

import torch
from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM,
    pipeline,
    BitsAndBytesConfig
)
import warnings
warnings.filterwarnings('ignore')


# Check available device
device = "cuda" if torch.cuda.is_available() else "mps" if torch.backends.mps.is_available() else "cpu"
print("=" * 60)
print("System Information")
print("=" * 60)
print(f"\n🖥️  Device: {device}")
print(f"🐍 PyTorch Version: {torch.__version__}")
print(f"🤗 Transformers: Available\n")


# Example 1: Using a Small Instruction-Tuned Model (Flan-T5)
print("=" * 60)
print("Example 1: Flan-T5 (Instruction-Tuned)")
print("=" * 60)

print("\n📦 Loading Flan-T5-Small (80M parameters)...")
print("   This is a small, fast model good for learning.\n")

try:
    from transformers import T5ForConditionalGeneration
    
    model_name = "google/flan-t5-small"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = T5ForConditionalGeneration.from_pretrained(model_name)
    
    # Move to device
    model = model.to(device)
    
    # Test prompts
    prompts = [
        "Translate to French: Hello, how are you?",
        "Summarize: Artificial intelligence is transforming industries worldwide.",
        "Answer: What is the capital of France?"
    ]
    
    for prompt in prompts:
        print(f"📝 Prompt: {prompt}")
        
        inputs = tokenizer(prompt, return_tensors="pt").to(device)
        outputs = model.generate(**inputs, max_length=100)
        response = tokenizer.decode(outputs[0], skip_special_tokens=True)
        
        print(f"🤖 Response: {response}\n")

except Exception as e:
    print(f"⚠️  Could not load Flan-T5: {e}")
    print("   Continuing with other examples...\n")


# Example 2: Using Pipeline API (Easiest Method)
print("=" * 60)
print("Example 2: Pipeline API (Simplified)")
print("=" * 60)

print("\n📦 Loading model with pipeline...\n")

try:
    # Create a text generation pipeline
    generator = pipeline(
        "text-generation",
        model="distilgpt2",  # Small model for demo
        device=0 if device == "cuda" else -1
    )
    
    prompt = "The future of artificial intelligence is"
    
    print(f"📝 Prompt: {prompt}")
    
    outputs = generator(
        prompt,
        max_length=50,
        num_return_sequences=2,
        temperature=0.8,
        do_sample=True
    )
    
    print(f"\n🤖 Generated Responses:\n")
    for i, output in enumerate(outputs, 1):
        print(f"{i}. {output['generated_text']}\n")

except Exception as e:
    print(f"⚠️  Pipeline error: {e}\n")


# Example 3: Instruction-Tuned Model with Proper Formatting
print("=" * 60)
print("Example 3: Instruction-Tuned Model (Proper Format)")
print("=" * 60)

print("""
📚 Popular Instruction-Tuned Models:

Small (< 1B params):
- google/flan-t5-small (80M) - Fast, good for learning
- google/flan-t5-base (250M) - Better quality
- microsoft/phi-2 (2.7B) - Strong performance

Medium (3-7B params):
- meta-llama/Llama-2-7b-chat-hf (7B) - Requires auth
- mistralai/Mistral-7B-Instruct-v0.2 (7B) - Strong
- HuggingFaceH4/zephyr-7b-beta (7B) - Excellent

Large (13B+ params):
- meta-llama/Llama-2-13b-chat-hf (13B)
- mistralai/Mixtral-8x7B-Instruct-v0.1 (47B)

Note: Larger models require more RAM/VRAM
""")


# Example 4: Model Quantization (4-bit) for Efficiency
print("=" * 60)
print("Example 4: 4-bit Quantization (Memory Efficient)")
print("=" * 60)

print("""
💡 Quantization reduces model size and memory usage:
- FP32 (full precision): 4 bytes per parameter
- FP16 (half precision): 2 bytes per parameter
- INT8 (8-bit): 1 byte per parameter
- INT4 (4-bit): 0.5 bytes per parameter

Example: 7B model
- FP32: ~28GB
- FP16: ~14GB
- INT8: ~7GB
- INT4: ~3.5GB

This makes large models runnable on consumer hardware!
""")

try:
    # Configure 4-bit quantization
    quantization_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_compute_dtype=torch.float16,
        bnb_4bit_use_double_quant=True,
        bnb_4bit_quant_type="nf4"
    )
    
    print("\n📦 Loading quantized model (if GPU available)...\n")
    
    if device == "cuda":
        model_name = "google/flan-t5-base"
        
        tokenizer_q = AutoTokenizer.from_pretrained(model_name)
        model_q = T5ForConditionalGeneration.from_pretrained(
            model_name,
            quantization_config=quantization_config,
            device_map="auto"
        )
        
        prompt = "Explain quantum computing in simple terms."
        print(f"📝 Prompt: {prompt}")
        
        inputs = tokenizer_q(prompt, return_tensors="pt").to("cuda")
        outputs = model_q.generate(**inputs, max_length=100)
        response = tokenizer_q.decode(outputs[0], skip_special_tokens=True)
        
        print(f"🤖 Response: {response}\n")
    else:
        print("⚠️  Quantization requires CUDA GPU. Skipping...\n")

except Exception as e:
    print(f"⚠️  Quantization example failed: {e}\n")


# Example 5: Chat Template Formatting
print("=" * 60)
print("Example 5: Chat Template Formatting")
print("=" * 60)

print("""
🎯 Instruction-tuned models expect specific formats:

Alpaca Format:
```
Below is an instruction that describes a task.

### Instruction:
{instruction}

### Response:
```

ChatML Format:
```
<|im_start|>user
{message}<|im_end|>
<|im_start|>assistant
```

LLaMA-2 Format:
```
<s>[INST] {message} [/INST]
```

Always check the model card for the correct format!
""")


# Example 6: Practical Use Case - Text Classification
print("=" * 60)
print("Example 6: Text Classification with Instruction Model")
print("=" * 60)

try:
    classifier = pipeline(
        "text-classification",
        model="distilbert-base-uncased-finetuned-sst-2-english",
        device=0 if device == "cuda" else -1
    )
    
    texts = [
        "I love this product! It's amazing!",
        "This is terrible. Waste of money.",
        "It's okay, nothing special."
    ]
    
    print("\n📊 Sentiment Classification:\n")
    
    for text in texts:
        result = classifier(text)[0]
        print(f"Text: {text}")
        print(f"Sentiment: {result['label']} (confidence: {result['score']:.2%})\n")

except Exception as e:
    print(f"⚠️  Classification error: {e}\n")


# Example 7: Question Answering
print("=" * 60)
print("Example 7: Question Answering")
print("=" * 60)

try:
    qa_pipeline = pipeline(
        "question-answering",
        model="distilbert-base-cased-distilled-squad",
        device=0 if device == "cuda" else -1
    )
    
    context = """
    Python is a high-level, interpreted programming language. 
    It was created by Guido van Rossum and first released in 1991. 
    Python emphasizes code readability and uses significant indentation.
    """
    
    questions = [
        "Who created Python?",
        "When was Python first released?",
        "What does Python emphasize?"
    ]
    
    print("\n❓ Question Answering:\n")
    print(f"Context: {context}\n")
    
    for question in questions:
        result = qa_pipeline(question=question, context=context)
        print(f"Q: {question}")
        print(f"A: {result['answer']} (confidence: {result['score']:.2%})\n")

except Exception as e:
    print(f"⚠️  QA error: {e}\n")


# Example 8: Text Summarization
print("=" * 60)
print("Example 8: Text Summarization")
print("=" * 60)

try:
    summarizer = pipeline(
        "summarization",
        model="facebook/bart-large-cnn",
        device=0 if device == "cuda" else -1
    )
    
    article = """
    Artificial intelligence has made remarkable progress in recent years. 
    Machine learning algorithms can now perform tasks that were once thought 
    to require human intelligence, such as image recognition, natural language 
    processing, and game playing. Deep learning, a subset of machine learning, 
    uses neural networks with multiple layers to learn hierarchical representations 
    of data. This has led to breakthroughs in computer vision, speech recognition, 
    and language translation. However, challenges remain, including the need for 
    large amounts of training data, computational resources, and addressing ethical 
    concerns around bias and fairness in AI systems.
    """
    
    print("\n📄 Original Text:")
    print(article)
    
    summary = summarizer(article, max_length=50, min_length=25, do_sample=False)
    
    print(f"\n📝 Summary:")
    print(summary[0]['summary_text'])
    print()

except Exception as e:
    print(f"⚠️  Summarization error: {e}\n")


# Best Practices
print("=" * 60)
print("📚 Hugging Face Best Practices")
print("=" * 60)
print("""
1. Model Selection:
   ✅ Start with small models for testing
   ✅ Check model card for requirements
   ✅ Verify license for your use case
   ✅ Consider quantized versions

2. Memory Management:
   ✅ Use quantization for large models
   ✅ Clear cache: torch.cuda.empty_cache()
   ✅ Use device_map="auto" for multi-GPU
   ✅ Batch processing for efficiency

3. Generation Parameters:
   ✅ max_length: Control output length
   ✅ temperature: Randomness (0.0-2.0)
   ✅ top_p: Nucleus sampling
   ✅ top_k: Limit token selection
   ✅ do_sample: Enable sampling

4. Performance Optimization:
   ✅ Use pipeline API when possible
   ✅ Batch inputs together
   ✅ Use GPU if available
   ✅ Cache models locally

5. Prompt Engineering:
   ✅ Follow model's expected format
   ✅ Be specific and clear
   ✅ Provide examples (few-shot)
   ✅ Test different phrasings

Common Issues:
- Out of memory: Use smaller model or quantization
- Slow inference: Use GPU or smaller model
- Poor quality: Try different model or better prompt
- Format errors: Check model card for correct format

Resources:
- Model Hub: https://huggingface.co/models
- Documentation: https://huggingface.co/docs/transformers
- Tutorials: https://huggingface.co/learn
- Community: https://discuss.huggingface.co
""")


# Comparison Table
print("=" * 60)
print("📊 Model Comparison")
print("=" * 60)
print("""
| Model | Size | Speed | Quality | Use Case |
|-------|------|-------|---------|----------|
| Flan-T5-Small | 80M | ⚡⚡⚡ | ⭐⭐ | Learning, Testing |
| Flan-T5-Base | 250M | ⚡⚡ | ⭐⭐⭐ | General Tasks |
| Phi-2 | 2.7B | ⚡⚡ | ⭐⭐⭐⭐ | Coding, Reasoning |
| Mistral-7B | 7B | ⚡ | ⭐⭐⭐⭐⭐ | Production |
| LLaMA-2-13B | 13B | ⚡ | ⭐⭐⭐⭐⭐ | High Quality |

Hardware Requirements:
- CPU Only: Flan-T5-Small/Base, DistilGPT2
- 8GB GPU: Phi-2, Mistral-7B (quantized)
- 16GB GPU: Mistral-7B (full), LLaMA-2-7B
- 24GB+ GPU: LLaMA-2-13B, Mixtral-8x7B
""")

print("\n✅ Hugging Face Examples Complete!\n")
