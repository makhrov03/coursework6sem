; ModuleID = "main"
target triple = "x86_64-pc-windows-msvc"
target datalayout = ""

@"true" = constant i1 1
@"false" = constant i1 0


define i32 @"main"()
{
main_entry:
  %".2" = alloca i32
  store i32 2, i32* %".2"
  %".7" = load i32, i32* %".2"
  ret i32 %".7"
}
