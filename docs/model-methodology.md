# Market and paper methodology

No statistical forecasts or simulations run in v0.1. Analysts are external sources, not model inputs. Historical hit rate is a description of entered records, not a future probability or evidence of skill.

## Structured outcomes

Supported player statistics: points, rebounds, assists, PR, PA, RA and PRA. For combinations the user must supply the verified sum; the service does not manufacture box scores. Team/game markets use the explicitly selected team or both-team total. For moneylines and spreads the actual value is selected-team score minus opponent score; a spread adds the recorded handicap before comparing with zero.

Over/under comparisons push on equality. Integer `at_least` alternatives win on equality. Full NBA moneyline ties should not occur after overtime, but a recorded zero margin is treated as a push under this version's explicit comparison convention; use only rules compatible with it. Regulation/overtime scope must match the locked market. DNP can void or remain action; action without a verified actual result stays pending. Postponed games can remain pending or void according to recorded rules; cancelled games void. Unsupported market-specific conventions must not be approximated.

Parlays use linked selections, not copied predictions. A loss defeats an ordinary accumulator; otherwise unresolved legs keep it pending. All push/void legs return stake. Explicit `reduce_void_legs` removes push/void legs and multiplies remaining **recorded** individual prices, only when those verified terms apply. `void_entire` returns the stake as soon as a push/void triggers the recorded rule. It takes precedence even over another losing leg. Special promotions and revised correlated prices are not modelled. Select a compatible convention or leave returns unavailable.

The calculated original product is displayed separately from the original combined price. A missing displayed price is not replaced with the product for a paper win. No joint probability is computed by multiplying marginal probabilities. Shared-game selections produce correlation warnings.

## Virtual accounting

For stake s and decimal odds d: win profit is s(d−1), loss is −s, push/void is 0. Pending P/L is null. Unknown winning price makes total P/L and ROI unavailable, while known P/L is reported separately. A loss is known to lose its recorded stake even if its price is missing. A fully void entry needs no winning price.

ROI = known complete net profit / total settled stakes, including push/void stakes in the denominator. Pending stakes are excluded; no settled stake means ROI is null. No stake-weighted model accuracy is inferred. Drawdown is the maximum peak-to-trough cumulative virtual P/L in settlement order, with entry id as deterministic tie-break; losing streak resets on non-loss outcomes. Missing returns make full drawdown/streak unavailable.

Break-even probability is 1/d; one-unit binary expected profit is p×d−1. These binary expressions do not include push/void probability. For a three-way model, expected profit is p_win(d−1)−p_loss and p_push contributes zero. Price mathematics does not establish an edge without a validated probability model.

Future derived metrics: offensive efficiency = 100×points/possessions; defensive efficiency uses opponent points; a common approximate possession expression is FGA−ORB+TO+0.44×FTA. These formulas are documented candidates, **not implemented calculations**. Missing inputs and source-specific definitions must be retained when implementing them. Pace requires a documented overtime/minutes adjustment, not an unqualified raw total.
