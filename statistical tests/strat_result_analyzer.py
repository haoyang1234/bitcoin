import os
import json
import glob
import numpy as np
import pandas as pd

#result_folder = "C:\\Projects\\hao_sweetbytes\\Pumpdump&needlecatcher\\"
result_folder = "D:\\bitrepo\\Pumpdump&needlecatcher\\FebAplcsv\\"
os.chdir(result_folder)
total_stats = pd.DataFrame()
for file in glob.glob('*.csv'):
    read_in_file = result_folder + file
    pair_name = file
    print(pair_name)
    
    min_entries = pd.read_csv(read_in_file)
    
    buy_trades = min_entries.loc[min_entries.buy != 0, :]
    buy_trades_ind = list(buy_trades.index)
    
    sell_trades = min_entries.loc[min_entries.sell != 0, :]
    sell_trades_ind = list(sell_trades.index)

    comm_ind = (buy_trades_ind + sell_trades_ind)
    comm_ind.sort()
    all_trades = min_entries.loc[comm_ind, :]

    trade_statistics = pd.DataFrame()
    for i in range(0, int(all_trades.shape[0] / 2)):
        entry_ind = all_trades.index[i * 2]
        exit_ind = all_trades.index[i * 2 + 1]
        entry_time = pd.to_datetime(all_trades.iloc[i * 2, 0])
        exit_time = pd.to_datetime(all_trades.iloc[i * 2 + 1, 0])
        #FIND THE max price between entry time and exit time. 
        pos_time = exit_time - entry_time
        entry_price = min_entries.loc[entry_ind, 'P']
        exit_price = min_entries.loc[exit_ind, 'P']
        price_return = round((all_trades.iloc[i * 2 + 1, 1] - all_trades.iloc[i * 2, 1]) /
                             all_trades.iloc[i * 2, 1] * 10000, 1)
        trade_position = round(all_trades.loc[entry_ind, 'position'], 2)
        trade_pnl = round(all_trades.loc[entry_ind, 'pnl'] + all_trades.loc[exit_ind, 'pnl'], 4)
        init_sell_theo = all_trades.loc[entry_ind, 'selltheo']
        pre_return = round((min_entries.loc[entry_ind, 'P'] - min_entries.loc[entry_ind - 5, 'P']) /
                           min_entries.loc[entry_ind - 5, 'P'] * 10000, 1)
        post_return = round((min_entries.loc[exit_ind + 5, 'P'] - min_entries.loc[exit_ind, 'P']) /
                            min_entries.loc[exit_ind, 'P'] * 10000, 1)
        min_price = round(min(min_entries.loc[entry_ind:exit_ind, 'P']), 8)
        max_price = round(max(min_entries.loc[entry_ind:exit_ind, 'P']), 8)
        trade_df = pd.DataFrame({'entry_time': entry_time, 'exit_time': exit_time, 'pos_time': pos_time,
                                 'price_return': price_return, 'trade_position': trade_position,
                                 'trade_pnl': trade_pnl, 'pre_return': pre_return, 'post_return': post_return,
                                 'min_price': min_price, 'max_price': max_price, 'exit_price': exit_price,
                                 'entry_price': entry_price, 'init_sell_theo': init_sell_theo}, index=[i],
                                columns=['entry_time', 'exit_time', 'pos_time', 'entry_price', 'exit_price',
                                         'min_price', 'max_price', 'price_return', 'trade_pnl', 'pre_return',
                                         'post_return', 'trade_position', 'init_sell_theo'])
        trade_statistics = trade_statistics.append(trade_df)

    trade_statistics['early_exit'] = trade_statistics['post_return'] > trade_statistics['price_return'] / 2
    trade_statistics['late_entry'] = trade_statistics['pre_return'] > trade_statistics['price_return'] / 2
    trade_statistics['tp_at_selltheo'] = trade_statistics['exit_price'] > trade_statistics['init_sell_theo']

    pair_stats = {}
    columns = ['total_pnl', 'number_of_trades', 'avg_profit', 'pnl_std', 'min_pnl', 'max_pnl',
               'early_exit_ratio', 'late_entry_ratio', 'avg_pos_time', 'tp_at_selltheo']
    pair_stats['total_pnl'] = round(np.sum(trade_statistics.loc[:, 'trade_pnl']), 2)
    pair_stats['number_of_trades'] = trade_statistics.shape[0]
    pair_stats['avg_profit'] = round(pair_stats['total_pnl'] / pair_stats['number_of_trades'], 2)
    pair_stats['pnl_std'] = round(trade_statistics.trade_pnl.std(), 2)
    pair_stats['min_pnl'] = round(trade_statistics.trade_pnl.min(), 2)
    pair_stats['max_pnl'] = round(trade_statistics.trade_pnl.max(), 2)
    pair_stats['early_exit_ratio'] = round(np.sum(trade_statistics.early_exit) / all_trades.shape[0] * 2 * 100, 2)
    pair_stats['late_entry_ratio'] = round(np.sum(trade_statistics.late_entry) / all_trades.shape[0] * 2 * 100, 2)
    pair_stats['tp_at_selltheo'] = round(np.sum(trade_statistics['tp_at_selltheo']) / all_trades.shape[0] * 100, 2)
    pair_stats['avg_pos_time'] = np.mean(trade_statistics.pos_time)
    ps = pd.DataFrame(pair_stats, index=[pair_name], columns=columns)
    total_stats = total_stats.append(ps)

print(total_stats)
