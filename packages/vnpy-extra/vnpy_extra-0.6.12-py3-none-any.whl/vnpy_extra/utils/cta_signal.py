"""
@author  : MG
@Time    : 2020/10/12 12:02
@File    : signal.py
@contact : mmmaaaggg@163.com
@desc    : 用于
"""
import typing

import numpy as np
from vnpy.app.cta_strategy import (
    TickData,
    BarData,
    CtaSignal as CtaSignalBase,
)
from vnpy.trader.constant import Interval

from .enhancement import BarGenerator, ArrayManager, CtaSignal


class MACDSignal(CtaSignalBase):
    """"""

    def __init__(self, fast_window: int, slow_window: int, signal_period: int,
                 threshold: int = 1, z_score: int = 1,
                 period: int = 30, interval: Interval = Interval.MINUTE, reverse_bs: int = 0):
        """
        :param fast_window
        :param slow_window
        :param signal_period
        :param threshold 阈值，超过正的阈值或低于负的阈值才会产生信号。分钟级数据由于数值波动较小，要适度减少这个中间地带
        :param z_score 标准化转换，None、0为关闭，>=1 转化的bar数量
        :param period
        :param interval
        :param reverse_bs
        """
        super().__init__()

        self.fast_window = fast_window
        self.slow_window = slow_window
        self.signal_period = signal_period
        self.interval = interval
        self.reverse_bs = reverse_bs
        # 分钟级数据由于数值波动较小，要适度减少这个中间地带
        self.threshold = threshold
        self.z_score = (z_score is None or z_score >= 1)  # 默认为True
        self.period = period if period != 0 else 30
        self.bg = BarGenerator(self.on_bar, window=self.period, on_window_bar=self.on_n_min_bar, interval=self.interval)
        size = max(self.fast_window, self.slow_window, self.signal_period) * 2
        size = np.max([size, z_score]) if self.z_score else size
        self.am = ArrayManager(size=size)
        # logger.info(f"fast_window, slow_window, signal_period, period="
        #             f"{self.fast_window, self.slow_window, self.signal_period, self.period}")

    def on_tick(self, tick: TickData):
        """
        Callback of new tick data update.
        """
        self.bg.update_tick(tick)

    def on_bar(self, bar: BarData):
        """
        Callback of new bar data update.
        """
        self.bg.update_bar(bar)

    def on_n_min_bar(self, bar: BarData):
        """"""
        self.am.update_bar(bar)
        if not self.am.inited:
            self.set_signal_pos(0)
            return

        _, _, macd = self.am.macd(self.fast_window, self.slow_window, self.signal_period, self.z_score)

        if macd < -self.threshold:
            self.set_signal_pos(1 if self.reverse_bs else -1)
        elif macd > self.threshold:
            self.set_signal_pos(-1 if self.reverse_bs else 1)
        else:
            # self.set_signal_pos(0)
            pass


class KDJSignal(CtaSignalBase):
    """"""

    def __init__(self, fastk_period: int = 9, slowk_period: int = 3, slowd_period: int = 3,
                 higher_boundary_add50: int = 20, enable_close: int = 1,
                 period: int = 30, interval: Interval = Interval.MINUTE, reverse_bs: int = 0):
        """"""
        super().__init__()

        self.fastk_period = fastk_period if fastk_period != 0 else 9
        self.slowk_period = slowk_period if slowk_period != 0 else 3
        self.slowd_period = slowd_period if slowd_period != 0 else 3
        self.interval = interval
        if higher_boundary_add50 is None or higher_boundary_add50 == 0:
            higher_boundary_add50 = 20

        self.higher_boundary = 50 + higher_boundary_add50
        self.lower_boundary = 50 - higher_boundary_add50
        self.enable_close = enable_close
        self.reverse_bs = reverse_bs

        self.period = period if period != 0 else 30
        self.bg = BarGenerator(self.on_bar, window=self.period, on_window_bar=self.on_n_min_bar, interval=self.interval)
        self.am = ArrayManager(size=self.fastk_period + self.slowk_period + self.slowd_period)
        # logger.info(f"fast_window, slow_window, signal_period, period="
        #             f"{self.fast_window, self.slow_window, self.signal_period, self.period}")
        self._k, self._d, self._j = None, None, None

    def on_tick(self, tick: TickData):
        """
        Callback of new tick data update.
        """
        self.bg.update_tick(tick)

    def on_bar(self, bar: BarData):
        """
        Callback of new bar data update.
        """
        self.bg.update_bar(bar)

    def on_n_min_bar(self, bar: BarData):
        """"""
        self.am.update_bar(bar)
        if not self.am.inited:
            self.set_signal_pos(0)
            return

        k, d, j = self.am.kdj(self.fastk_period, self.slowk_period, self.slowd_period)
        if self._k is None:
            self._k, self._d, self._j = k, d, j
            return
        if k > d and self._k < self._d and self._k < self.lower_boundary:
            # 低位金叉
            self.set_signal_pos(-1 if self.reverse_bs else 1)
        elif k < d and self._k > self._d and self._k > self.higher_boundary:
            # 高位死叉
            self.set_signal_pos(1 if self.reverse_bs else -1)
        elif self.enable_close:
            pos = self.get_signal_pos()
            if pos != 0:
                if self.reverse_bs:
                    pos = -pos

                if pos > 0 and k < d and self._k > self._d:
                    # 死叉 平 多仓
                    self.set_signal_pos(0)
                elif pos < 0 and k > d and self._k < self._d:
                    # 金叉 平 空仓
                    self.set_signal_pos(0)

        self._k, self._d, self._j = k, d, j


