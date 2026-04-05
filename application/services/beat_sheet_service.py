"""节拍表生成服务

为章节大纲生成场景列表（Beat Sheet）
"""

import uuid
import json
import logging
from typing import Dict, List, Optional
from datetime import datetime

from domain.novel.entities.beat_sheet import BeatSheet
from domain.novel.value_objects.scene import Scene
from domain.novel.repositories.beat_sheet_repository import BeatSheetRepository
from domain.novel.repositories.chapter_repository import ChapterRepository
from domain.novel.repositories.storyline_repository import StorylineRepository
from domain.ai.services.llm_service import LLMService, GenerationConfig
from domain.ai.value_objects.prompt import Prompt
from infrastructure.ai.chromadb_vector_store import ChromaDBVectorStore

logger = logging.getLogger(__name__)


class BeatSheetService:
    """节拍表生成服务

    为章节大纲生成 3-5 个场景，采用混合检索策略：
    1. 强制包含（Must-Have）：主要人物、活跃故事线、前置章节状态
    2. 向量检索（Nice-to-Have）：相关伏笔、地点、时间线
    """

    def __init__(
        self,
        beat_sheet_repo: BeatSheetRepository,
        chapter_repo: ChapterRepository,
        storyline_repo: StorylineRepository,
        llm_service: LLMService,
        vector_store: ChromaDBVectorStore,
        bible_service=None,
    ):
        self.beat_sheet_repo = beat_sheet_repo
        self.chapter_repo = chapter_repo
        self.storyline_repo = storyline_repo
        self.llm_service = llm_service
        self.vector_store = vector_store
        self.bible_service = bible_service

    async def generate_beat_sheet(
        self,
        chapter_id: str,
        outline: str
    ) -> BeatSheet:
        """为章节生成节拍表

        Args:
            chapter_id: 章节 ID
            outline: 章节大纲

        Returns:
            生成的节拍表
        """
        logger.info(f"Generating beat sheet for chapter {chapter_id}")

        # 1. 混合检索：获取相关上下文
        context = await self._retrieve_relevant_context(chapter_id, outline)

        # 2. 构建提示词
        prompt = self._build_beat_sheet_prompt(outline, context)

        # 3. 调用 LLM 生成节拍表
        config = GenerationConfig(max_tokens=2048, temperature=0.7)
        response = await self.llm_service.generate(prompt, config)

        # 4. 解析响应
        scenes = self._parse_llm_response(response)

        # 5. 创建节拍表实体
        beat_sheet = BeatSheet(
            id=str(uuid.uuid4()),
            chapter_id=chapter_id,
            scenes=scenes
        )

        # 6. 保存到仓储
        await self.beat_sheet_repo.save(beat_sheet)

        logger.info(f"Beat sheet generated with {len(scenes)} scenes")
        return beat_sheet

    async def _retrieve_relevant_context(
        self,
        chapter_id: str,
        outline: str
    ) -> Dict:
        """混合检索策略：强制包含 + 向量检索

        Phase 1.1 简化版：只实现基础功能
        """
        context = {}

        # === 第一层：强制包含（Must-Have） ===
        # TODO: 实现获取主要人物和活跃故事线
        # 当前简化版：暂时跳过

        # === 第二层：向量检索（Nice-to-Have） ===
        # TODO: 实现向量检索（需要先将 outline 转换为向量）
        # 当前简化版：暂时跳过向量检索
        context["foreshadowings"] = []

        return context

    def _build_beat_sheet_prompt(
        self,
        outline: str,
        context: Dict
    ) -> Prompt:
        """构建节拍表生成提示词"""

        system_prompt = """你是一位专业的小说编剧，擅长将章节大纲拆解为具体的场景（Scene）。

你的任务是将章节大纲拆解为 3-5 个场景，每个场景应该：
1. 有明确的场景目标（Scene Goal）
2. 指定 POV 角色（从哪个角色的视角叙述）
3. 指定地点（可选）
4. 指定情绪基调（例如：紧张、温馨、悲伤、激烈）
5. 预估字数（每个场景 500-1000 字）

请以 JSON 格式返回场景列表，格式如下：
{
  "scenes": [
    {
      "title": "场景标题",
      "goal": "这个场景要达成什么目标",
      "pov_character": "POV 角色名称",
      "location": "地点（可选）",
      "tone": "情绪基调",
      "estimated_words": 800
    }
  ]
}

注意事项：
- 场景之间要有逻辑连贯性
- 每个场景聚焦一个明确目标，避免贪多
- POV 角色应该是章节中的主要角色
- 预估字数总和应该在 2000-4000 字之间
"""

        # 构建用户提示词
        user_prompt = f"""章节大纲：
{outline}

"""

        # 添加相关伏笔（如果有）
        if context.get("foreshadowings"):
            user_prompt += "\n相关伏笔（可以在场景中呼应）：\n"
            for foreshadowing in context["foreshadowings"][:5]:  # 最多显示 5 条
                user_prompt += f"- {foreshadowing.get('description', 'N/A')}\n"

        user_prompt += "\n请生成场景列表（JSON 格式）："

        return Prompt(
            system=system_prompt,
            user=user_prompt
        )

    def _parse_llm_response(self, response) -> List[Scene]:
        """解析 LLM 响应，提取场景列表"""
        try:
            # 提取响应文本（处理 GenerationResult 对象）
            if hasattr(response, 'content'):
                response_text = response.content
            elif hasattr(response, 'text'):
                response_text = response.text
            else:
                response_text = str(response)

            # 尝试提取 JSON（可能被包裹在 markdown 代码块中）
            response_text = response_text.strip()
            if response_text.startswith("```json"):
                response_text = response_text[7:]
            if response_text.startswith("```"):
                response_text = response_text[3:]
            if response_text.endswith("```"):
                response_text = response_text[:-3]
            response_text = response_text.strip()

            data = json.loads(response_text)
            scenes_data = data.get("scenes", [])

            scenes = []
            for i, scene_data in enumerate(scenes_data):
                scene = Scene(
                    title=scene_data.get("title", f"场景 {i+1}"),
                    goal=scene_data.get("goal", ""),
                    pov_character=scene_data.get("pov_character", "未知"),
                    location=scene_data.get("location"),
                    tone=scene_data.get("tone"),
                    estimated_words=scene_data.get("estimated_words", 800),
                    order_index=i
                )
                scenes.append(scene)

            if not scenes:
                raise ValueError("No scenes generated")

            return scenes

        except Exception as e:
            logger.error(f"Failed to parse LLM response: {e}")
            logger.error(f"Response: {response_text if 'response_text' in locals() else response}")
            raise ValueError(f"Failed to parse beat sheet response: {e}")

    async def get_beat_sheet(self, chapter_id: str) -> Optional[BeatSheet]:
        """获取章节的节拍表"""
        return await self.beat_sheet_repo.get_by_chapter_id(chapter_id)

    async def delete_beat_sheet(self, chapter_id: str) -> None:
        """删除章节的节拍表"""
        await self.beat_sheet_repo.delete_by_chapter_id(chapter_id)
