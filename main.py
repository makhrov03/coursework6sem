from Lexer import Lexer
from Parser import Parser
from CodeGen import Compiler
from AST import Program

import json
import time


import llvmlite.binding as llvm
from ctypes import CFUNCTYPE, c_int, c_float


def lexer_debug():
    lexer = Lexer(code=code)
    while lexer.current_ch is not None:
        print(lexer.next_token())


def parser_debug():
    lexer = Lexer(code=code)
    parser = Parser(lexer=lexer)
    program: Program = parser.parse_program()
    if len(parser.errors) > 0:
        for err in parser.errors:
            print(err)
        exit(1)
    with open("AST.json", "w") as json_file:
        json.dump(program.json(), json_file, indent=4)

    print("AST.json created")




def code_gen_debug():
    lexer = Lexer(code=code)
    parser = Parser(lexer=lexer)
    program = parser.parse_program()

    if len(parser.errors) > 0:
        for err in parser.errors:
            print(err)
        exit(1)
    compiler = Compiler()
    compiler.compile(node=program)

    module = compiler.module
    module.triple = llvm.get_default_triple()

    with open("code.ll", "w") as ll_file:
        ll_file.write(str(module))

    print("code.ll created")


def code_debug():
    lexer = Lexer(code=code)
    parser = Parser(lexer=lexer)
    program = parser.parse_program()

    compiler = Compiler()
    compiler.compile(node=program)

    module = compiler.module
    module.triple = llvm.get_default_triple()

    llvm.initialize()
    llvm.initialize_native_target()
    llvm.initialize_native_asmprinter()

    try:
        llvm_ir_parsed = llvm.parse_assembly(str(module))
        llvm_ir_parsed.verify()
    except Exception as e:
        print(e)
        raise

    target_machine = llvm.Target.from_default_triple().create_target_machine()

    engine = llvm.create_mcjit_compiler(llvm_ir_parsed, target_machine)
    engine.finalize_object()

    entry = engine.get_function_address('main')
    cfunc = CFUNCTYPE(c_int)(entry)

    st = time.time()

    result = cfunc()

    end = time.time()

    print(f"Output: {result}, Time: {round((end - st) * 1000, 6)} ms.")


def main():

    parser_debug()
    code_gen_debug()
    code_debug()



if __name__ == "__main__":
    with open("tests/test_optimizer.txt", "r") as file:
        code = file.read()

    main()
