"""
Tool definitions for the agentic chatbot.
These tools enable the LLM to search and retrieve information from the knowledge base.
"""

from typing import Any

# Tool definitions for OpenAI function calling
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "search_experience",
            "description": "Search for relevant work experience based on a query. Use this when the user asks about work history, roles, companies, or specific job-related achievements.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The search query about work experience (e.g., 'LLM engineering experience', 'team leadership roles')"
                    }
                },
                "required": ["query"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "search_projects",
            "description": "Search for relevant projects based on a query. Use this when the user asks about specific projects, technical implementations, or portfolio work.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The search query about projects (e.g., 'voice AI projects', 'chatbot implementations')"
                    }
                },
                "required": ["query"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "search_skills",
            "description": "Search for information about technical skills and competencies. Use this when the user asks about specific technologies, tools, or skill levels.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The search query about skills (e.g., 'Python expertise', 'cloud platforms')"
                    }
                },
                "required": ["query"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "match_requirements",
            "description": "Match job requirements against skills and experience. Use this when the user provides job requirements or asks if Qasim is a good fit for a role.",
            "parameters": {
                "type": "object",
                "properties": {
                    "requirements": {
                        "type": "string",
                        "description": "The job requirements or role description to match against"
                    }
                },
                "required": ["requirements"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_profile_overview",
            "description": "Get a general overview of Qasim's profile, including summary, core competencies, and key highlights. Use this for introductory questions or general 'tell me about yourself' queries.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_education_certifications",
            "description": "Get information about education background and professional certifications.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    }
]


class ToolExecutor:
    """Executes tool calls using the vector store."""
    
    def __init__(self, vector_store):
        self.vector_store = vector_store
    
    def execute(self, tool_name: str, arguments: dict[str, Any]) -> str:
        """Execute a tool and return the result as a string."""
        
        if tool_name == "search_experience":
            results = self.vector_store.search(
                query=arguments["query"],
                n_results=3,
                filter_type="experience"
            )
            return self._format_results(results, "Experience")
        
        elif tool_name == "search_projects":
            results = self.vector_store.search(
                query=arguments["query"],
                n_results=4,
                filter_type="project"
            )
            return self._format_results(results, "Projects")
        
        elif tool_name == "search_skills":
            # Search both skills and experience for comprehensive skill info
            skill_results = self.vector_store.search(
                query=arguments["query"],
                n_results=2,
                filter_type="skills"
            )
            exp_results = self.vector_store.search(
                query=arguments["query"],
                n_results=2,
                filter_type="experience"
            )
            combined = skill_results + exp_results
            return self._format_results(combined, "Skills & Experience")
        
        elif tool_name == "match_requirements":
            # Broad search across all types for requirement matching
            results = self.vector_store.search(
                query=arguments["requirements"],
                n_results=6
            )
            return self._format_results(results, "Matching Experience & Skills")
        
        elif tool_name == "get_profile_overview":
            # Get profile and achievements
            profile_results = self.vector_store.search(
                query="professional profile summary core competencies",
                n_results=2,
                filter_type="profile"
            )
            achievement_results = self.vector_store.search(
                query="key achievements career highlights",
                n_results=1,
                filter_type="achievements"
            )
            combined = profile_results + achievement_results
            return self._format_results(combined, "Profile Overview")
        
        elif tool_name == "get_education_certifications":
            edu_results = self.vector_store.search(
                query="education degree university",
                n_results=2,
                filter_type="education"
            )
            cert_results = self.vector_store.search(
                query="certifications credentials",
                n_results=1,
                filter_type="certifications"
            )
            combined = edu_results + cert_results
            return self._format_results(combined, "Education & Certifications")
        
        else:
            return f"Unknown tool: {tool_name}"
    
    def _format_results(self, results: list[dict], title: str) -> str:
        """Format search results for LLM consumption."""
        if not results:
            return f"No {title.lower()} found matching the query."
        
        formatted_parts = [f"=== {title} ===\n"]
        for i, result in enumerate(results, 1):
            formatted_parts.append(f"--- Result {i} ---")
            formatted_parts.append(result["content"])
            formatted_parts.append("")
        
        return "\n".join(formatted_parts)
