; ModuleID = "main"
target triple = "x86_64-pc-windows-msvc"
target datalayout = ""

@"true" = constant i1 1
@"false" = constant i1 0
define i32 @"add"(i32 %".1", i32 %".2")
{
add_entry:
  %".4" = alloca i32
  store i32 %".1", i32* %".4"
  %".6" = alloca i32
  store i32 %".2", i32* %".6"
  %".8" = load i32, i32* %".4"
  %".9" = load i32, i32* %".6"
  %".10" = add i32 %".8", %".9"
  ret i32 %".10"
}

define i32 @"sub"(i32 %".1", i32 %".2")
{
sub_entry:
  %".4" = alloca i32
  store i32 %".1", i32* %".4"
  %".6" = alloca i32
  store i32 %".2", i32* %".6"
  %".8" = load i32, i32* %".4"
  %".9" = load i32, i32* %".6"
  %".10" = sub i32 %".8", %".9"
  ret i32 %".10"
}

define i32 @"main"()
{
main_entry:
  %".2" = alloca i32
  store i32 50, i32* %".2"
  store i32 100, i32* %".2"
  store i32 4, i32* %".2"
  store i32 2, i32* %".2"
  %".7" = load i32, i32* %".2"
  ret i32 %".7"
}
