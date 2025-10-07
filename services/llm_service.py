import os
import time
from groq import Groq
from opentelemetry import trace, metrics
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Groq client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Get tracer
tracer = trace.get_tracer(__name__)

# Get meter for metrics
meter = metrics.get_meter(__name__)

# Create metrics
llm_request_counter = meter.create_counter(
    name="llm_requests_total",
    description="Total number of LLM requests",
    unit="1"
)

llm_response_time = meter.create_histogram(
    name="llm_response_time_seconds",
    description="LLM response time in seconds",
    unit="s"
)

llm_token_counter = meter.create_counter(
    name="llm_tokens_total",
    description="Total tokens used",
    unit="1"
)

async def generate_completion(prompt: str, max_tokens: int = 100, temperature: float = 0.7):
    """
    Generate completion using Groq LLM with full tracing and metrics
    """
    with tracer.start_as_current_span("llm_generate_completion") as span:
        # Add span attributes
        span.set_attribute("llm.provider", "groq")
        span.set_attribute("llm.model", "llama-3.1-8b-instant")
        span.set_attribute("llm.prompt", prompt)
        span.set_attribute("llm.max_tokens", max_tokens)
        span.set_attribute("llm.temperature", temperature)

        start_time = time.time()

        try:
            # Make LLM API call
            chat_completion = client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
                model="llama-3.1-8b-instant",
                max_tokens=max_tokens,
                temperature=temperature,
            )

            # Extract response
            response_text = chat_completion.choices[0].message.content
            tokens_used = chat_completion.usage.total_tokens

            # Calculate response time
            response_time = time.time() - start_time

            # Add metrics (only if meters are available)
            if llm_request_counter:
                llm_request_counter.add(1, {"model": "llama-3.1-8b-instant", "status": "success"})
            if llm_response_time:
                llm_response_time.record(response_time, {"model": "llama-3.1-8b-instant"})
            if llm_token_counter:
                llm_token_counter.add(tokens_used, {"model": "llama-3.1-8b-instant"})

            # Add span attributes for response
            span.set_attribute("llm.response_time", response_time)
            span.set_attribute("llm.tokens_used", tokens_used)
            span.set_attribute("llm.status", "success")

            return {
                "response": response_text,
                "model": "llama-3.1-8b-instant",
                "tokens_used": tokens_used
            }

        except Exception as e:
            # Record error in span
            span.set_attribute("llm.status", "error")
            span.set_attribute("error.message", str(e))
            span.record_exception(e)

            # Increment error counter
            if llm_request_counter:
                llm_request_counter.add(1, {"model": "llama-3.1-8b-instant", "status": "error"})

            raise e
