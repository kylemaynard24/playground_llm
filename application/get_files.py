## root is one level up ..

import os
import subprocess

def good_file_name(word):
    bad_file_names = [".git", ".avif", "template", "describe", "prompt", "get_files"]
    res = all(fn not in word for fn in bad_file_names)
    # print(res)
    return res

def get_files_in_parent_subdirs():
    files = []
    current_dir = os.getcwd()    
    parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
    app_files = []

    for item in os.listdir(parent_dir):
        item_path = os.path.join(parent_dir, item)
        if os.path.isdir(item_path) and good_file_name(item_path):
            for root, dirs, files in os.walk(item_path):
                for file in files:                    
                    full_path = os.path.join(root, file)
                    app_files.append(full_path)
    return app_files

def organize_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    return {"File Name": file_path.replace("/", "_").replace(".",""), "Content": content}

def create_prompt(file_content, template="./prompts/template_prompt.txt"):
    # write a templated prompt in which you replace the <File_Name> and <CONTENT>
    content = ""
    with open(template, 'r', encoding='utf-8') as file:
        content = file.read()
        content = content.replace("<FILE_NAME>", file_content["File Name"])
        content = content.replace("<CONTENT>", file_content["Content"])
    with open("./templated_prompts/template_for_" + file_content["File Name"] + ".txt", "w", encoding="utf-8") as file:
        file.write(content)

def get_codellama_results():
    # make sure that codellama is pulled for bash
    # /Users/kylemaynard/git_playground/application/templated_prompts
    # read in the prompt
    # subprocess.run(["ollama", "pull", "codellama"])
    prompts_path = "/Users/kylemaynard/git_playground/application/templated_prompts/"
    code_llama_response = ""
    for item in os.listdir(prompts_path):
        print(item)
        item_path = os.path.join(prompts_path, item)
        with open(item_path, 'r', encoding='utf-8') as file:
            content = file.read()
            # run the codellama cli command, example: ollama codellama describe_script.txt 
            print(content)
            codellama_cmd = subprocess.run(["ollama", "run", "codellama", item_path], capture_output=True, text=True)
            code_llama_response = codellama_cmd.stdout
        with open("./prompt_result_files/" + item.replace(".txt", "") + ".txt", "w", encoding="utf-8") as file:
            file.write(code_llama_response)

if __name__ == "__main__":
    files = get_files_in_parent_subdirs()
    for file in files:
        if(good_file_name(file)):
            create_prompt(organize_file(file))
    get_codellama_results()