import numpy as np


def get_reference_signals(freqs, sampling_rate, num_seconds, num_harmonics=3):
    """
    第一步核心任务：构建 CCA 参考信号矩阵 Y_f

    参数:
    freqs: list, 你的刺激频率列表 [8, 9, 10, 11, 13]
    sampling_rate: int, 设备采样率，申请书中提到 >= 250Hz
    num_seconds: float, 数据窗口长度，申请书中提到 0.5-1秒
    num_harmonics: int, 谐波数量，申请书建议 2-3次，这里默认取3以提高精度

    返回:
    reference_signals: dict, 键为频率，值为对应的参考信号矩阵 (Nh*2, Ns)
    """
    reference_signals = {}
    t = np.arange(0, int(num_seconds * sampling_rate)) / sampling_rate

    for f in freqs:
        y_f = []
        for h in range(1, num_harmonics + 1):
            # 生成正弦和余弦分量 (sin(2*pi*f*h*t), cos(2*pi*f*h*t))
            y_f.append(np.sin(2 * np.pi * f * h * t))
            y_f.append(np.cos(2 * np.pi * f * h * t))

        # 转换为 numpy 矩阵
        reference_signals[f] = np.array(y_f)

    return reference_signals


# --- 测试代码 ---
if __name__ == "__main__":
    # 项目申请书中的参数
    target_freqs = [8, 9, 10, 11, 13]  #
    fs = 250  # [cite: 152]
    duration = 1.0  # [cite: 119]

    refs = get_reference_signals(target_freqs, fs, duration)

    print(f"频率 8Hz 的参考矩阵形状: {refs[8].shape}")
    # 预期输出: (6, 250) -> 6行代表3次谐波的sin/cos对，250列代表1秒的数据点