class RSISignal(CtaSignalBase):
    """"""

    def __init__(self, win_size: int = 9,
                 higher_boundary_add50: int = 20, period: int = 30,
                 enable_close: int = 0, interval: Interval = Interval.MINUTE,
                 reverse_bs: int = 0):
        """"""
        super().__init__()

        self.win_size = win_size if win_size != 0 else 9
        self.interval = interval if interval != 0 else Interval.MINUTE
        self.higher_boundary = 50 + (higher_boundary_add50 if higher_boundary_add50 != 0 else 20)
        self.lower_boundary = 50 - (higher_boundary_add50 if higher_boundary_add50 != 0 else 20)
        self.enable_close = enable_close
        self.reverse_bs = reverse_bs

        self.period = period if period != 0 else 30
        self.bg = BarGenerator(self.on_bar, window=self.period, on_window_bar=self.on_n_min_bar, interval=self.interval)
        self.am = ArrayManager(size=win_size + 1)
        # logger.info(f"fast_window, slow_window, signal_period, period="
        #             f"{self.fast_window, self.slow_window, self.signal_period, self.period}")

    def on_tick(self, tick: TickData):
        """
        Callback of new tick data update.
        """
        self.bg.update_tick(tick)

    def on_bar(self, bar: BarData):
        """
        Callback of new bar data update.
        """
        self.bg.update_bar(bar)

    def on_n_min_bar(self, bar: BarData):
        """"""
        self.am.update_bar(bar)
        if not self.am.inited:
            self.set_signal_pos(0)

        value = self.am.rsi(self.win_size)
        if value < self.lower_boundary:
            # 低位
            self.set_signal_pos(1 if self.reverse_bs else -1)
        elif value > self.higher_boundary:
            # 高位
            self.set_signal_pos(-1 if self.reverse_bs else 1)
        elif self.enable_close:
            pos = self.get_signal_pos()
            if self.reverse_bs:
                pos = -pos

            if pos > 0 and value < 50:
                # 平 多仓
                self.set_signal_pos(0)
            elif pos < 0 and value > 50:
                # 平 空仓
                self.set_signal_pos(0)


class BOLLSignal(CtaSignalBase):
    """"""

    def __init__(
            self, win_size: int = 26, dev: float = 1,
            period: int = 30, interval: Interval = Interval.MINUTE, reverse_bs: int = 0
    ):
        """"""
        super().__init__()

        self.win_size = win_size
        self.interval = interval
        self.dev = dev
        self.reverse_bs = reverse_bs

        self.period = period
        self.bg = BarGenerator(self.on_bar, window=self.period, on_window_bar=self.on_n_min_bar, interval=self.interval)
        self.am = ArrayManager(size=win_size + 1)
        # logger.info(f"fast_window, slow_window, signal_period, period="
        #             f"{self.fast_window, self.slow_window, self.signal_period, self.period}")

    def on_tick(self, tick: TickData):
        """
        Callback of new tick data update.
        """
        self.bg.update_tick(tick)

    def on_bar(self, bar: BarData):
        """
        Callback of new bar data update.
        """
        self.bg.update_bar(bar)

    def on_n_min_bar(self, bar: BarData):
        """"""
        self.am.update_bar(bar)
        if not self.am.inited:
            self.set_signal_pos(0)

        close = bar.close_price
        up, down = self.am.boll(self.win_size, self.dev)
        if close > up:
            # 低位
            self.set_signal_pos(-1 if self.reverse_bs else 1)
        elif close < down:
            # 高位
            self.set_signal_pos(1 if self.reverse_bs else -1)
        else:
            pos = self.get_signal_pos()
            pos = -pos if self.reverse_bs else pos
            mid = (up + down) / 2
            if pos > 0 and close < mid:
                self.set_signal_pos(0)
            elif pos < 0 and close > mid:
                self.set_signal_pos(0)


class MACrossSignal(CtaSignal):
    """
    signal_pos >=1:金叉， <=-1:死叉, 0 无交叉
    数字的绝对值为距离上一个金叉或死叉的距离
    """

    def __init__(self, fast, slow, array_size: typing.Optional[int] = None, period=1):
        self.fast = fast
        self.slow = slow
        if array_size is None:
            array_size = max(fast, slow)
        super().__init__(period=period, array_size=array_size)
        self._last_fast_ma = None
        self._last_slow_ma = None

    def on_window(self, bar: BarData):
        super().on_window(bar)
        slow_ma = self.am.sma(self.slow)
        fast_ma = self.am.sma(self.fast)
        if self._last_fast_ma is not None:
            if fast_ma > slow_ma and self._last_fast_ma <= self._last_slow_ma:
                # 金叉
                self.signal_pos = 1
            elif fast_ma < slow_ma and self._last_fast_ma >= self._last_slow_ma:
                # 死叉
                self.signal_pos = -1
            else:
                if self.signal_pos > 0:
                    self.signal_pos += 1
                elif self.signal_pos < 0:
                    self.signal_pos -= 1
                else:
                    pass

        self._last_fast_ma = fast_ma
        self._last_slow_ma = slow_ma


if __name__ == "__main__":
    pass
