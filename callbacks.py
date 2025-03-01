from langchain.callbacks.base import BaseCallbackHandler

class IntermediateStepHandler(BaseCallbackHandler):
    def __init__(self):
        self.steps = []
        self.current_step = {}
    
    def on_agent_action(self, action, **kwargs):
        self.current_step["action"] = action.log
        self.steps.append(f"🔧 **Action**: `{action.tool}`\n```\n{action.log}\n```")
    
    def on_tool_end(self, output, **kwargs):
        self.steps.append(f" **Observation**:\n```\n{output}\n```")
        self.current_step = {}