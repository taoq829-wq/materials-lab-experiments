import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.optimize import curve_fit

plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['font.sans-serif'] = ['DejaVu Sans']

# ===== 仪器已知参数 =====
nu_sample = 0.27  # 样品泊松比
Ei = 1141e9       # 金刚石压头模量 Pa
nui = 0.07        # 金刚石压头泊松比
# Berkovich压头 面积函数 A = 24.5 * hc^2 (单位nm²，对应P单位mN，h单位nm)

src_path = r"C:\Users\Administrator\Desktop\实验 大三上\纳米压痕\111.xls"

# 读取仪器结果
results_df = pd.read_excel(src_path, sheet_name='Results', header=None)
# 仪器给出的三个点数据
instrument = {
    'Test 001': {'E': 74.1, 'H': 0.41, 'Pmax': 9.956, 'hmax': 1033.8, 'S': 0.41693},  # S单位mN/nm: 416930 N/m = 0.41693 mN/nm
    'Test 002': {'E': 234.3, 'H': 3.62, 'Pmax': 9.955, 'hmax': 367.8, 'S': 0.38739},
    'Test 003': {'E': 238.7, 'H': 4.14, 'Pmax': 9.949, 'hmax': 346.9, 'S': 0.367813}
}

test_sheets = ['Test 001', 'Test 002', 'Test 003']
colors = ['#1f77b4', '#ff7f0e', '#2ca02c']

def oliver_pharr(h, P, Pmax_idx):
    """Oliver-Pharr方法计算S, hc, Er, H, E"""
    hmax = h[Pmax_idx]
    Pmax = P[Pmax_idx]
    
    # 取卸载段（P从Pmax降到0的部分），取卸载段上部30%-90%数据拟合幂律 P = alpha*(h - hf)^m
    # 找到卸载段：P开始下降之后的部分
    unload_start = Pmax_idx
    # 找卸载段结束（P接近0的点）
    unload_end = Pmax_idx
    for i in range(Pmax_idx, len(P)):
        if P[i] < 0.01 * Pmax:
            unload_end = i
            break
    
    # 取卸载段上部25%-90%的点拟合
    unload_P = P[unload_start:unload_end]
    unload_h = h[unload_start:unload_end]
    n = len(unload_P)
    fit_start = int(0.1 * n)
    fit_end = int(0.8 * n)
    fit_h = unload_h[fit_start:fit_end]
    fit_P = unload_P[fit_start:fit_end]
    
    # 幂律拟合 P = alpha*(h - hf)^m
    def power_law(h, alpha, hf, m):
        return alpha * (h - hf) ** m
    
    try:
        popt, _ = curve_fit(power_law, fit_h, fit_P, p0=[1e-3, hmax*0.7, 1.5], maxfev=10000)
        alpha, hf, m = popt
    except:
        # 失败的话用线性拟合卸载斜率
        slope, intercept = np.polyfit(fit_h, fit_P, 1)
        S = slope  # mN/nm
        hc = hmax - 0.75 * Pmax / S
        A = 24.5 * hc**2  # nm²
        H = Pmax / A * 1e3  # P是mN，A是nm²，1 mN/nm² = 1e9 Pa = 1e3 GPa
        Er = np.sqrt(np.pi) / (2 * np.sqrt(A)) * S * 1e9  # S: mN/nm = 1e3 N/m, A: nm²=1e-18 m²
        Er = Er / 1e9  # 转GPa
        E = 1 / ((1 - nu_sample**2)/Er - (1 - nui**2)/Ei*1e-9)
        return S, hc, H, E, hmax, Pmax
    
    # 刚度S = dP/dh 在hmax处 = alpha*m*(hmax - hf)^(m-1)
    S = alpha * m * (hmax - hf)**(m-1)  # mN/nm
    
    # 接触深度 hc = hmax - epsilon*Pmax/S，Berkovich压头epsilon=0.75
    epsilon = 0.75
    hc = hmax - epsilon * Pmax / S
    
    # 接触面积A = 24.5 * hc² (Berkovich，单位nm²)
    A = 24.5 * hc**2
    
    # 硬度 H = Pmax / A，单位转换：P是mN，A是nm²
    # P(mN) = 1e-3 N; A(nm²) = 1e-18 m²; 1 GPa = 1e9 Pa
    # H(Pa) = (P*1e-3) / (A*1e-18) = P*1e15 / A
    # H(GPa) = P*1e15 / (A*1e9) = P*1e6 / A
    H = Pmax / A * 1e6  # GPa
    
    # 折算模量 Er = (sqrt(pi)/(2*sqrt(A))) * S
    # S单位mN/nm = 1e-3 N / 1e-9 m = 1e6 N/m；A单位nm²=1e-18 m²
    S_SI = S * 1e6  # N/m
    A_SI = A * 1e-18  # m²
    Er = (np.sqrt(np.pi) / (2 * np.sqrt(A_SI))) * S_SI  # Pa
    Er_GPa = Er / 1e9
    
    # 样品模量 E
    Er_inv = 1/Er_GPa
    term = (1 - nui**2) / (Ei / 1e9)
    E = 1 / ((1 - nu_sample**2)/Er_GPa - term)
    
    return S, hc, H, E, hmax, Pmax

