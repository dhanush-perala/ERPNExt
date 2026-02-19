import os

def resolve_conflicts(directory):
    for root, dirs, files in os.walk(directory):
        if any(d in root for d in ['.git', 'node_modules', 'env', 'sites']):
            continue
        for file in files:
            path = os.path.join(root, file)
            try:
                # Only process text files that likely have conflicts
                if not any(file.endswith(ext) for ext in ['.py', '.js', '.json', '.html', '.css', '.md']):
                    continue
                    
                with open(path, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                
                if not any("<<<<<<<" in line for line in lines):
                    continue
                    
                print(f"Resolving conflicts in {path}")
                new_lines = []
                state = "KEEP" # KEEP, HEAD, OTHER
                
                for line in lines:
                    sline = line.strip()
                    if sline.startswith("<<<<<<<"):
                        state = "HEAD"
                    elif sline.startswith("======="):
                        state = "OTHER"
                    elif sline.startswith(">>>>>>>"):
                        state = "KEEP"
                    else:
                        if state == "KEEP" or state == "HEAD":
                            new_lines.append(line)
                            
                with open(path, 'w', encoding='utf-8') as f:
                    f.writelines(new_lines)
            except Exception as e:
                print(f"Error processing {path}: {e}")

if __name__ == "__main__":
    resolve_conflicts('/home/neemus/frappe-bench-new/apps/erpnext')
