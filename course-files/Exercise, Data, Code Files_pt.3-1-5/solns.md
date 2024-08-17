(1) if both hamburgers and hot dogs, then also fries.

    (w_hm + w_hd) <= 1 + w_ff

(2) ff only if either hd or hm (or both)

    (w_hm + w_hd >= w_ff)

   hm  hd  ff    hm + hd >= 1  
   0   0   0      0
   0   0   1      1
   0   1   0      1
   0   1   1      1
   1   0   0      1
   1   0   1      1
   1   1   0      1
   1   1   1      1

(3) either:
  (i) steak
  (ii) both hm and hd
  (iii) both (i) and (ii)

  2 * w_s + w_hm + w_hd >= 2

(4) if no steak, then both hd and hm

   w_s  w_hd  w_hm
   0     0     0 
   0     0     1
   0     1     0
   0     1     1     yes
   1     0     0     yes
   1     0     1     yes
   1     1     0     yes
   1     1     1     yes

  2 * w_s + w_hm + w_hd >= 2

(5) both steak and hamburgers and hot dogs cannot be on menu

   w_s  w_hd  w_hm
   0     0     0     yes 
   0     0     1     yes
   0     1     0     yes
   0     1     1     yes
   1     0     0     yes
   1     0     1     yes
   1     1     0     yes
   1     1     1

   w_s + w_hm + w_hd <= 2

(6) The menu may not have both of these pairs:
  (i) steak and fish-and-chips
  (ii) hamburgers and hot dogs

   s   fc   hm   md
   0   0    0    0
   0   0    0    1
   0   0    1    0
   0   0    1    1   
   0   1    0    0
   0   1    0    1
   0   1    1    0
   0   1    1    1  
   1   0    0    0
   1   0    0    1
   1   0    1    0
   1   0    1    1 
   1   1    0    0 
   1   1    0    1
   1   1    1    0
   1   1    1    1   no

  w_s + w_fc + w_hm + w_hd <= 3


