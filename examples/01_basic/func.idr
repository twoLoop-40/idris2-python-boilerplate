module Main

private helperFunction: Int -> Int
helperFunction x = x + 1

public export apiFunction : Int -> Int
apiFunction x = helperFunction x * 2

 

main : IO ()
main = printLn (apiFunction 5)

