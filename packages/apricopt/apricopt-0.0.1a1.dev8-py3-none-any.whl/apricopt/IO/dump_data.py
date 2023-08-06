"""
This file is part of Apricopt.

Apricopt is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Apricopt is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Apricopt.  If not, see <http://www.gnu.org/licenses/>.

Copyright (C) 2020 Marco Esposito, Leonardo Picchiami.
"""

from typing import List, Dict
import csv

from apricopt.model.Model import Model


def write_vps_header_to_tsv(initialization_model: Model, admissibility_model: Model, treatments, filename: str):
    ids = [p_id for p_id in initialization_model.parameters.keys()]
    ids.sort()

    treatment_results_ids = [tr.id for tr in admissibility_model.treatment_results]
    results_keys = []
    for treatment_id in treatments.keys():
        results_keys += [f"{result_id}_{treatment_id}" for result_id in treatment_results_ids]

    # response_keys = [f"{admissibility_model.treatment_results.id}_{treatment_id}" for treatment_id in treatments.keys()]
    #response_keys.sort()

    results_keys.sort()

    keys = ['id', 'init_time', 'admissible', 'response'] + results_keys + ids
    with open(filename, "w") as f:
        writer = csv.writer(f, delimiter='\t')
        writer.writerow(keys)


def dump_virtual_patients_to_PEtab_tsv(model: Model, virtual_patients: List[Dict], filename: str):
    keys = list(virtual_patients[0].keys())
    keys.remove('id')
    keys.remove('init_time')
    keys.remove('admissible')
    keys.remove('response')
    #response_keys = [k for k in keys if k.startswith(f"{model.treatment_results.id}_")]
    response_keys = [k for k in keys if any(k.startswith(f"{tr.id}_") for tr in model.treatment_results)]
    response_keys.sort()
    for k in response_keys: keys.remove(k)
    keys.sort()
    keys.insert(0, 'id')
    keys.insert(1, 'init_time')
    keys.insert(2, 'admissible')
    keys.insert(3, 'response')
    for i in range(len(response_keys)):
        keys.insert(4+i, response_keys[i])

    with open(filename, "a") as f:
        writer = csv.writer(f, delimiter='\t')
        lines = []
        for vp in virtual_patients:
            line = []
            for key in keys:
                line += [vp[key]]
            lines+=[line]
        writer.writerows(lines)
