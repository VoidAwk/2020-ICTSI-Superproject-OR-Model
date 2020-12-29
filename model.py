import numpy as np
import json

'''
Parameter definitions
'''
teu = {
    'L': 6.096,
    'H': 2.591,
    'W': 2.438
}

speeds = {
    'gantry': {
        'empty': 90,
        'loaded': 45
    },
    'trolley': {
        'empty': 70,
        'loaded': 70
    },
    'hoisting': {
        'empty': 24,
        'loaded': 12
    }
}

'''
Objective Function Components
'''


def expected_ct_receiving(L, H, W, dim=teu, speeds=speeds):
    gantry_range = {
        'min': 0,
        'max': L * dim.get('L')
    }
    trolley_range = {
        'min': 0,
        'max': W * dim.get('W')
    }
    hoisting_range = {
        'min': 0,
        'max': 15.4
    }

    times = []

    # 1: Max(T-rcte, T-rrge)
    e_D_rcte = (trolley_range.get('min') + trolley_range.get('max')) / 2
    e_T_rcte = e_D_rcte / speeds.get('trolley').get('empty')

    e_D_rrge = (gantry_range.get('min') + gantry_range.get('max')) / 2
    e_T_rrge = e_D_rrge / speeds.get('gantry').get('empty')

    times.append(e_T_rcte if e_T_rcte >= e_T_rrge else e_T_rrge)

    # 2: t-tche
    e_t_tche = (hoisting_range.get('max')) / \
        speeds.get('hoisting').get('empty')

    times.append(e_t_tche)

    # 3: t-p
    e_t_p = 5 / 60  # 5 seconds

    times.append(e_t_p)

    # 4: t-cthl
    e_t_cthl = (hoisting_range.get('max')) / \
        speeds.get('hoisting').get('loaded')

    times.append(e_t_cthl)

    # 5: T-crtl
    e_D_crtl = (trolley_range.get('min') + trolley_range.get('max')) / 2
    e_T_crtl = e_D_crtl / speeds.get('trolley').get('loaded')

    times.append(e_T_crtl)

    # 6: T-trhl
    e_D_trhl = (hoisting_range.get('min') + hoisting_range.get('max')) / 2
    e_T_trhl = e_D_trhl / speeds.get('hoisting').get('loaded')

    times.append(e_T_trhl)

    # 7: t-r
    e_t_r = 5 / 60  # 5 seconds

    times.append(e_t_r)

    # 8: T-rthe
    e_D_rthe = (hoisting_range.get('min') + hoisting_range.get('max')) / 2
    e_T_rthe = e_D_rthe / speeds.get('hoisting').get('empty')

    times.append(e_T_rthe)

    return sum(times)


def expected_ct_loading(L, H, W, dim=teu, speeds=speeds):
    gantry_range = {
        'min': 0,
        'max': L * dim.get('L')
    }
    trolley_range = {
        'min': 0,
        'max': W * dim.get('W')
    }
    hoisting_range = {
        'min': 0,
        'max': 15.4
    }

    times = []

    # 1: Max(T-crte, T-rrge) (f=1/l0)
    l0 = 10  # Assumption
    e_D_crte = (trolley_range.get('min') + trolley_range.get('max')) / 2
    e_T_crte = e_D_crte / speeds.get('trolley').get('empty')

    e_D_rrge = (gantry_range.get('min') + gantry_range.get('max')) / 2
    e_T_rrge = e_D_rrge / speeds.get('gantry').get('empty')

    times.append((e_T_crte if e_T_crte >= e_T_rrge else e_T_rrge) * (1 / l0))

    # 2: T-trhe
    e_D_trhe = (hoisting_range.get('min') + hoisting_range.get('max')) / 2
    e_T_trhe = e_D_trhe / speeds.get('hoisting').get('empty')

    times.append(e_T_trhe)

    # 3: t-p
    e_t_p = 5 / 60  # 5 seconds

    times.append(e_t_p)

    # 4: T-rthl
    e_D_rthl = (hoisting_range.get('min') + hoisting_range.get('max')) / 2
    e_T_rthl = e_D_rthl / speeds.get('hoisting').get('loaded')

    times.append(e_T_rthl)

    # 5: T-rctl
    e_D_rctl = (trolley_range.get('min') + trolley_range.get('max')) / 2
    e_T_rctl = e_D_rctl / speeds.get('trolley').get('loaded')

    times.append(e_T_rctl)

    # 6: t-tchl
    e_D_tchl = hoisting_range.get('max')
    e_t_tchl = e_D_tchl / speeds.get('hoisting').get('loaded')

    times.append(e_t_tchl)

    # 7: t-r
    e_t_r = 5 / 60  # 5 seconds

    times.append(e_t_r)

    # 8: t-cthe
    e_D_cthe = hoisting_range.get('max')
    e_t_cthe = e_D_cthe / speeds.get('hoisting').get('empty')

    times.append(e_t_cthe)

    # 9: T-crte (f=(l0-1)/l0)
    l0 = 10  # Assumption
    e_D_crte = (trolley_range.get('min') + trolley_range.get('max')) / 2
    e_T_crte = e_D_crte / speeds.get('trolley').get('empty')

    times.append(e_T_crte * (l0-1) / l0)

    return sum(times)


