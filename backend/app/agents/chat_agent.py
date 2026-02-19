"""
Agentic chat handler with tool calling capabilities.
Implements a simple but effective agent loop without heavy frameworks.
"""

import json
from openai import OpenAI
from typing import Generator

from ..prompts import SYSTEM_PROMPT
from ..tools import TOOLS, ToolExecutor
from ..models import ChatMessage


class ChatAgent:
    """
    Agentic chatbot that uses tool calling to retrieve relevant information
    before generating responses.
    """
    
    def __init__(
        self,
        openai_api_key: str,
        model_name: str,
        vector_store
    ):
        self.client = OpenAI(api_key=openai_api_key)
        self.model_name = model_name
        self.tool_executor = ToolExecutor(vector_store)
        self.max_tool_iterations = 3  # Prevent infinite loops
    
    def chat(
        self,
        user_message: str,
        conversation_history: list[ChatMessage]
    ) -> tuple[str, list[str]]:
        """
        Process a chat message and return a response.
        
        Args:
            user_message: The user's message
            conversation_history: Previous messages in the conversation
        
        Returns:
            Tuple of (response_text, list_of_sources_used)
        """
        # Build messages list
        messages = [{"role": "system", "content": SYSTEM_PROMPT}]
        
        # Add conversation history
        for msg in conversation_history[-10:]:  # Keep last 10 messages for context
            messages.append({"role": msg.role, "content": msg.content})
        
        # Add current user message
        messages.append({"role": "user", "content": user_message})
        
        sources_used = []
        
        # Agent loop with tool calling
        for iteration in range(self.max_tool_iterations):
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=messages,
                tools=TOOLS,
                tool_choice="auto"
            )
            
            assistant_message = response.choices[0].message
            
            # Check if model wants to use tools
            if assistant_message.tool_calls:
                # Add assistant message with tool calls
                messages.append({
                    "role": "assistant",
                    "content": assistant_message.content,
                    "tool_calls": [
                        {
                            "id": tc.id,
                            "type": "function",
                            "function": {
                                "name": tc.function.name,
                                "arguments": tc.function.arguments
                            }
                        }
                        for tc in assistant_message.tool_calls
                    ]
                })
                
                # Execute each tool call
                for tool_call in assistant_message.tool_calls:
                    tool_name = tool_call.function.name
                    arguments = json.loads(tool_call.function.arguments)
                    
                    # Execute the tool
                    result = self.tool_executor.execute(tool_name, arguments)
                    
                    # Track sources
                    sources_used.append(f"{tool_name}: {arguments}")
                    
                    # Add tool result to messages
                    messages.append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": result
                    })
            else:
                # No more tool calls, return the response
                return assistant_message.content or "", sources_used
        
        # If we hit max iterations, get final response
        final_response = self.client.chat.completions.create(
            model=self.model_name,
            messages=messages
        )
        
        return final_response.choices[0].message.content or "", sources_used
    
    def chat_stream(
        self,
        user_message: str,
        conversation_history: list[ChatMessage]
    ) -> Generator[str, None, None]:
        """
        Stream a chat response.
        
        Note: Tool calls are executed first (non-streaming), then the final
        response is streamed for better UX.
        """
        # Build messages list
        messages = [{"role": "system", "content": SYSTEM_PROMPT}]
        
        # Add conversation history
        for msg in conversation_history[-10:]:
            messages.append({"role": msg.role, "content": msg.content})
        
        # Add current user message
        messages.append({"role": "user", "content": user_message})
        
        # First, execute any needed tool calls (non-streaming)
        for iteration in range(self.max_tool_iterations):
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=messages,
                tools=TOOLS,
                tool_choice="auto"
            )
            
            assistant_message = response.choices[0].message
            
            if assistant_message.tool_calls:
                # Add assistant message with tool calls
                messages.append({
                    "role": "assistant",
                    "content": assistant_message.content,
                    "tool_calls": [
                        {
                            "id": tc.id,
                            "type": "function",
                            "function": {
                                "name": tc.function.name,
                                "arguments": tc.function.arguments
                            }
                        }
                        for tc in assistant_message.tool_calls
                    ]
                })
                
                # Execute each tool call
                for tool_call in assistant_message.tool_calls:
                    tool_name = tool_call.function.name
                    arguments = json.loads(tool_call.function.arguments)
                    result = self.tool_executor.execute(tool_name, arguments)
                    
                    messages.append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": result
                    })
            else:
                # No tool calls, break to streaming phase
                break
        
        # Now stream the final response
        stream = self.client.chat.completions.create(
            model=self.model_name,
            messages=messages,
            stream=True
        )
        
        for chunk in stream:
            if chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content
