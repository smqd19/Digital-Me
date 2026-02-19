import json
from pathlib import Path
from typing import Any


def load_knowledge_base(path: str) -> dict[str, Any]:
    """Load the knowledge base JSON file."""
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def create_chunks(knowledge_base: dict[str, Any]) -> list[dict[str, Any]]:
    """
    Create semantic chunks from the knowledge base for vector storage.
    Each chunk contains text content and metadata for filtering.
    """
    chunks = []
    
    # Profile chunk
    profile = knowledge_base.get("profile", {})
    profile_text = f"""
Profile: {profile.get('name', '')}
Title: {profile.get('title', '')}
Experience: {profile.get('years_of_experience', '')} years
Location: {profile.get('location', '')}

Summary: {profile.get('summary', '')}

Core Competencies: {', '.join(profile.get('core_competencies', []))}
"""
    chunks.append({
        "id": "profile",
        "text": profile_text.strip(),
        "metadata": {"type": "profile", "category": "overview"}
    })
    
    # Experience chunks
    for exp in knowledge_base.get("experience", []):
        exp_text = f"""
Work Experience: {exp.get('role', '')} at {exp.get('company', '')}
Duration: {exp.get('duration', '')}
Type: {exp.get('type', '')}
Location: {exp.get('location', '')}

Description: {exp.get('description', '')}

Key Achievements:
{chr(10).join('- ' + a for a in exp.get('achievements', []))}

Technologies Used: {', '.join(exp.get('technologies', []))}

Skills Demonstrated: {', '.join(exp.get('skills_demonstrated', []))}
"""
        chunks.append({
            "id": exp.get("id", ""),
            "text": exp_text.strip(),
            "metadata": {
                "type": "experience",
                "company": exp.get("company", ""),
                "role": exp.get("role", ""),
                "technologies": exp.get("technologies", [])
            }
        })
    
    # Project chunks
    for proj in knowledge_base.get("projects", []):
        # Build project text
        proj_parts = [
            f"Project: {proj.get('name', '')}",
            f"Category: {proj.get('category', '')}",
            f"Tags: {', '.join(proj.get('tags', []))}",
            "",
            f"Description: {proj.get('description', '')}"
        ]
        
        if proj.get("problem_solved"):
            proj_parts.append(f"\nProblem Solved: {proj.get('problem_solved')}")
        
        if proj.get("key_features"):
            proj_parts.append("\nKey Features:")
            proj_parts.extend(f"- {f}" for f in proj.get("key_features", []))
        
        if proj.get("technical_details"):
            tech_details = proj.get("technical_details", {})
            if tech_details.get("architecture"):
                proj_parts.append("\nTechnical Architecture:")
                proj_parts.extend(f"- {a}" for a in tech_details.get("architecture", []))
        
        if proj.get("impact"):
            proj_parts.append("\nImpact & Results:")
            proj_parts.extend(f"- {i}" for i in proj.get("impact", []))
        
        if proj.get("technologies"):
            proj_parts.append(f"\nTechnologies: {', '.join(proj.get('technologies', []))}")
        
        if proj.get("sample_interactions"):
            proj_parts.append("\nSample Interactions:")
            proj_parts.extend(f'- "{s}"' for s in proj.get("sample_interactions", []))
        
        if proj.get("components"):
            proj_parts.append("\nComponents:")
            for comp in proj.get("components", []):
                proj_parts.append(f"- {comp.get('name', '')}: {comp.get('description', '')}")
        
        chunks.append({
            "id": proj.get("id", ""),
            "text": "\n".join(proj_parts).strip(),
            "metadata": {
                "type": "project",
                "category": proj.get("category", ""),
                "name": proj.get("name", ""),
                "tags": proj.get("tags", []),
                "technologies": proj.get("technologies", [])
            }
        })
    
    # Skills chunk (consolidated)
    skills = knowledge_base.get("skills", {})
    skills_parts = ["Technical Skills Overview:\n"]
    
    # GenAI & LLMs
    if skills.get("generative_ai_llms"):
        gen_ai = skills["generative_ai_llms"]
        skills_parts.append("Generative AI & LLMs:")
        skills_parts.append(f"  Models: {', '.join(gen_ai.get('models', []))}")
        skills_parts.append(f"  Frameworks: {', '.join(gen_ai.get('frameworks', []))}")
        skills_parts.append(f"  Techniques: {', '.join(gen_ai.get('techniques', []))}")
        skills_parts.append(f"  Optimization: {', '.join(gen_ai.get('optimization', []))}")
        skills_parts.append(f"  Vector DBs: {', '.join(gen_ai.get('vector_databases', []))}")
        skills_parts.append("")
    
    # Machine Learning
    if skills.get("machine_learning"):
        ml = skills["machine_learning"]
        skills_parts.append("Machine Learning:")
        skills_parts.append(f"  Frameworks: {', '.join(ml.get('frameworks', []))}")
        skills_parts.append(f"  Techniques: {', '.join(ml.get('techniques', []))}")
        skills_parts.append(f"  Specializations: {', '.join(ml.get('specializations', []))}")
        skills_parts.append("")
    
    # NLP
    if skills.get("nlp"):
        nlp = skills["nlp"]
        skills_parts.append("Natural Language Processing:")
        skills_parts.append(f"  Libraries: {', '.join(nlp.get('libraries', []))}")
        skills_parts.append(f"  Applications: {', '.join(nlp.get('applications', []))}")
        skills_parts.append("")
    
    # Cloud
    if skills.get("cloud_platforms"):
        cloud = skills["cloud_platforms"]
        skills_parts.append("Cloud Platforms:")
        if cloud.get("aws"):
            aws = cloud["aws"]
            skills_parts.append(f"  AWS Compute: {', '.join(aws.get('compute', []))}")
            skills_parts.append(f"  AWS AI/ML: {', '.join(aws.get('ai_ml', []))}")
        if cloud.get("gcp"):
            skills_parts.append(f"  GCP: {', '.join(cloud.get('gcp', []))}")
        if cloud.get("azure"):
            skills_parts.append(f"  Azure: {', '.join(cloud.get('azure', []))}")
        skills_parts.append("")
    
    # Programming
    if skills.get("programming_languages"):
        prog = skills["programming_languages"]
        skills_parts.append("Programming Languages:")
        skills_parts.append(f"  Expert: {', '.join(prog.get('expert', []))}")
        skills_parts.append(f"  Proficient: {', '.join(prog.get('proficient', []))}")
        skills_parts.append("")
    
    # Leadership
    if skills.get("leadership"):
        skills_parts.append("Leadership & Business Skills:")
        skills_parts.extend(f"  - {s}" for s in skills.get("leadership", []))
    
    chunks.append({
        "id": "skills",
        "text": "\n".join(skills_parts).strip(),
        "metadata": {"type": "skills", "category": "overview"}
    })
    
    # Education chunks
    for edu in knowledge_base.get("education", []):
        edu_text = f"""
Education: {edu.get('degree', '')}
Institution: {edu.get('institution', '')}
Duration: {edu.get('duration', '')}

Highlights:
{chr(10).join('- ' + h for h in edu.get('highlights', []))}
"""
        chunks.append({
            "id": edu.get("id", ""),
            "text": edu_text.strip(),
            "metadata": {"type": "education", "degree": edu.get("degree", "")}
        })
    
    # Certifications chunk
    certs = knowledge_base.get("certifications", [])
    if certs:
        cert_parts = ["Certifications:\n"]
        for cert in certs:
            cert_parts.append(f"- {cert.get('name', '')} ({cert.get('issuer', '')})")
            cert_parts.append(f"  {cert.get('description', '')}")
        chunks.append({
            "id": "certifications",
            "text": "\n".join(cert_parts).strip(),
            "metadata": {"type": "certifications", "category": "credentials"}
        })
    
    # Key achievements chunk
    achievements = knowledge_base.get("key_achievements", [])
    if achievements:
        ach_text = "Key Career Achievements:\n" + "\n".join(f"- {a}" for a in achievements)
        chunks.append({
            "id": "achievements",
            "text": ach_text,
            "metadata": {"type": "achievements", "category": "highlights"}
        })
    
    return chunks