def expected_ct_discharging(L, W, H, dim=teu, speeds=speeds):
    gantry_range = {
        'min': 0,
        'max': L * dim.get('L')
    }
    trolley_range = {
        'min': 0,
        'max': W * dim.get('W')
    }
    hoisting_range = {
        'min': 0,
        'max': 15.4
    }

    times = []

    # 1: Max(T-rcte, T-rrge) (f=(1/uwh))
    uwh = W * H - (H - 1)
    e_D_rcte = (trolley_range.get('min') + trolley_range.get('max')) / 2
    e_T_rcte = e_D_rcte / speeds.get('trolley').get('empty')

    e_D_rrge = (gantry_range.get('min') + gantry_range.get('max')) / 2
    e_T_rrge = e_D_rrge / speeds.get('gantry').get('empty')

    time_1 = e_T_rcte if e_T_rcte >= e_T_rrge else e_T_rrge
    time_1 = time_1 / uwh

    times.append(time_1)

    # 2: t-tche
    e_t_tche = (hoisting_range.get('max')) / \
        speeds.get('hoisting').get('empty')

    times.append(e_t_tche)

    # 3: t-p
    e_t_p = 5 / 60  # 5 seconds

    times.append(e_t_p)

    # 4: t-cthl
    e_t_cthl = (hoisting_range.get('max')) / \
        speeds.get('hoisting').get('loaded')

    times.append(e_t_cthl)

    # 5: T-crtl
    e_D_crtl = (trolley_range.get('min') + trolley_range.get('max')) / 2
    e_T_crtl = e_D_crtl / speeds.get('trolley').get('loaded')

    times.append(e_T_crtl)

    # 6: T-trhl
    e_D_trhl = (hoisting_range.get('min') + hoisting_range.get('max')) / 2
    e_T_trhl = e_D_trhl / speeds.get('hoisting').get('loaded')

    times.append(e_T_trhl)

    # 7: t-r
    e_t_r = 5 / 60  # 5 seconds

    times.append(e_t_r)

    # 8: T-rthe
    e_D_rthe = (hoisting_range.get('min') + hoisting_range.get('max')) / 2
    e_T_rthe = e_D_rthe / speeds.get('hoisting').get('empty')

    times.append(e_T_rthe)

    # 9: T-rcte (f=(uwh-1)/uwh)
    e_D_rcte = (trolley_range.get('min') + trolley_range.get('max')) / 2
    e_T_rcte = e_D_rcte / speeds.get('trolley').get('empty')
    e_T_rcte = e_T_rcte * (uwh-1) / uwh

    times.append(e_T_rcte)

    return sum(times)


