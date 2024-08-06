Feature 4, and either feature 6 or 11 (or both) must be used:

   2x_4 + x_6 + x_11 >= 3

If feature 4 is not used, then either feature 6 or 11 (or both) must be used:
   is it x_4 + x_6 + x_11 >= 1?

x_4  x_6  x_11   LHS   RHS   Constraint true?  Want this result?
----------------------------------------------------------------
 0    0    0      0     1          f                no
 0    0    1      1     1          T                yes
 0    1    0      1     1          T                yes
 0    1    1      2     1          T                yes
 1    0    0      1     1          T                yes
 1    0    1      2     1          T                yes
 1    1    0      2     1          T                yes
 1    1    1      3     1          T                yes

We're all good here.

7. x_2 + x_3 <= 1

8. -x_1 + 2x_2 - x_3 >= 1

