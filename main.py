from openai import OpenAI
from prompt import SYSTEM_PROMPT, tools
import json
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()


openai_client = OpenAI()


def main():
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    while True:
        query = input(">_")
        messages.append({"role": "user", "content": query})

        while True:
            response = openai_client.chat.completions.create(
                model="gpt-4.1",
                messages=messages,
                response_format={"type": "json_object"},
            )
            messages.append(
                {"role": "assistant", "content": response.choices[0].message.content}
            )
            resp_dict = json.loads(response.choices[0].message.content)
            print(resp_dict["type"])
            print(resp_dict["result"], "\n")

            if resp_dict["type"] == "tool_call":
                res = tools[resp_dict["result"]]()
                print(res)
                messages.append(
                    {
                        "role": "assistant",
                        "content": json.dumps(
                            {"type": "tool_call_result", "result": res}
                        ),
                    }
                )

            if resp_dict["type"] == "result":
                break


if __name__ == "__main__":
    main()
