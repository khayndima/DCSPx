from betting_utils import ensemble_lambdas, ensemble_probs, compute_ev

def predict_match(home, away, date, odds, dc_model, external_model=None):
    lam_dc = dc_model.predict_expected_goals(home, away, date)
    lam_ext = external_model.predict_expected_goals(home, away, date) if external_model else None

    lam_h, lam_a = ensemble_lambdas(lam_dc, lam_ext)
    matrix = dc_model.score_matrix(lam_h, lam_a)
    probs_12 = dc_model.outcome_probs(matrix)
    extra = dc_model.extra_probs(matrix)

    probs_ext = external_model.predict_probs(home, away, date) if external_model else None
    probs = ensemble_probs(probs_12, probs_ext)

    return {
        'fixture': f"{home} vs {away}",
        'λ_home': round(lam_h, 2),
        'λ_away': round(lam_a, 2),
        'P_home': round(probs['home'], 3),
        'P_draw': round(probs['draw'], 3),
        'P_away': round(probs['away'], 3),
        'EV_home': round(compute_ev(probs['home'], odds['home']), 3),
        'EV_draw': round(compute_ev(probs['draw'], odds['draw']), 3),
        'EV_away': round(compute_ev(probs['away'], odds['away']), 3),
        'BTTS_prob': round(extra['BTTS'], 3),
        'Over25_prob': round(extra['Over25'], 3),
        'EV_BTTS': round(compute_ev(extra['BTTS'], odds['BTTS']), 3),
        'EV_Over25': round(compute_ev(extra['Over25'], odds['Over25']), 3),
        'Top_outcome': max(probs, key=probs.get)
    }
