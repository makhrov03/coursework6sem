import re


def find_called_functions(llvm_ir):
    called_functions = set(re.findall(r'call\s+\w+\s+@"(\w+)"', llvm_ir))
    return called_functions


def optimize_unused_functions(llvm_ir):
    called_functions = find_called_functions(llvm_ir)

    lines = llvm_ir.splitlines()

    in_function = False

    current_function = ""

    optimized_lines = []

    for line in lines:
        match = re.match(r'define\s+\w+\s+@"(\w+)"\(', line)
        if match:
            current_function = match.group(1)
            in_function = True

        if in_function and current_function != "main" and current_function not in called_functions:
            if line.strip() == "}":
                in_function = False
            continue

        optimized_lines.append(line)

    return "\n".join(optimized_lines)


def optimize_variable_assignments(llvm_ir):
    lines = llvm_ir.splitlines()

    last_assignment = {}

    optimized_lines = []

    for line in lines:

        store_match = re.match(r'\s*store\s+i32\s+(\d+),\s+i32\*\s+(%".\d+")', line)
        if store_match:
            value = store_match.group(1)
            var_name = store_match.group(2)

            last_assignment[var_name] = line
        else:

            load_match = re.match(r'\s*%".\d+"\s*=\s*load\s+i32,\s+i32\*\s+(%".\d+")', line)
            if load_match:
                var_name = load_match.group(1)

                if var_name in last_assignment:
                    optimized_lines.append(last_assignment.pop(var_name))

            optimized_lines.append(line)

    return "\n".join(optimized_lines)


with open('code.ll', 'r') as file:
    llvm_ir = file.read()

llvm_ir = optimize_unused_functions(llvm_ir)
llvm_ir = optimize_variable_assignments(llvm_ir)

with open('optimized_code.ll', 'w') as file:
    file.write(llvm_ir)

print("created optimized_code.ll")