def expected_ct_delivering(L, W, H, dim=teu, speeds=speeds):
    gantry_range = {
        'min': 0,
        'max': L * dim.get('L')
    }
    trolley_range = {
        'min': 0,
        'max': W * dim.get('W')
    }
    hoisting_range = {
        'min': 0,
        'max': 15.4
    }

    times = []

    # 1: Max(T-crte, T-rrge)
    e_D_crte = (trolley_range.get('min') + trolley_range.get('max')) / 2
    e_T_crte = e_D_crte / speeds.get('trolley').get('empty')

    e_D_rrge = (gantry_range.get('min') + gantry_range.get('max')) / 2
    e_T_rrge = e_D_rrge / speeds.get('gantry').get('empty')

    times.append(max([e_T_crte, e_T_rrge]))

    # 2: TR (f=Rwh)
    def expected_ct_rehandling(L, W, H, dim=dim, speeds=speeds):
        gantry_range = {
            'min': 0,
            'max': L * dim.get('L')
        }
        trolley_range = {
            'min': 0,
            'max': W * dim.get('W')
        }
        hoisting_range = {
            'min': 0,
            'max': 15.4
        }

        times = []

        # 1: T-trhe
        e_D_trhe = (hoisting_range.get('min') + hoisting_range.get('max')) / 2
        e_T_trhe = e_D_trhe / speeds.get('hoisting').get('empty')

        times.append(e_T_trhe)

        # 2: t-p
        e_t_p = 5 / 60  # 5 seconds

        times.append(e_t_p)

        # 3: T-rthl
        e_D_rthl = (hoisting_range.get('min') + hoisting_range.get('max')) / 2
        e_T_rthl = e_D_rthl / speeds.get('hoisting').get('loaded')

        times.append(e_T_rthl)

        # 4: T-rrtl
        e_D_rrtl = (trolley_range.get('min') + trolley_range.get('max')) / 2
        e_T_rrtl = e_D_rrtl / speeds.get('trolley').get('loaded')

        times.append(e_T_rrtl)

        # 5: T-trhl
        e_D_trhl = (hoisting_range.get('min') + hoisting_range.get('max')) / 2
        e_T_trhl = e_D_trhl / speeds.get('hoisting').get('loaded')

        times.append(e_T_trhl)

        # 6: t-r
        e_t_r = 5 / 60  # 5 seconds

        times.append(e_t_r)

        # 7: T-rthe
        e_D_rthe = (hoisting_range.get('min') + hoisting_range.get('max')) / 2
        e_T_rthe = e_D_rthe / speeds.get('hoisting').get('empty')

        times.append(e_T_rthe)

        # 8: T-rrte
        e_D_rrte = (trolley_range.get('min') + trolley_range.get('max')) / 2
        e_T_rrte = e_D_rrte / speeds.get('trolley').get('empty')

        times.append(e_T_rrte)

        return sum(times)

    Rwh = (H - 1) / 4 + (H + 2) / (16 * W)
    times.append(expected_ct_rehandling(L, W, H, dim=dim, speeds=speeds) * Rwh)

    # 3: T-trhe
    e_D_trhe = (hoisting_range.get('min') + hoisting_range.get('max')) / 2
    e_T_trhe = e_D_trhe / speeds.get('hoisting').get('empty')

    times.append(e_T_trhe)

    # 4: t-p
    e_t_p = 5 / 60  # 5 seconds

    times.append(e_t_p)

    # 5: T-rthl
    e_D_trhl = (hoisting_range.get('min') + hoisting_range.get('max')) / 2
    e_T_trhl = e_D_trhl / speeds.get('hoisting').get('loaded')

    times.append(e_T_trhl)

    # 6: T-rctl
    e_D_rctl = (trolley_range.get('min') + trolley_range.get('max')) / 2
    e_T_rctl = e_D_rctl / speeds.get('trolley').get('loaded')

    times.append(e_T_rctl)

    # 7: t-tchl
    e_D_tchl = hoisting_range.get('max')
    e_t_tchl = e_D_tchl / speeds.get('hoisting').get('loaded')

    times.append(e_t_tchl)

    # 8: t-r
    e_t_r = 5 / 60  # 5 seconds

    times.append(e_t_r)

    # 9: t-cthe
    e_D_cthe = hoisting_range.get('max')
    e_t_cthe = e_D_cthe / speeds.get('hoisting').get('empty')

    times.append(e_t_cthe)

    return sum(times)


'''
Addtl. Program Parameters & Constraints
'''
bounds_L = {'min': 1, 'max': 100}
bounds_H = {'min': 1, 'max': 8}
bounds_W = {'min': 1, 'max': 100}
min_storage = 6 * 5 * 16
alphas = [0.5, 0.6, 0.7, 0.8, 0.9]

results = []
for alpha in alphas:
    alpha_result = []
    for L in range(bounds_L.get('min'), bounds_L.get('max') + 1):
        for H in range(bounds_H.get('min'), bounds_H.get('max') + 1):
            for W in range(bounds_W.get('min'), bounds_W.get('max') + 1):
                alpha_result.append({'configuration': (L, H, W),
                                     'pho_c': alpha * expected_ct_loading(L, H, W) + (1 - alpha) * expected_ct_receiving(L, H, W),
                                     'phi_c': alpha * expected_ct_discharging(L, H, W) + (1 - alpha) * expected_ct_delivering(L, H, W)})
    results.append({'alpha': alpha, 'results': alpha_result})


with open('raw-model-results.json', 'w') as f:
    json.dump(results, f, indent=4)

'''
Data processing
'''
results_file = 'raw-model-results.json'
with open(results_file, 'r') as f:
    total_results = json.load(f)

'''
Addtl. filtering
'''
min_size = 480  # 6 x 16 x 5
max_stack_height = 5

report = []

for alpha in total_results:
    alpha_results = alpha.get('results')
    filtered_results = []
    for result in alpha_results:
        if (np.prod(result.get('configuration')) >= min_size) and \
                (result.get('configuration')[1] <= max_stack_height):
            filtered_results.append(result)
    min_pho_c = min([i.get('pho_c') for i in filtered_results])
    min_pho_c_config = [
        i for i in filtered_results if i.get('pho_c') <= min_pho_c][0]
    min_phi_c = min([i.get('phi_c') for i in filtered_results])
    min_phi_c_config = [
        i for i in filtered_results if i.get('phi_c') <= min_phi_c][0]
    report.append({'alpha': alpha.get('alpha'),
                   'optimum pho-c': {'config': min_pho_c_config.get('configuration'), 'value': min_pho_c},
                   'optimum phi-c': {'config': min_phi_c_config.get('configuration'), 'value': min_phi_c}
                   })

with open('report.json', 'w') as f:
    json.dump(report, f, indent=4, sort_keys=True)
