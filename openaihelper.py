import openai
class OpenAiHelper:
    def __init__(self):
        self.ai = openai
        self.ai.api_key = ""
        
        
    def makeRandomAffirmation(self):   
        completion = self.ai.chat.completions.create(model="gpt-3.5-turbo", messages=[
            {
                "role": "system",
                "content": "You are a helpful API assistant providing affirmations for users with depressive mindsets."
            },
            {
                "role": "user",
                "content": "Generate one affirmation."
            }

            ])
        return completion.choices[0].message.content
    
    def makeGuidedAffirmation(self,problem):   
        completion = self.ai.chat.completions.create(model="gpt-3.5-turbo", messages=[
            {
                "role": "system",
                "content": "You are a helpful API assistant providing affirmations for users with depressive mindsets."
            },
            {
                "role": "user",
                "content": "Generate one affirmation to help me with " +problem + "."
            }

            ])
        return completion.choices[0].message.content
    
    