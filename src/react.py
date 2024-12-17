import sys, os
sys.path.append('..')
root  = '../root/'

from agents import ReactAgent
import globals

strategy: ReflexionStrategy = ReflexionStrategy.NONE
agent_cls = ReactAgent

import json

datas = json.load(open('../data/dataset.json', 'r'))

import argparse

parser = argparse.ArgumentParser(description="Process some integers.")
parser.add_argument('--model', type=str, required=True, help='实验基座模型')
parser.add_argument('--date', type=str, required=True, help='实验日期，用于区别输出路径，如output_date')
args = parser.parse_args()
model_name = args.model
date = args.date

os.makedirs(f"./output_{date}", exist_ok=True)

output = open(f'./output_{date}/react_{date}_{model_name}.json', 'a') 

log_txt = open(f'./output_{date}/log_react_{date}_{model_name}.txt', 'a')

os.makedirs(f"./token_{date}", exist_ok=True)
globals.token_txt = open(f"./token_{date}/react_{date}_{model_name}.json", 'a') # 定义存储路径
globals.total_token = 0                                                         # 本次实验消耗的token

from utils import *
import traceback

n = 5
trial = 0


for idx, data in enumerate(datas[0:300]):
    try:
        globals.this_question_total_token = 0
        globals.this_question_input_token = 0
        globals.this_question_output_token = 0

        query = data['question']
        print(query)
        log_txt.write(query + '\n')

        used_tools, table_used_prompt = filter_table_and_tool(query, model_name)

        # 求和工具
        used_tools.append(get_sum_tool)
        used_tools.append(get_rank_tool)
        # 检索工具
        used_tools.append(legal_article_retriever_tool)
        used_tools.append(legal_case_retriever_tool)
        used_tools.append(legal_knowledge_retriever_tool)

        tools = "\n\n".join([f"{tool.name}: {tool.description}" for tool in used_tools])
        tool_names = " ".join([f"{tool.name}" for tool in used_tools])

        print(tools)

        react_agent = agent_cls(model_name=model_name, question=query, tools=tools, tool_names=tool_names, table_used_prompt=table_used_prompt)
        react_agent.run()

        final_answer = LLM(FILTER_PROMPT.format(query=query, info=react_agent.scratchpad), model_name)

        summary_anwer = LLM(SUMMARY_PROMPT.format(query=query, info=react_agent.scratchpad), model_name)
        
        final_answer = re.sub(r'(?<=\d),(?=\d)', '', final_answer)
        summary_anwer = re.sub(r'(?<=\d),(?=\d)', '', summary_anwer)
        
        print(f"final_anwer is {final_answer}")
        print(f"summary_answer is {summary_anwer}")

        output.write(json.dumps({
            "id": data['id'],
            "res": final_answer,
            "summary": summary_anwer
        }, ensure_ascii=False) + '\n')
        output.flush()

        globals.token_txt.write(json.dumps({
            "id": data['id'],
            "input_token": globals.this_question_input_token,
            "output_token": globals.this_question_output_token,
            "total_token": globals.this_question_total_token,
            "current_total_token":  globals.total_token
        }, ensure_ascii=False) + '\n')
        globals.token_txt.flush()

        log_txt.write(react_agent.scratchpad)
        log_txt.write('\n')
        log_txt.write(f"final_anwer is {final_answer}")
        log_txt.write('\n')
        log_txt.write(f"summary_answer is {summary_anwer}")
        log_txt.write('\n\n\n')
        log_txt.flush()
    except Exception as e:
        # log_txt.write(f"something wrong here: {traceback.print_exception(type(e), e, e.__traceback__)}")
        traceback.print_exc(file=log_txt)
        log_txt.flush()
        output.write(json.dumps({
            "id": data['id'],
            "res": "silence",
            "summary": "silence"
        }, ensure_ascii=False) + '\n')
        output.flush()
        globals.token_txt.write(json.dumps({
            "id": data['id'],
            "input_token": globals.this_question_input_token,
            "output_token": globals.this_question_output_token,
            "total_token": globals.this_question_total_token,
            "current_total_token":  globals.total_token
        }, ensure_ascii=False) + '\n')
        globals.token_txt.flush()
