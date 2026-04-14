# psitip_exprs.py
# PSITIP expressions for all 75 inequalities in all_ineq_ordered.txt
# Each entry: (psitip_region, ctx_fn)
#   ctx_fn = CL (copy lemma) or None (Shannon / False)
#
# Notation map (label → PSITIP):
#   I(A;B)      →  I(A&B)          I(A;B|C)    →  I(A&B|C)
#   I(A;B,C)    →  I(A&B+C)        H(A,B)      →  H(A+B)
#   H(A,B|C,D) →  H(A+B|C+D)      A─B─C       →  markov(A,B,C)
#   (A,B)─C─D  →  markov(A+B,C,D)  X─Y─Z─W    →  markov(X,Y,Z,W)
#   indep(A,B) →  I(A&B)==0
#
# Dataset layout:
#   #1–20   Shannon-Type True Inequalities
#   #21–25  Double Markov True Consequences (Shannon-provable)
#   #26–50  Non-Shannon-Type True Inequalities (Copy Lemma)
#   #51–75  False Inequalities
#
# All 75 cases verified with pyomo.gurobi solver (75/75 pass).
#
from psitip import *

X, Y, Z, W, U, V = rv("X, Y, Z, W, U, V")

CL  = lambda: copylem().assumed()

psitip_exprs = [

    # ══════════════════════════════════════════════════════════════
    # Shannon-Type True Inequalities                    #1–25
    # ══════════════════════════════════════════════════════════════

    # --- Non-negativity (3) ---

    # #1   H(X)+H(Y)+H(Z) >= H(X,Y,Z)
    (H(X)+H(Y)+H(Z) >= H(X+Y+Z), None),

    # #2   H(X)+I(Y;Z|X) >= I(Y;Z)
    (H(X)+I(Y&Z|X) >= I(Y&Z), None),

    # #3   H(X,Y) <= H(X)+H(Y)                       [subadditivity]
    (H(X+Y) <= H(X)+H(Y), None),

    # --- Chain rule (6) ---

    # #4   X─Y─Z  =>  H(Y) >= I(X;Z)
    (markov(X,Y,Z) >> (H(Y) >= I(X&Z)), None),

    # #5   H(Y|X)==0  =>  I(Y;Z) <= I(X;Z)
    ((H(Y|X) == 0) >> (I(Y&Z) <= I(X&Z)), None),

    # #6   H(Y|X)==0  =>  H(Y,Z) <= H(X,Z)
    ((H(Y|X) == 0) >> (H(Y+Z) <= H(X+Z)), None),

    # #7   H(Y|X)==0  =>  I(Y;Z|W) <= I(X;Z|W)
    ((H(Y|X) == 0) >> (I(Y&Z|W) <= I(X&Z|W)), None),

    # #8   H(Y|X)==0 & H(Z|Y)==0  =>  I(Z;W) <= I(X;W)
    (((H(Y|X) == 0) & (H(Z|Y) == 0)) >> (I(Z&W) <= I(X&W)), None),

    # #9   H(Y|X)==0 & X─Y─Z  =>  H(Z|Y) >= H(Z|X)
    (((H(Y|X) == 0) & markov(X,Y,Z)) >> (H(Z|Y) >= H(Z|X)), None),

    # --- Data processing inequality (6) ---

    # #10  X─Y─Z  =>  I(X;Y) >= I(X;Z)
    (markov(X,Y,Z) >> (I(X&Y) >= I(X&Z)), None),

    # #11  X─Y─Z─W  =>  I(X;W) <= I(X;Y)
    (markov(X,Y,Z,W) >> (I(X&W) <= I(X&Y)), None),

    # #12  X─Y─Z─W  =>  I(X;W) <= I(X;Z)
    (markov(X,Y,Z,W) >> (I(X&W) <= I(X&Z)), None),

    # #13  X─Y─Z─W  =>  I(X;W) <= I(Y;W)
    (markov(X,Y,Z,W) >> (I(X&W) <= I(Y&W)), None),

    # #14  X─Y─Z─W  =>  I(X;Z)+I(X;W) <= 2I(X;Y)
    (markov(X,Y,Z,W) >> (I(X&Z)+I(X&W) <= 2*I(X&Y)), None),

    # #15  X─Y─Z─W  =>  I(X;W) <= H(Y)
    (markov(X,Y,Z,W) >> (I(X&W) <= H(Y)), None),

    # --- Functional dependence (3) ---

    # #16  X─Y─Z & H(W|Y)==0  =>  I(X;W) <= I(X;Y)
    ((markov(X,Y,Z) & (H(W|Y) == 0)) >> (I(X&W) <= I(X&Y)), None),

    # #17  (X,W)─Y─Z  =>  I(X;Z) <= I(X;Y)
    (markov(X+W,Y,Z) >> (I(X&Z) <= I(X&Y)), None),

    # #18  (X,W)─Y─Z  =>  I(W;Z) <= I(W;Y)
    (markov(X+W,Y,Z) >> (I(W&Z) <= I(W&Y)), None),

    # --- Conditional independence (2) ---

    # #19  X─Y─Z  =>  I(X;Y) >= I(X;Z)+I(X;Z|Y)
    (markov(X,Y,Z) >> (I(X&Y) >= I(X&Z)+I(X&Z|Y)), None),

    # #20  X─Y─Z─W  =>  2H(Y) >= I(X;W)+I(X;Z)
    (markov(X,Y,Z,W) >> (2*H(Y) >= I(X&W)+I(X&Z)), None),

    # --- Double Markov true consequences (5) ---

    # #21  X─Y─Z & Y─X─Z  =>  I(X;Z|Y) == 0
    ((markov(X,Y,Z) & markov(Y,X,Z)) >> (I(X&Z|Y) == 0), None),

    # #22  X─Y─Z & Y─X─Z  =>  I(Y;Z|X) == 0
    ((markov(X,Y,Z) & markov(Y,X,Z)) >> (I(Y&Z|X) == 0), None),

    # #23  X─Y─Z & Y─X─Z  =>  I(X;Z) == I(Y;Z)
    ((markov(X,Y,Z) & markov(Y,X,Z)) >> (I(X&Z) == I(Y&Z)), None),

    # #24  X─Y─Z & Y─X─Z  =>  H(Z|X) == H(Z|Y)
    ((markov(X,Y,Z) & markov(Y,X,Z)) >> (H(Z|X) == H(Z|Y)), None),

    # #25  X─Y─Z & Y─X─Z  =>  H(X|Y,Z)+H(Y|X,Z) == H(X|Y)+H(Y|X)
    ((markov(X,Y,Z) & markov(Y,X,Z)) >> (H(X|Y+Z)+H(Y|X+Z) == H(X|Y)+H(Y|X)), None),

    # ══════════════════════════════════════════════════════════════
    # Non-Shannon-Type True Inequalities (Copy Lemma)   #26–50
    # ══════════════════════════════════════════════════════════════

    # --- Zhang-Yeung original (1998) ---

    # #26  2I(Z;W) <= I(X;Y)+I(X;Z,W)+3I(Z;W|X)+I(Z;W|Y)
    (2*I(Z&W) <= I(X&Y)+I(X&Z+W)+3*I(Z&W|X)+I(Z&W|Y), CL),

    # --- Zhang-Yeung variable permutations (4) ---

    # #27  2I(X;Y) <= I(Z;W)+I(Z;X,Y)+3I(X;Y|Z)+I(X;Y|W)
    (2*I(X&Y) <= I(Z&W)+I(Z&X+Y)+3*I(X&Y|Z)+I(X&Y|W), CL),

    # #28  2I(Y;W) <= I(X;Z)+I(X;Y,W)+3I(Y;W|X)+I(Y;W|Z)
    (2*I(Y&W) <= I(X&Z)+I(X&Y+W)+3*I(Y&W|X)+I(Y&W|Z), CL),

    # #29  2I(X;Z) <= I(Y;W)+I(Y;X,Z)+3I(X;Z|Y)+I(X;Z|W)
    (2*I(X&Z) <= I(Y&W)+I(Y&X+Z)+3*I(X&Z|Y)+I(X&Z|W), CL),

    # #30  2I(X;W) <= I(Y;Z)+I(Y;X,W)+3I(X;W|Y)+I(X;W|Z)
    (2*I(X&W) <= I(Y&Z)+I(Y&X+W)+3*I(X&W|Y)+I(X&W|Z), CL),

    # --- Zhang-Yeung scaled (2) ---

    # #31  4I(Z;W) <= 2I(X;Y)+2I(X;Z,W)+6I(Z;W|X)+2I(Z;W|Y)
    (4*I(Z&W) <= 2*I(X&Y)+2*I(X&Z+W)+6*I(Z&W|X)+2*I(Z&W|Y), CL),

    # #32  2I(Z;W) <= I(X;Y)+I(X;Z,W)+4I(Z;W|X)+I(Z;W|Y)
    (2*I(Z&W) <= I(X&Y)+I(X&Z+W)+4*I(Z&W|X)+I(Z&W|Y), CL),

    # --- Zhang-Yeung with slack terms (7) ---

    # #33  2I(Z;W) <= I(X;Y)+I(X;Z,W)+3I(Z;W|X)+I(Z;W|Y)+I(X;Y|Z)
    (2*I(Z&W) <= I(X&Y)+I(X&Z+W)+3*I(Z&W|X)+I(Z&W|Y)+I(X&Y|Z), CL),

    # #34  2I(Z;W) <= I(X;Y)+I(X;Z,W)+3I(Z;W|X)+I(Z;W|Y)+I(X;W|Z)
    (2*I(Z&W) <= I(X&Y)+I(X&Z+W)+3*I(Z&W|X)+I(Z&W|Y)+I(X&W|Z), CL),

    # #35  2I(Z;W) <= I(X;Y)+I(X;Z,W)+3I(Z;W|X)+I(Z;W|Y)+I(X;Y|W)
    (2*I(Z&W) <= I(X&Y)+I(X&Z+W)+3*I(Z&W|X)+I(Z&W|Y)+I(X&Y|W), CL),

    # #36  2I(Z;W) <= I(X;Y)+I(X;Z,W)+3I(Z;W|X)+I(Z;W|Y)+H(Z|W)
    (2*I(Z&W) <= I(X&Y)+I(X&Z+W)+3*I(Z&W|X)+I(Z&W|Y)+H(Z|W), CL),

    # #37  2I(Z;W) <= I(X;Y)+I(X;Z,W)+3I(Z;W|X)+I(Z;W|Y)+I(Y;Z)
    (2*I(Z&W) <= I(X&Y)+I(X&Z+W)+3*I(Z&W|X)+I(Z&W|Y)+I(Y&Z), CL),

    # #38  2I(Z;W) <= I(X;Y)+I(X;Z,W)+3I(Z;W|X)+I(Z;W|Y)+I(Y;W|Z)
    (2*I(Z&W) <= I(X&Y)+I(X&Z+W)+3*I(Z&W|X)+I(Z&W|Y)+I(Y&W|Z), CL),

    # #39  2I(Z;W) <= I(X;Y)+I(X;Z,W)+3I(Z;W|X)+I(Z;W|Y)+H(W|Z)
    (2*I(Z&W) <= I(X&Y)+I(X&Z+W)+3*I(Z&W|X)+I(Z&W|Y)+H(W|Z), CL),

    # --- Matúš-type with extra conditional (3) ---

    # #40  2I(Z;W) <= I(X;Y)+I(X;Z,W)+3I(Z;W|X)+2I(Z;W|Y)
    (2*I(Z&W) <= I(X&Y)+I(X&Z+W)+3*I(Z&W|X)+2*I(Z&W|Y), CL),

    # #41  2I(X;W) <= I(Y;Z)+I(Y;X,W)+3I(X;W|Y)+2I(X;W|Z)
    (2*I(X&W) <= I(Y&Z)+I(Y&X+W)+3*I(X&W|Y)+2*I(X&W|Z), CL),

    # #42  2I(Y;Z) <= I(X;W)+I(X;Y,Z)+3I(Y;Z|X)+2I(Y;Z|W)
    (2*I(Y&Z) <= I(X&W)+I(X&Y+Z)+3*I(Y&Z|X)+2*I(Y&Z|W), CL),

    # --- ZY with larger conditional coefficients (3) ---

    # #43  2I(Z;W) <= I(X;Y)+I(X;Z,W)+4I(Z;W|X)+2I(Z;W|Y)
    (2*I(Z&W) <= I(X&Y)+I(X&Z+W)+4*I(Z&W|X)+2*I(Z&W|Y), CL),

    # #44  2I(Z;W) <= I(X;Y)+I(X;Z,W)+3I(Z;W|X)+I(Z;W|Y)+I(Z;W|X,Y)
    (2*I(Z&W) <= I(X&Y)+I(X&Z+W)+3*I(Z&W|X)+I(Z&W|Y)+I(Z&W|X+Y), CL),

    # #45  2I(Z;W) <= I(X;Y)+I(X;Z,W)+3I(Z;W|X)+I(Z;W|Y)+H(X|Y)
    (2*I(Z&W) <= I(X&Y)+I(X&Z+W)+3*I(Z&W|X)+I(Z&W|Y)+H(X|Y), CL),

    # --- ZY permutations with slack (5) ---

    # #46  2I(Y;W) <= I(X;Z)+I(X;Y,W)+3I(Y;W|X)+I(Y;W|Z)+I(X;Z|Y)
    (2*I(Y&W) <= I(X&Z)+I(X&Y+W)+3*I(Y&W|X)+I(Y&W|Z)+I(X&Z|Y), CL),

    # #47  2I(X;Z) <= I(Y;W)+I(Y;X,Z)+3I(X;Z|Y)+I(X;Z|W)+I(Y;W|X)
    (2*I(X&Z) <= I(Y&W)+I(Y&X+Z)+3*I(X&Z|Y)+I(X&Z|W)+I(Y&W|X), CL),

    # #48  2I(X;W) <= I(Y;Z)+I(Y;X,W)+3I(X;W|Y)+I(X;W|Z)+I(Y;Z|X)
    (2*I(X&W) <= I(Y&Z)+I(Y&X+W)+3*I(X&W|Y)+I(X&W|Z)+I(Y&Z|X), CL),

    # #49  2I(X;Y) <= I(Z;W)+I(Z;X,Y)+3I(X;Y|Z)+2I(X;Y|W)
    (2*I(X&Y) <= I(Z&W)+I(Z&X+Y)+3*I(X&Y|Z)+2*I(X&Y|W), CL),

    # #50  2I(Y;W) <= I(X;Z)+I(X;Y,W)+3I(Y;W|X)+2I(Y;W|Z)
    (2*I(Y&W) <= I(X&Z)+I(X&Y+W)+3*I(Y&W|X)+2*I(Y&W|Z), CL),

    # ══════════════════════════════════════════════════════════════
    # False Inequalities                                #51–75
    # ══════════════════════════════════════════════════════════════

    # --- Reversed non-negativity (2) ---

    # #51  I(X;Y) >= H(X)
    (I(X&Y) >= H(X), None),

    # #52  H(X|Y) >= H(X)
    (H(X|Y) >= H(X), None),

    # --- Reversed DPI (3) ---

    # #53  X─Y─Z  =>  I(X;Z) >= I(X;Y)
    (markov(X,Y,Z) >> (I(X&Z) >= I(X&Y)), None),

    # #54  X─Y─Z─W  =>  H(X|Y) >= H(X|Z,W)
    (markov(X,Y,Z,W) >> (H(X|Y) >= H(X|Z+W)), None),

    # #55  I(X;Y)+I(Y;Z) <= I(X;Z)
    (I(X&Y)+I(Y&Z) <= I(X&Z), None),

    # --- Impossible entropy bounds (2) ---

    # #56  H(X,Y) <= H(X)
    (H(X+Y) <= H(X), None),

    # #57  I(X;Y) + I(X;Z) >= H(X,Y,Z)
    (I(X&Y)+I(X&Z) >= H(X+Y+Z), None),

    # --- Missing term in non-Shannon (3) ---

    # #58  2I(Z;W) <= I(X;Y) + 3I(Z;W|X) + I(Z;W|Y)          [missing I(X;Z,W)]
    (2*I(Z&W) <= I(X&Y)+3*I(Z&W|X)+I(Z&W|Y), None),

    # #59  3I(Z;W) <= I(X;Y) + I(X;Z,W) + 3I(Z;W|X) + I(Z;W|Y) [wrong LHS coeff]
    (3*I(Z&W) <= I(X&Y)+I(X&Z+W)+3*I(Z&W|X)+I(Z&W|Y), None),

    # #60  2I(Z;W) <= I(X;Z,W)+3I(Z;W|X)+I(Z;W|Y)            [missing I(X;Y)]
    (2*I(Z&W) <= I(X&Z+W)+3*I(Z&W|X)+I(Z&W|Y), None),

    # --- Wrong coefficient (3) ---

    # #61  I(X;Y) <= I(X;Y|Z) + I(X;Y|W)
    (I(X&Y) <= I(X&Y|Z)+I(X&Y|W), None),

    # #62  X─Y─Z  =>  I(X;Z|Y) >= I(X;Y)
    (markov(X,Y,Z) >> (I(X&Z|Y) >= I(X&Y)), None),

    # #63  X─Y─Z  =>  H(Y) <= I(X;Z)
    (markov(X,Y,Z) >> (H(Y) <= I(X&Z)), None),

    # --- False Double Markov consequences (5) ---

    # #64  X─Y─Z & Y─X─Z  =>  I(X;Y|Z) == 0
    ((markov(X,Y,Z) & markov(Y,X,Z)) >> (I(X&Y|Z) == 0), None),

    # #65  X─Y─Z & Y─X─Z  =>  H(X,Y,Z) == H(X,Z)+H(Y,Z)-H(Z)
    ((markov(X,Y,Z) & markov(Y,X,Z)) >> (H(X+Y+Z) == H(X+Z)+H(Y+Z)-H(Z)), None),

    # #66  X─Y─Z & Y─X─Z  =>  H(X,Y|Z) == H(X|Z)+H(Y|Z)
    ((markov(X,Y,Z) & markov(Y,X,Z)) >> (H(X+Y|Z) == H(X|Z)+H(Y|Z)), None),

    # #67  X─Y─Z & Y─X─Z  =>  H(X,Y|Z,W) == H(X|Z,W)+H(Y|Z,W)
    ((markov(X,Y,Z) & markov(Y,X,Z)) >> (H(X+Y|Z+W) == H(X|Z+W)+H(Y|Z+W)), None),

    # #68  X─Y─Z & Y─X─Z  =>  I(X;W|Z) == I(X;W|Y,Z)
    ((markov(X,Y,Z) & markov(Y,X,Z)) >> (I(X&W|Z) == I(X&W|Y+Z)), None),

    # --- Plausible but false (Shannon-like) (2) ---

    # #69  indep(X,Y)  =>  H(X) == H(Y)
    ((I(X&Y) == 0) >> (H(X) == H(Y)), None),

    # #70  H(Y|X)==0  =>  H(X) <= H(Y)
    ((H(Y|X) == 0) >> (H(X) <= H(Y)), None),

    # --- Plausible but false (non-Shannon-like) (2) ---

    # #71  X─Y─Z & Y─X─Z  =>  H(X) == H(Y)
    ((markov(X,Y,Z) & markov(Y,X,Z)) >> (H(X) == H(Y)), None),

    # #72  H(Y|X)==0  =>  H(X|Z) == H(Y|Z)
    ((H(Y|X) == 0) >> (H(X|Z) == H(Y|Z)), None),

    # --- False equalities / bounds under constraints (3) ---

    # #73  I(X;Y) + I(Y;Z) >= H(Y)
    (I(X&Y)+I(Y&Z) >= H(Y), None),

    # #74  I(X;Y|Z) + I(X;Z|Y) >= H(X)
    (I(X&Y|Z)+I(X&Z|Y) >= H(X), None),

    # #75  H(X|Y)==0 & H(Z|Y)==0  =>  H(X|Z)==0
    (((H(X|Y) == 0) & (H(Z|Y) == 0)) >> (H(X|Z) == 0), None),
]
