cryptalis - IBKR - Code Repository
------------

### Strategy Description

### Clémence and Clementine Strategy

**Overview:**
This strategy involves two bots, Clémence and Clementine, designed to trade based on candle movements. Clémence is a long bot, while Clementine is a short bot. The strategy
capitalizes on the directional movements of the EUR/USD pair.

### Strategy Details:

#### 1. **Initial Setup:**

- **Clémence (Long Bot):** Buys when the candle moves up.
- **Clementine (Short Bot):** Sells when the candle moves down.

#### 2. **Entry Conditions:**

- **Clémence:**
    - Enters a long position when the candle moves upward.
- **Clementine:**
    - Enters a short position when the candle moves downward.

#### 3. **Exit Conditions:**

- **Clémence:**
    - Exits the trade when the candle stops moving upward or reaches a stop-loss.
- **Clementine:**
    - Exits the trade when the candle stops moving downward or reaches a stop-loss.

#### 4. **Stop-Loss and Take-Profit:**

- **Stop-Loss:**
    - Clémence sets a stop-loss at a level to minimize losses if the price moves downward.
    - Clementine sets a stop-loss at a level to minimize losses if the price moves upward.
- **Take-Profit:**
    - Both bots aim to maximize profits based on the movement of the candle.

#### 5. **Profit Sharing:**## this we will talk about later

- When a candle moves in one direction:
    - Clémence profits from upward movements and exits at the stop-loss or take-profit level.
    - Clementine profits from downward movements and exits at the stop-loss or take-profit level.
- After each trade cycle:
    - Profits are split, and both bots reinvest the profits into new positions.

### Example Trading Cycle:

1. **Candle Moves Up:**
    - **Clémence:** Buys EUR/USD.
    - **Clementine:** Exits short position (if any) at a stop-loss.
    - **Clémence:** Takes profit or stops out.
    - **Clementine:** Re-enters a short position if the price starts to fall.
2. **Candle Moves Down:**
    - **Clementine:** Sells EUR/USD.
    - **Clémence:** Exits long position (if any) at a stop-loss.
    - **Clementine:** Takes profit or stops out.
    - **Clémence:** Re-enters a long position if the price starts to rise.

### Implementation Steps:

1. **Bot Development:**
    - Develop the bots with the ability to detect candle movements and execute trades accordingly.
    - Integrate stop-loss and take-profit mechanisms.
2. **Backtesting:**
    - Backtest the strategy using historical EUR/USD data to ensure its effectiveness.
3. **Deployment:**
    - Deploy the bots in a live trading environment with real-time data feeds.
4. **Monitoring:**
    - Continuously monitor the bots’ performance and make adjustments as necessary to optimize profitability.
      This strategy is designed to take advantage of short-term movements in the EUR/USD pair by having two specialized bots that work in tandem to capture profits from both upward
      and downward movements.

### Invocation

`docker-compose up`
