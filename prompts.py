from langchain.prompts import PromptTemplate

REACT_INSTRUCTION = """解决一个问答任务, 步骤包括交替进行的"思考", "行动"和"观察".
- "思考"用于基于现在的情况推理下一步, 注意你只需要思考下一步.
- "行动"是指通过一个 json 块指定要使用的工具, 包含一个 action 键(工具名称)和一个 action_input 键(工具输入).
有效的 "action" 值包括: "Final Answer" 或 {tool_names}.
你可以使用以下工具:
{tools}
其中相关的数据表格及其包含的字段包括(只要在表格中出现的字段可以作为columns参数中的值!):
{table_used_prompt}
- "行动"一次只能调用一次工具, 若要多次调用工具, 请拆分成多步分别调用.
- "行动"一定要按照以下json格式输出, 可以被Python json.loads函数解析:
```json
{{
    "action": $TOOL_NAME,
    "action_input": $INPUT
}}
```

以下是一些示例:
{examples}
(示例结束)

注意:当你在输出"行动"时, 结果一定要按照以下json格式输出, 可以被Python json.loads函数解析:
```json
{{
    "action": $TOOL_NAME,
    "action_input": $INPUT
}}
```
当你在输出"思考"时, 每次只思考下一步, 不要多思考!

问题: {question}
{scratchpad}
"""

PS_INSTRUCTION_PLAN = """解决一个问答任务, 请你理解问题并制定解决问题的逐步计划.
请以标题"计划:"开头输出计划, 并接着提供一个步骤列表, 每个步骤以"第n步:"开头, 其中n为当前步骤的编号(1, 2, 3,...).
该计划应包含若干单独的步骤, 逐步完成这些步骤将得出正确答案.
请确保计划足以准确完成任务, 不要跳过任何步骤,也不要添加任何多余的步骤.
最后一步总是"根据上述步骤, 请回答用户的原始问题".
在计划的末尾, 请写上"计划结束".

你可以使用以下工具:
{tools}
其中相关的数据表格及其包含的字段包括(只要在表格中出现的字段可以作为columns参数中的值!):
{table_used_prompt}

注意, 你只需负责制定计划并按照要求输出计划, 请不要实际执行计划!!!

以下是一些示例:
{examples}
(示例结束)

问题: {question}
"""

PS_INSTRUCTION_SOLVE = """给定单步计划, 请你按照计划的内容输出你具体要执行的行动, "行动"是通过一个 json 块指定要使用的工具, 包含一个 action 键(工具名称)和一个 action_input 键(工具输入).
有效的 "action" 值包括: "Final Answer" 或 {tool_names}.
你可以使用以下工具:
{tools}
其中相关的数据表格及其包含的字段包括(只要在表格中出现的字段可以作为columns参数中的值!):
{table_used_prompt}
- "行动"一次只能调用一次工具, 若要多次调用工具, 请拆分成多步分别调用.
- "行动"一定要按照以下json格式输出, 可以被Python json.loads函数解析:
```json
{{
    "action": $TOOL_NAME,
    "action_input": $INPUT
}}
```

以下是一些示例:
{examples}
(示例结束)

你需要执行的单步计划: {plan}
你目前已完成的步骤是: {scratchpad}
行动:
"""

PE_INSTRUCTION_REPLAN = """解决一个问答任务, 请你理解问题并制定解决问题的逐步计划.
请以标题"计划:"开头输出计划, 并接着提供一个步骤列表, 每个步骤以"第n步:"开头, 其中n为当前步骤的编号(1, 2, 3,...).
该计划应包含若干单独的步骤, 逐步完成这些步骤将得出正确答案.
请确保计划足以准确完成任务, 不要跳过任何步骤, 也不要添加任何多余的步骤.
最后一步总是"根据上述步骤, 请回答用户的原始问题".
在计划的末尾, 请写上"计划结束".

你可以使用以下工具:
{tools}
其中相关的数据表格及其包含的字段包括(只要在表格中出现的字段可以作为columns参数中的值!):
{table_used_prompt}

注意, 你只需负责制定计划并按照要求输出计划, 请不要实际执行计划!!!

以下是一些示例:
{examples}
(示例结束)

问题: {question}
你的原始计划是: {plan}
你目前已完成的步骤是: {scratchpad}
请根据情况更新计划.如果你觉得需要更多的步骤, 请严格按照格式要求列出仍然需要完成的计划步骤.对于已经完成的步骤请原样保留, 同时不要重复添加已经完成的步骤.
每个步骤以"第n步"开头, 其中n为当前步骤的编号(1, 2, 3,...).
最后一步总是"根据上述步骤, 请回答用户的原始问题".
在计划的末尾, 请写上"计划结束".
"""

react_agent_prompt = PromptTemplate(
                        input_variables=["table_used_prompt", "tools", "tool_names", "examples", "question", "scratchpad"],
                        template = REACT_INSTRUCTION,                              # React的 prompt
                        )

ps_plan_prompt = PromptTemplate(
                        input_variables=["table_used_prompt", "tools", "examples", "question"],
                        template = PS_INSTRUCTION_PLAN,                              # ps的 prompt
                        )

ps_solve_prompt = PromptTemplate(
                        input_variables=["tool_names", "table_used_prompt", "tools", "examples", "plan", 'scratchpad'],
                        template = PS_INSTRUCTION_SOLVE,                              # ps的 prompt
                        )

pe_replan_prompt = PromptTemplate(
                        input_variables=["table_used_prompt", "tools", "examples", "plan", 'scratchpad', 'question'],
                        template = PE_INSTRUCTION_REPLAN,                              # ps的 prompt
                        )