results = {}
plt.figure(figsize=(10,7), dpi=150)

for i, sheet in enumerate(test_sheets):
    df = pd.read_excel(src_path, sheet_name=sheet, header=None, skiprows=2)
    df.columns = ['Segment', 'h_nm', 'P_mN', 't_s']
    # 去掉Segment列的非数值行
    df = df.dropna(subset=['h_nm', 'P_mN'])
    h = df['h_nm'].values.astype(float)
    P = df['P_mN'].values.astype(float)
    
    # 找最大载荷点
    Pmax_idx = np.argmax(P)
    
    S, hc, H_calc, E_calc, hmax, Pmax = oliver_pharr(h, P, Pmax_idx)
    
    results[sheet] = {
        'hmax': hmax, 'Pmax': Pmax,
        'S_calc': S, 'S_inst': instrument[sheet]['S'],
        'hc': hc,
        'H_calc': H_calc, 'H_inst': instrument[sheet]['H'],
        'E_calc': E_calc, 'E_inst': instrument[sheet]['E']
    }
    
    plt.plot(h, P, color=colors[i], lw=1.5, label=f"{sheet} (Pmax={Pmax:.2f} mN, hmax={hmax:.1f} nm)")

plt.xlabel("Displacement h / nm", fontsize=12)
plt.ylabel("Load P / mN", fontsize=12)
plt.title("Nanoindentation P-h Curves (3 Tests)", fontsize=13)
plt.legend(fontsize=10)
plt.grid(alpha=0.3)
plt.tight_layout()
plt.savefig("nanoindent_ph_curves.png", dpi=300, bbox_inches="tight")
plt.close()

# 输出结果对比表
print("="*80)
print(f"{'Test':<12} {'参数':<8} {'计算值':<12} {'仪器值':<12} {'相对误差':<10}")
print("-"*80)
for sheet in test_sheets:
    r = results[sheet]
    e_err_E = abs(r['E_calc'] - r['E_inst'])/r['E_inst']*100
    e_err_H = abs(r['H_calc'] - r['H_inst'])/r['H_inst']*100
    e_err_S = abs(r['S_calc'] - r['S_inst'])/r['S_inst']*100
    print(f"{sheet:<12} {'E(GPa)':<8} {r['E_calc']:<12.2f} {r['E_inst']:<12.2f} {e_err_E:<10.1f}%")
    print(f"{'':<12} {'H(GPa)':<8} {r['H_calc']:<12.3f} {r['H_inst']:<12.2f} {e_err_H:<10.1f}%")
    print(f"{'':<12} {'S(mN/nm)':<8} {r['S_calc']:<12.2f} {r['S_inst']:<12.2f} {e_err_S:<10.1f}%")
    print("-"*80)

# 保存结果到csv
import csv
with open('nanoindent_results.csv', 'w', newline='', encoding='utf-8-sig') as f:
    writer = csv.writer(f)
    writer.writerow(['Test', 'Pmax(mN)', 'hmax(nm)', 'S_calc(mN/nm)', 'S_inst(mN/nm)', 
                     'H_calc(GPa)', 'H_inst(GPa)', 'E_calc(GPa)', 'E_inst(GPa)'])
    for sheet in test_sheets:
        r = results[sheet]
        writer.writerow([sheet, f"{r['Pmax']:.3f}", f"{r['hmax']:.1f}",
                         f"{r['S_calc']:.2f}", f"{r['S_inst']:.2f}",
                         f"{r['H_calc']:.3f}", f"{r['H_inst']:.2f}",
                         f"{r['E_calc']:.2f}", f"{r['E_inst']:.2f}"])

print("\nP-h曲线已保存: nanoindent_ph_curves.png")
print("对比结果已保存: nanoindent_results.csv")
