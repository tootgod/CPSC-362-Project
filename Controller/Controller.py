from abc import ABC, abstractmethod
import Model.SmaBacktest as sma
import Model.MACDBacktest as MACD
import Model.BBbacktest as BB


class TradingStrategy(ABC):
    @abstractmethod
    def getName(self):
        pass

    @abstractmethod
    def getBacktestResults(self, sec):
        pass

    @abstractmethod
    def plot(self, dpg, sec, results):
        pass


class SMAStrategy(TradingStrategy):
    def getName(self):
        return "SMA"
    
    def getBacktestResults(self, sec):
        return sma.backtest_sma(sec)
    
    def plot(self, dpg, sec, results):
        (
            balance, total_gain_loss, annual_return, total_return,
            _, _, smasmalllist, smabiglist, tdateB, tdateS, tHeightB, tHeightS
        ) = results

        dpg.add_text(f"{self.getName()} Backtest Results")
        dpg.add_text(f"Final Balance: ${balance:,.2f}")
        dpg.add_text(f"Total Gain/Loss: ${total_gain_loss:,.2f}")
        dpg.add_text(f"Annual Return: {annual_return:.2f}%")
        dpg.add_text(f"Total Return: {total_return:.2f}%")
        
        with dpg.plot(label="Closing Prices", height=600, width=900):
            dpg.add_plot_legend()
            dpg.add_plot_axis(dpg.mvXAxis, label="Trade number", time=True)
            y_axis = dpg.add_plot_axis(dpg.mvYAxis, label="Capital")
            dpg.set_axis_limits_auto(y_axis)
            dpg.add_scatter_series(tdateB, tHeightB, parent=y_axis, label="Buy Signal")
            dpg.add_scatter_series(tdateS, tHeightS, parent=y_axis, label="Sell Signal")
            dpg.add_line_series(sec.historical_dates, smasmalllist, parent=y_axis, label="SMA Long Data")
            dpg.add_line_series(sec.historical_dates, smabiglist, parent=y_axis, label="SMA Short Data")


class BBStrategy(TradingStrategy):
    def getName(self):
        return "BB"
    
    def getBacktestResults(self, sec):
        return BB.BB_backtest(sec)
    
    def plot(self, dpg, sec, results):
        (
            balance, total_gain_loss, annual_return, total_return,
            _, _, mband, uband, lband, tDateB, tDateS, tHeightB, tHeightS
        ) = results

        dpg.add_text(f"{self.getName()} Backtest Results")
        dpg.add_text(f"Final Balance: ${balance:,.2f}")
        dpg.add_text(f"Total Gain/Loss: ${total_gain_loss:,.2f}")
        dpg.add_text(f"Annual Return: {annual_return:.2f}%")
        dpg.add_text(f"Total Return: {total_return:.2f}%")

        with dpg.plot(label="Closing Prices", height=600, width=900):
            dpg.add_plot_legend()
            dpg.add_plot_axis(dpg.mvXAxis, label="Trade number", time=True)
            y_axis = dpg.add_plot_axis(dpg.mvYAxis, label="Capital")
            dpg.set_axis_limits_auto(y_axis)
            dpg.add_scatter_series(tDateB, tHeightB, parent=y_axis, label="Buy Signal")
            dpg.add_scatter_series(tDateS, tHeightS, parent=y_axis, label="Sell Signal")
            dpg.add_line_series(sec.historical_dates, sec.historical_closes, parent=y_axis, label="Closes")
            dpg.add_line_series(sec.historical_dates, mband, parent=y_axis, label="Middle Band")
            dpg.add_line_series(sec.historical_dates, uband, parent=y_axis, label="Upper Band")
            dpg.add_line_series(sec.historical_dates, lband, parent=y_axis, label="Lower Band")


class MACDStrategy(TradingStrategy):
    def getName(self):
        return "MACD"
    
    def getBacktestResults(self, sec):
        macd_backtest = MACD.MACDBacktest(sec.historical_data, symbol="MACD")
        summary, tdateB, tdateS, tHeightB, tHeightS = macd_backtest.run()
        macd_line, signal_line = macd_backtest.calculate_macd()
        return summary, tdateB, tdateS, tHeightB, tHeightS, macd_line, signal_line
    
    def plot(self, dpg, sec, results):
        summary, tdateB, tdateS, tHeightB, tHeightS, macd_line, signal_line = results

        # Ensure lines are converted to lists
        macd_line = macd_line.to_list() if hasattr(macd_line, 'to_list') else macd_line
        signal_line = signal_line.to_list() if hasattr(signal_line, 'to_list') else signal_line

        # Ensure the lengths of MACD and signal lines match the dates
        min_length = min(len(sec.historical_dates), len(macd_line), len(signal_line))
        dates = sec.historical_dates[:min_length]
        macd_line = macd_line[:min_length]
        signal_line = signal_line[:min_length]

        # Display the results summary
        dpg.add_text(f"{self.getName()} Backtest Results")
        dpg.add_text(f"Final Balance: ${summary['final_balance']:,.2f}")
        dpg.add_text(f"Total % Return: {summary['percent_return']:.2f}%")

        # Plot the results
        with dpg.plot(label="Closing Prices", height=600, width=900):
            dpg.add_plot_legend()
            dpg.add_plot_axis(dpg.mvXAxis, label="Trade number", time=True)
            y_axis = dpg.add_plot_axis(dpg.mvYAxis, label="Capital")
            dpg.set_axis_limits_auto(y_axis)

            dpg.add_scatter_series(tdateB, tHeightB, parent=y_axis, label="Sell Signal") #we flipped them buy over signal, sell under signal
            dpg.add_scatter_series(tdateS, tHeightS, parent=y_axis, label="Buy Signal")
            dpg.add_line_series(dates, macd_line, parent=y_axis, label="MACD")  # Red for MACD line
            dpg.add_line_series(dates, signal_line, parent=y_axis, label="Signal")  # Blue for Signal line

