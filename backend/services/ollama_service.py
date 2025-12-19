import httpx
from config import settings
from typing import Optional

class OllamaService:
    def __init__(self):
        self.base_url = settings.OLLAMA_BASE_URL
        self.model = settings.OLLAMA_MODEL
    
    async def generate(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        """Generate text using Ollama API"""
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        
        try:
            # Connect timeout 3s, Read timeout 120s (for generation)
            async with httpx.AsyncClient(timeout=httpx.Timeout(120.0, connect=3.0)) as client:
                response = await client.post(
                    f"{self.base_url}/api/chat",
                    json={
                        "model": self.model,
                        "messages": messages,
                        "stream": False
                    }
                )
                response.raise_for_status()
                data = response.json()
                return data.get("message", {}).get("content", "")
        except Exception as e:
            # Fallback response if Ollama is not available
            print(f"Ollama Error: {e}")
            return "Unable to connect to AI"
    
    async def analyze_mood(self, mood_text: str) -> dict:
        """Analyze user's mood and generate encouragement"""
        system_prompt = """你是一个温暖体贴的情绪助理。用户会告诉你他们的心情。
请用以下JSON格式回复（只回复JSON，不要其他内容）：
{
    "encouragement": "鼓励和安慰的话语（100-150字）",
    "suggestion": "给用户的建议（50-80字）",
    "emoji": "一个最适合的表情符号",
    "mood_score": 情绪分数从-1到1的数字
}"""
        
        response = await self.generate(mood_text, system_prompt)
        try:
            import json
            # Try to parse JSON from response
            start = response.find("{")
            end = response.rfind("}") + 1
            if start != -1 and end > start:
                return json.loads(response[start:end])
        except:
            pass
        
        # Fallback Mock Response (looks real)
        return {
            "encouragement": "感受到你的心情了。无论此刻是阴雨还是晴天，请记住，所有的情绪都是生命流动的证明。给自己一个温暖的拥抱，你做得很棒了。",
            "suggestion": "也许可以尝试深呼吸三次，或者听一首舒缓的音乐，让自己慢慢放松下来。",
            "emoji": "🌿",
            "mood_score": 0.5
        }
    
    async def analyze_love_chat(self, chat_content: str) -> dict:
        """Analyze chat and suggest better replies"""
        system_prompt = """你是一个专业的恋爱教练。用户会发送他们的聊天记录。
请分析对话并用以下JSON格式回复（只回复JSON）：
{
    "analysis": "对当前对话状态的分析（80-120字）",
    "suggestions": ["建议回复1", "建议回复2", "建议回复3"],
    "tips": "提高好感度的技巧（50-80字）",
    "affection_score": 当前好感度预估0-100
}"""
        
        response = await self.generate(chat_content, system_prompt)
        try:
            import json
            start = response.find("{")
            end = response.rfind("}") + 1
            if start != -1 and end > start:
                return json.loads(response[start:end])
        except:
            pass
        
        return {
            "analysis": response,
            "suggestions": ["今天怎么样？", "想你了~", "有空一起吃饭吗？"],
            "tips": "保持真诚，展现关心。",
            "affection_score": 50
        }
    
    async def reflect_diary(self, diary_content: str) -> dict:
        """Generate self-reflection analysis"""
        system_prompt = """你是一个温柔的心理顾问，帮助用户进行自我反省。
用户会分享今天的一句话或想法。
请用以下JSON格式回复（只回复JSON）：
{
    "reflection": "深入的反思分析（100-150字）",
    "growth_insight": "成长洞察（80-100字）",
    "tomorrow_suggestion": "明天可以尝试的一件事",
    "growth_score": 自我成长评分0-100
}"""
        
        response = await self.generate(diary_content, system_prompt)
        try:
            import json
            start = response.find("{")
            end = response.rfind("}") + 1
            if start != -1 and end > start:
                return json.loads(response[start:end])
        except:
            pass
        
        return {
            "reflection": response,
            "growth_insight": "每一天都是成长的机会。",
            "tomorrow_suggestion": "尝试做一件让自己开心的事。",
            "growth_score": 70
        }
    
    async def interpret_tarot(self, cards: list, question: str = "") -> str:
        """Interpret tarot cards with AI"""
        system_prompt = """你是一个神秘而温暖的塔罗牌占卜师。
请根据抽到的牌为用户进行解读，语气要神秘但充满希望和安慰。
解读要具体，结合用户的问题（如果有），给出实际的建议。
回复长度200-300字。"""
        
        prompt = f"用户的问题：{question if question else '请为我占卜'}\n抽到的牌：{', '.join(cards)}"
        return await self.generate(prompt, system_prompt)
    
    async def voice_companion(self, user_message: str) -> str:
        """Voice companion chat response"""
        system_prompt = """你是一个温暖的语音陪伴助理，名叫小塔。
用户可能感到孤独，需要有人陪伴聊天。
请用温暖、关心的语气回复，像一个贴心的朋友。
回复要简短自然（50-100字），适合语音朗读。"""
        
        return await self.generate(user_message, system_prompt)


ollama_service = OllamaService()
