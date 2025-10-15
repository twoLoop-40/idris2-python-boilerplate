module Main

import Data.Vect
import Data.Fin

||| A safe list with length tracking
||| This demonstrates dependent types for compile-time guarantees

-- Basic safe operations

||| Safe head: only works on non-empty lists
||| Type guarantees: list has at least 1 element
safeHead : Vect (S n) a -> a
safeHead (x :: xs) = x

||| Safe tail: only works on non-empty lists
safeTail : Vect (S n) a -> Vect n a
safeTail (x :: xs) = xs

||| Safe indexing using Fin (bounded natural numbers)
||| Fin n means: natural number strictly less than n
||| This makes out-of-bounds access impossible!
safeIndex : Fin n -> Vect n a -> a
safeIndex FZ (x :: xs) = x
safeIndex (FS k) (x :: xs) = safeIndex k xs

||| Take exactly n elements from a vector
||| Type ensures the vector has at least n elements
safeTake : (n : Nat) -> Vect (n + m) a -> Vect n a
safeTake Z xs = []
safeTake (S k) (x :: xs) = x :: safeTake k xs

||| Drop exactly n elements from a vector
safeDrop : (n : Nat) -> Vect (n + m) a -> Vect m a
safeDrop Z xs = xs
safeDrop (S k) (x :: xs) = safeDrop k xs

||| Zip two vectors of the same length
||| Type guarantees: both inputs have exactly the same length
zipVect : Vect n a -> Vect n b -> Vect n (a, b)
zipVect [] [] = []
zipVect (x :: xs) (y :: ys) = (x, y) :: zipVect xs ys

||| Replicate a value n times
||| Result is guaranteed to have exactly n elements
safeReplicate : (n : Nat) -> a -> Vect n a
safeReplicate Z x = []
safeReplicate (S k) x = x :: safeReplicate k x

-- Advanced: Matrix operations with dependent types

||| Matrix with dimensions in the type
||| Matrix rows cols a = matrix with 'rows' rows and 'cols' columns
Matrix : Nat -> Nat -> Type -> Type
Matrix rows cols a = Vect rows (Vect cols a)

||| Create a zero matrix
zeroMatrix : (rows : Nat) -> (cols : Nat) -> Matrix rows cols Int
zeroMatrix rows cols = safeReplicate rows (safeReplicate cols 0)

||| Matrix addition: dimensions must match
||| Compiler ensures both matrices have same size
matAdd : Matrix r c Int -> Matrix r c Int -> Matrix r c Int
matAdd [] [] = []
matAdd (row1 :: rows1) (row2 :: rows2) =
  zipWith (+) row1 row2 :: matAdd rows1 rows2

||| Get element at position (i, j)
||| Fin types guarantee indices are in bounds!
matIndex : Fin r -> Fin c -> Matrix r c a -> a
matIndex i j mat = safeIndex j (safeIndex i mat)

-- Business logic example: Safe vector operations

||| Map over a vector - length is preserved
mapVect : (a -> b) -> Vect n a -> Vect n b
mapVect f [] = []
mapVect f (x :: xs) = f x :: mapVect f xs

||| Sum all elements in a vector
sumVect : Num a => Vect n a -> a
sumVect [] = 0
sumVect (x :: xs) = x + sumVect xs

-- Example with validation

||| A non-empty list
||| Type guarantees at least one element
data NonEmpty : Type -> Type where
  MkNonEmpty : (head : a) -> (tail : List a) -> NonEmpty a

||| Convert Vect (S n) to NonEmpty
||| Both guarantee non-emptiness!
vectToNonEmpty : Vect (S n) a -> NonEmpty a
vectToNonEmpty (x :: xs) = MkNonEmpty x (toList xs)

||| Safe minimum - only works on non-empty vectors
||| Returns the minimum element
safeMinimum : Ord a => Vect (S n) a -> a
safeMinimum (x :: []) = x
safeMinimum (x :: y :: ys) = min x (safeMinimum (y :: ys))

||| Safe maximum - only works on non-empty vectors
safeMaximum : Ord a => Vect (S n) a -> a
safeMaximum (x :: []) = x
safeMaximum (x :: y :: ys) = max x (safeMaximum (y :: ys))

-- Example main function for testing
main : IO ()
main = do
  putStrLn "=== Safe List Operations ==="

  -- Safe head examples
  let vec1 : Vect 5 Int = [1, 2, 3, 4, 5]
  printLn $ "Head: " ++ show (safeHead vec1)  -- 1

  -- Safe indexing (Fin ensures in bounds)
  printLn $ "Index 0: " ++ show (safeIndex 0 vec1)  -- 1
  printLn $ "Index 2: " ++ show (safeIndex 2 vec1)  -- 3

  -- Take/drop
  printLn $ "Take 3: " ++ show (safeTake 3 vec1)  -- [1, 2, 3]
  printLn $ "Drop 2: " ++ show (safeDrop 2 vec1)  -- [3, 4, 5]

  -- Zip
  let vec2 : Vect 5 Char = ['a', 'b', 'c', 'd', 'e']
  printLn $ "Zipped: " ++ show (zipVect vec1 vec2)  -- [(1,'a'), (2,'b'), ...]

  putStrLn "\n=== Matrix Operations ==="

  -- Matrix operations
  let mat1 : Matrix 2 3 Int = [[1, 2, 3], [4, 5, 6]]
  let mat2 : Matrix 2 3 Int = [[7, 8, 9], [10, 11, 12]]
  printLn $ "Matrix Add: " ++ show (matAdd mat1 mat2)  -- [[8, 10, 12], [14, 16, 18]]

  -- Matrix indexing
  printLn $ "Element at (0,1): " ++ show (matIndex 0 1 mat1)  -- 2
  printLn $ "Element at (1,2): " ++ show (matIndex 1 2 mat1)  -- 6

  putStrLn "\n=== Safe Min/Max ==="

  -- Safe minimum/maximum
  let nums : Vect 4 Int = [42, 17, 93, 5]
  printLn $ "Minimum: " ++ show (safeMinimum nums)  -- 5
  printLn $ "Maximum: " ++ show (safeMaximum nums)  -- 93

  putStrLn "\n✅ All operations completed safely!"
