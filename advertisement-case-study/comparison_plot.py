import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

opt_prices_df_exp = pd.read_csv("campaign_results.csv")

idxs_daily = [opt_prices_df_exp[opt_prices_df_exp.rounds == i]["safe_idx"].values.tolist() for i in range(25)]
rois = []
revenues = []
costs = []
clicks = []
cpc = []
safe_set_sizes = []
payprices = []
bidprices = []

for i in range(25):

    batch = opt_prices_df_exp[opt_prices_df_exp.rounds == i]
    bid_rows = batch[batch.opt_prices > 0]
    rois.append(np.sum(bid_rows["click"]) / np.sum(bid_rows["opt_prices"]))
    revenues.append(np.sum(bid_rows["click"] * np.abs(bid_rows["opt_prices"])))
    costs.append(np.sum(np.abs(bid_rows["opt_prices"])))
    total_achievable_clicks = np.sum(bid_rows["click"])
    achieved_click = np.sum(bid_rows[(bid_rows.click > 0) & (bid_rows.click_predictions_mean > 0)]["click"])
    clicks.append(100*achieved_click/total_achievable_clicks)
    cpc.append(np.sum(bid_rows[bid_rows > 0]["opt_prices"])/bid_rows[bid_rows > 0]["click"].count())
    safe_set_sizes.append(len(batch[batch.opt_prices > 0])/ len(batch))
    payprices.append(bid_rows["payprice"].mean())
    bidprices.append(bid_rows["opt_prices"].mean())

days = [i for i in range(26)]

payprices = [0] + payprices
bidprices = [0] + bidprices
rois = [0] + rois

plt.figure(figsize=(9,5))
plt.step(days, payprices, label="Benchmark bidding prices", color="red", linewidth=1.5)
plt.step(days, bidprices, label="Optimized bidding prices", color="steelblue", linewidth=1.5)
plt.title("Comparison of mean bidding prices", fontsize=12)
plt.ylim([0, 91])
plt.yticks([i for i in range(0, 91, 10)])
plt.xticks([i for i in range(26)])
plt.margins(0,0)
plt.xlabel("Campaigns")
plt.ylabel("Mean bid prices")
plt.legend()
plt.savefig("Comparison-bidding-prices.png", dpi=600)
