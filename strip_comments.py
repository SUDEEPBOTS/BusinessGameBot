import os
import tokenize
import io

def remove_comments(source_code):
    io_obj = io.StringIO(source_code)
    out = ""
    last_lineno = -1
    last_col = 0
    
    try:
        for tok in tokenize.generate_tokens(io_obj.readline):
            token_type = tok[0]
            token_string = tok[1]
            start_line, start_col = tok[2]
            end_line, end_col = tok[3]
            
            if start_line > last_lineno:
                last_col = 0
                
            if start_col > last_col:
                out += " " * (start_col - last_col)
                
            if token_type == tokenize.COMMENT:
                pass # skip comment
            else:
                out += token_string
                
            last_lineno = end_line
            last_col = end_col
    except tokenize.TokenError:
        return source_code # fallback if parsing fails
        
    # Clean up empty lines that were left behind by comment removal
    cleaned_lines = []
    for line in out.splitlines():
        if line.strip() == "" and len(line) > 0:
            pass # skip lines that became entirely whitespace
        else:
            cleaned_lines.append(line)
            
    return "\n".join(cleaned_lines)

def process_dir(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".py"):
                filepath = os.path.join(root, file)
                with open(filepath, "r", encoding="utf-8") as f:
                    content = f.read()
                
                new_content = remove_comments(content)
                
                # Further cleanup: remove lines that are just whitespace
                final_content = "\n".join([line for line in new_content.splitlines() if line.strip() or not line])
                
                if new_content != content:
                    with open(filepath, "w", encoding="utf-8") as f:
                        f.write(final_content)
                        print(f"Stripped comments from: {filepath}")

process_dir("/home/ubuntu/BUSINESS_BOT/BUSINESS")
