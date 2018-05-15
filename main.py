"""
Mean Reversion Hypothesis: When the 20-day SMA is lower than the 30-day SMA, open a long position. When the 10-daqy SMA is higher than the 30-day SMA, open a short position. Position size is proportional to the difference between the 10- & 30-day SMAs.
"""

def initialize(context):
    
    context.security_list = [sid(5060), sid(7792), sid(1941), sid(24556), sid(1746)]
    
    schedule_function(rebalance,
                      date_rules.week_start(),
                      time_rules.market_open())
    
    schedule_function(record_vars,
                     date_rules.every_day(),
                     time_rules.market_close())
    
def compute_weights(context, data):
    
    hist = data.history(context.security_list, 'price', 30, 'ld')
    
    prices_10 = hist[-10:]
    prices_30 = hist[-30:]
    
    sma_10 = prices_10.mean()
    sma_30 = prices_30.mean()
    
    raw_weights = (sma_10 - sma_30) / sma30
    
    normalized_weights = raw_weights / raw_weihts.abs().sum()
    
    return normalized_weights
                     
#rebalance gets calles once at the beginning of each week + adjust positions
#adjusting based on calculated weights
def rebalance(context, data):
    
    weights = compute_weights(context, data)
    
    for security in context.security_list:
        
    if data.can_trade(security):
        order_target_percent(security, weights[security])
        
def record_vars(context, data):
    
    longs = shorts = 0
    
    for position in context.portfolio.positions.itervalues():
        if position.amount > 0:
            longs += 1
        elif position.amount < 0:
            shorts += 1
            
  record(leverage=context.account.leverage, long_count=longs, short_count=shorts)                        
                   
