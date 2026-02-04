# agents/orchestrator/AgentOrchestrator.py
from typing import List, Dict, Optional
import yaml
import ollama
from pathlib import Path

class AgentOrchestrator:
    """
    Multi-agent orchestration framework.

    Flow:
    1. User query → Select agent (based on triggers)
    2. Load agent's skills (only what it needs)
    3. Agent executes with small, focused context
    """

    def __init__(self, config_path: str, skills_dir: str):
        """
        Initialize the orchestrator.

        Args:
            config_path: Path to agents.yaml
            skills_dir: Path to skills directory
        """
        self.agents = self._load_agent_config(config_path)
        self.skills_dir = Path(skills_dir)
        self.tools = {}  # Registry for Python tools (like ObsidianTool)

    def _load_agent_config(self, config_path: str) -> Dict:
        """Load agent definitions from agents.yaml"""
        with open(config_path) as f:
            return yaml.safe_load(f)['agents']

    def register_tool(self, name: str, tool_instance):
        """
        Register a Python tool (like ObsidianTool).
        Tools handle complex workflows that agents can't do alone.
        """
        self.tools[name] = tool_instance
        print(f"Registered tool: {name}")

    def load_skill(self, skill_name: str) -> Optional[Dict]:
        """
        Load a single skill by name.
        Reads the SKILL.md file and extracts metadata + content.
        """
        # Skills are stored directly in skills_dir/skill-name/SKILL.md
        skill_path = self.skills_dir / skill_name / "SKILL.md"

        if not skill_path.exists():
            print(f"Warning: Skill '{skill_name}' not found at {skill_path}")
            return None

        with open(skill_path, 'r') as f:
            content = f.read()
            metadata = self._parse_skill_metadata(content)
            return {
                'name': skill_name,
                'content': content,
                'metadata': metadata
            }

    def _parse_skill_metadata(self, content: str) -> Dict:
        """Extract YAML frontmatter from SKILL.md"""
        import re
        match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
        if match:
            return yaml.safe_load(match.group(1))
        return {}

    def select_agent(self, query: str) -> str:
        """
        Choose which agent should handle this query.

        Strategy:
        1. Check if query matches any agent triggers (from agents.yaml)
        2. Check if query matches any skill triggers (from SKILL.md files)
        3. Default to general_agent if no match

        Returns: agent name
        """
        query_lower = query.lower()

        # Strategy 1: Check agent triggers first
        for agent_name, agent_config in self.agents.items():
            triggers = agent_config.get('triggers', [])
            if any(trigger.lower() in query_lower for trigger in triggers):
                print(f"Selected agent '{agent_name}' based on agent trigger")
                return agent_name

        # Strategy 2: Check skill triggers
        # Scan all skills to see if their triggers match
        for skill_dir in self.skills_dir.iterdir():
            if skill_dir.is_dir():
                skill = self.load_skill(skill_dir.name)
                if skill:
                    triggers = skill['metadata'].get('triggers', [])
                    if any(trigger.lower() in query_lower for trigger in triggers):
                        # This skill is relevant - check if it requires a tool
                        if skill['metadata'].get('requires_tool'):
                            print(f"Selected workflow '{skill['name']}' (requires tool)")
                            return f"workflow:{skill['name']}"

                        # Find which agent has this skill
                        for agent_name, agent_config in self.agents.items():
                            if skill['name'] in agent_config.get('skills', []):
                                print(f"Selected agent '{agent_name}' based on skill trigger")
                                return agent_name

        # Default: use general_agent
        print("No specific agent matched, using general_agent")
        return 'general_agent'

    def load_agent_skills(self, agent_name: str) -> List[Dict]:
        """
        Load all skills assigned to this agent (from agents.yaml).
        This keeps the agent's context small and focused.
        """
        agent_config = self.agents.get(agent_name, {})
        skill_names = agent_config.get('skills', [])

        skills = []
        for skill_name in skill_names:
            skill = self.load_skill(skill_name)
            if skill:
                skills.append(skill)

        return skills

    def invoke_agent(self, agent_name: str, query: str,
                     skills: List[Dict] = None,
                     context: Optional[str] = None) -> str:
        """
        Call a specific agent to process the query.

        Args:
            agent_name: Which agent to use (doc_agent, research_agent, etc.)
            query: User's question/request
            skills: Optional list of skills to load (if None, loads agent's default skills)
            context: Optional context from previous agent responses
        """
        agent_config = self.agents[agent_name]

        # If skills not provided, load the agent's default skills
        if skills is None:
            skills = self.load_agent_skills(agent_name)

        # Build system prompt: agent's personality + skills
        system_prompt = agent_config.get('system_prompt', '')

        if skills:
            system_prompt += "\n\n# Your Available Skills:\n"
            for skill in skills:
                system_prompt += f"\n{skill['content']}\n"

        # Build message chain
        messages = [{'role': 'system', 'content': system_prompt}]

        if context:
            messages.append({'role': 'user', 'content': f"Context:\n{context}"})

        messages.append({'role': 'user', 'content': query})

        # Call the LLM
        response = ollama.chat(
            model=agent_config['model'],
            messages=messages
        )

        return response['message']['content']

    def execute_tool(self, tool_name: str, **kwargs) -> str:
        """Execute a registered Python tool"""
        if tool_name not in self.tools:
            return f"Error: Tool '{tool_name}' not found"

        tool = self.tools[tool_name]
        return tool.execute(**kwargs)

    def orchestrate(self, user_query: str) -> str:
        """
        Main entry point: route a user query to the right agent or tool.

        Flow:
        1. Select appropriate agent/workflow
        2. If it's a tool workflow, execute the tool
        3. Otherwise, invoke the agent with its skills
        """
        # Step 1: Decide which agent or workflow should handle this
        selection = self.select_agent(user_query)

        # Step 2: If it's a workflow (requires a tool), execute the tool
        if selection.startswith('workflow:'):
            skill_name = selection.split(':', 1)[1]
            skill = self.load_skill(skill_name)
            tool_name = skill['metadata'].get('requires_tool')

            if tool_name and tool_name in self.tools:
                # The tool will orchestrate everything (like ObsidianTool does)
                # Load all skills that might be needed by the tool's agents
                all_skills = [skill]

                # For obsidian-integration, also load skills for doc_agent and research_agent
                if skill_name == 'obsidian-integration':
                    # Load skills for doc_agent
                    for skill_name in ['daily-summary', 'markdown-processing']:
                        s = self.load_skill(skill_name)
                        if s:
                            all_skills.append(s)

                    # Load skills for research_agent
                    for skill_name in ['open-research', 'web-search']:
                        s = self.load_skill(skill_name)
                        if s:
                            all_skills.append(s)

                print(f"Loading {len(all_skills)} skills for tool: {[s['name'] for s in all_skills]}")
                return self.execute_tool(tool_name, query=user_query, skills=all_skills)
            else:
                return f"Error: Workflow '{skill_name}' requires tool '{tool_name}' which is not registered"

        # Step 3: Otherwise, invoke the selected agent
        # The agent will automatically load its skills from agents.yaml
        return self.invoke_agent(selection, user_query)