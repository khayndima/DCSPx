from itertools import combinations

def ensemble_lambdas(lam_dc, lam_ext, w=0.6):
    if lam_ext:
        return (w * lam_dc[0] + (1 - w) * lam_ext[0],
                w * lam_dc[1] + (1 - w) * lam_ext[1])
    return lam_dc

def ensemble_probs(probs_dc, probs_ext, w=0.6):
    if probs_ext:
        blended = {k: w * probs_dc[k] + (1 - w) * probs_ext[k] for k in probs_dc}
        total = sum(blended.values())
        return {k: v / total for k, v in blended.items()}
    return probs_dc

def compute_ev(prob, odds):
    return prob * (odds - 1) - (1 - prob)

def optimize_parlay(predictions, max_legs=3, min_ev=0.05, market_type="1X2"):
    parlays = []
    for r in range(2, max_legs + 1):
        for combo in combinations(predictions, r):
            legs = []
            total_prob = 1.0
            total_odds = 1.0
            valid = True
            for match in combo:
                if market_type == "1X2":
                    evs = {'home': match['EV_home'], 'draw': match['EV_draw'], 'away': match['EV_away']}
                    best = max(evs, key=evs.get)
                    if evs[best] < min_ev:
                        valid = False
                        break
                    prob = match[f'P_{best}']
                    odds = match[f'odds_{best}']
                    legs.append(f"{match['fixture']} → {best.upper()} @ {odds}")
                elif market_type == "BTTS":
                    if match['EV_BTTS'] < min_ev:
                        valid = False
                        break
                    prob = match['BTTS_prob']
                    odds = match['odds_BTTS']
                    legs.append(f"{match['fixture']} → BTTS @ {odds}")
                else:
                    if match['EV_Over25'] < min_ev:
                        valid = False
                        break
                    prob = match['Over25_prob']
                    odds = match['odds_Over25']
                    legs.append(f"{match['fixture']} → Over 2.5 @ {odds}")
                total_prob *= prob
                total_odds *= odds
            if valid:
                expected_return = total_prob * (total_odds - 1)
                parlays.append({'legs': legs, 'return': round(expected_return, 2)})
    return sorted(parlays, key=lambda x: x['return'], reverse=True)[:5]
