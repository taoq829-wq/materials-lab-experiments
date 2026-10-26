import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

plt.rcParams['axes.unicode_minus'] = False

# 0% Sn pure Pb
t0 = [i*20 for i in range(0, 60)]
T0 = [398, 392, 385, 378, 371, 364, 358, 352, 346, 340,
      335, 330, 326, 324, 324, 324, 323, 320, 316, 312,
      308, 304, 300, 296, 292, 288, 284, 280, 276, 272,
      268, 264, 260, 256, 252, 248, 244, 240, 236, 232,
      228, 224, 220, 216, 212, 208, 204, 200, 196, 192,
      188, 184, 180, 176, 172, 168, 164, 160, 156, 152]

# 20% Sn hypoeutectic
t20 = [i*20 for i in range(0,70)]
T20 = [402, 395, 388, 381, 374, 367, 360, 354, 348, 342,
       337, 332, 328, 323, 323, 322, 318, 312, 306, 300,
       294, 288, 282, 276, 270, 264, 258, 252, 246, 240,
       234, 228, 222, 216, 210, 204, 198, 192, 188, 182,
       182, 182, 182, 181, 178, 174, 170, 166, 162, 158,
       154, 150, 146, 142, 138, 134, 130, 126, 122, 118,
       114, 110, 106, 102, 98, 94, 90, 86, 82, 78]

# 61.9% Sn eutectic
t619 = [i*20 for i in range(0,65)]
T619 = [458, 448, 438, 428, 418, 408, 398, 388, 378, 368,
        358, 348, 338, 328, 318, 308, 298, 288, 278, 268,
        258, 248, 238, 228, 218, 208, 198, 190, 182, 182,
        182, 182, 182, 180, 176, 172, 168, 164, 160, 156,
        152, 148, 144, 140, 136, 132, 128, 124, 120, 116,
        112, 108, 104, 100, 96, 92, 88, 84, 80, 76,
        72, 68, 64, 60, 56]

# 80% Sn hypereutectic
t80 = [i*20 for i in range(0,75)]
T80 = [356, 353, 349, 345, 340, 336, 331, 326, 321, 316,
       311, 304, 297, 290, 283, 276, 269, 262, 255, 248,
       241, 234, 229, 229, 229, 228, 226, 224, 222, 220,
       218, 216, 214, 212, 210, 208, 206, 204, 202, 200,
       198, 196, 194, 192, 190, 188, 186, 184, 182, 182,
       182, 182, 182, 181, 177, 173, 169, 165, 161, 157,
       153, 149, 145, 141, 137, 133, 129, 125, 121, 117,
       113, 109, 105, 101, 97]

# 100% Sn pure Sn
t100 = [i*20 for i in range(0,96)]
T100 = [415,411,405,399,392,386,380,373,366,361,
        354,348,342,336,330,325,320,315,310,304,
        299,295,291,286,282,278,274,270,266,262,
        258,255,251,248,244,241,238,235,232,232,
        232,232,232,232,231,230,228,226,226,225,
        223,221,220,219,216,212,206,201,197,194,
        191,188,185,182,180,177,175,173,171,169,
        167,165,163,161,159,158,156,154,153,151,
        149,148,146,145,143,142,140,139,138,136,
        135,133,132,131,129,128]

# Figure 1: Cooling curves
plt.figure(figsize=(10,6),dpi=150)
plt.plot(t0, T0, label="0% Sn (pure Pb)", lw=1.5)
plt.plot(t20, T20, label="20% Sn (hypoeutectic)", lw=1.5)
plt.plot(t619, T619, label="61.9% Sn (eutectic)", lw=1.5)
plt.plot(t80, T80, label="80% Sn (hypereutectic)", lw=1.5)
plt.plot(t100, T100, label="100% Sn (pure Sn)", lw=1.5)
plt.xlabel("Time t / s")
plt.ylabel("Temperature T / ℃")
plt.title("Pb-Sn Alloy Cooling Curves")
plt.legend()
plt.grid(alpha=0.3)
plt.tight_layout()
plt.savefig("cooling_curves.png", dpi=300, bbox_inches="tight")
plt.close()

# Figure 2: Pb-Sn phase diagram
plt.figure(figsize=(8,6),dpi=150)
x_sn = [0, 20, 61.9, 80, 100]
T_liquid = [324, 323, 182, 229, 232]
plt.hlines(y=182, xmin=0, xmax=100, color="red", linestyle="--", label="Eutectic line 182℃")
plt.plot(x_sn, T_liquid, marker="o", c="#2277bb", label="Measured liquidus")
plt.xlabel("Mass fraction of Sn w(Sn) / %")
plt.ylabel("Temperature T / ℃")
plt.title("Pb-Sn Binary Phase Diagram")
plt.grid(alpha=0.3)
plt.legend()
plt.tight_layout()
plt.savefig("phase_diagram.png", dpi=300, bbox_inches="tight")
plt.close()

print("Done: cooling_curves.png and phase_diagram.png generated.")
