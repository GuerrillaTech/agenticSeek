
from sources.utility import pretty_print
from sources.agent import Agent
from sources.tools.webSearch import webSearch
class CasualAgent(Agent):
    def __init__(self, model, name, prompt_path, provider):
        """
        The casual agent is a special for casual talk to the user without specific tasks.
        """
        super().__init__(model, name, prompt_path, provider)
        self.tools = {
            "web_search": webSearch()
        }
        self.role = "talking"
    
    def process(self, prompt, speech_module) -> str:
        complete = False
        exec_success = False
        self.memory.push('user', prompt)

        self.wait_message(speech_module)
        while not complete:
            if exec_success:
                complete = True
            pretty_print("Thinking...", color="status")
            answer, reasoning = self.llm_request()
            exec_success, _ = self.execute_modules(answer)
            answer = self.remove_blocks(answer)
            self.last_answer = answer
        return answer, reasoning

if __name__ == "__main__":
    from llm_provider import Provider

    #local_provider = Provider("ollama", "deepseek-r1:14b", None)
    server_provider = Provider("server", "deepseek-r1:14b", "192.168.1.100:5000")
    agent = CasualAgent("deepseek-r1:14b", "jarvis", "prompts/casual_agent.txt", server_provider)
    ans = agent.process("Hello, how are you?")
    print(ans)